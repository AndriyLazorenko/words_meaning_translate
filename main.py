import requests
from textblob import Word
from textblob.wordnet import VERB
import pandas as pd
# from translate import Translator
# translator = Translator(to_lang="uk")

from mtranslate import translate


class MeaningTranslator:
    def __init__(self):
        self.df = pd.read_csv("in.csv", header=None)
        self.demo = self.df[1].dropna()
        self.app_id = 'e94904db'
        self.app_key = '25a83eec3bcd55a917ea1cd654a8696b'
        self.lang = 'en'
        self.debug_mode = True

    def get_meanings(self, words):
        ret = list()
        for word in words:
            w_list = word.split()
            if len(w_list) == 1:
                w = Word(word)
                try:
                    ret.append(w.definitions[0])
                except:
                    self.get_oxford_definition(ret, word)
            elif len(w_list) == 2:
                if w_list[0] == 'to':
                    w = Word(w_list[1])
                    try:
                        v = w.get_synsets(pos=VERB)
                        ret.append(v[0].definition())
                    except:
                        self.get_oxford_definition(ret, word)
                elif w_list[0] == 'a' or w_list[0] == 'an':
                    w = Word(w_list[1])
                    try:
                        ret.append(w.definitions[0])
                    except:
                        self.get_oxford_definition(ret, word)
                else:
                    ret.append('NOT IMPLEMENTED FOR 2 OR MORE WORDS')
            else:
                ret.append('NOT IMPLEMENTED FOR 2 OR MORE WORDS')
        return ret

    def get_oxford_definition(self, ret, word):
        if not self.debug_mode:
            try:
                url = 'https://od-api.oxforddictionaries.com:443/api/v1/entries/' + self.lang + '/' + word.lower()
                r = requests.get(url, headers={'app_id': self.app_id, 'app_key': self.app_key})
                meaning = r.json()['results'][0]['lexicalEntries'][0]['entries'][0]['senses'][0]['definitions'][0]
                ret.append(meaning)
            except:
                ret.append('NO MEANING FOUND')
        else:
            ret.append('NO MEANING FOUND')

    @staticmethod
    def get_translations(words):
        ret = list()
        num_words = len(words)
        i = 0
        tenth = num_words // 10
        word_ind = 0
        print('Starting translation...')
        for word in words:
            word_ind += 1
            if word_ind % tenth == 0:
                i += 1
                print(f'{10*i} % of words are translated')
            transl = translate(word, 'uk')
            ret.append(transl)

        return ret

    @staticmethod
    def form_dict(words, meanings, translations):
        out = dict()
        out['words'] = words
        out['meanings'] = meanings
        out['translations'] = translations
        return out

    def save_df(self, dic):
        df = pd.DataFrame.from_dict(dic)
        print(df)
        df.to_csv('out.csv')

    def run(self):
        words = self.demo
        meanings = self.get_meanings(self.demo)
        translations = self.get_translations(self.demo)
        out = self.form_dict(words, meanings, translations)
        self.save_df(out)


if __name__ == '__main__':
    mt = MeaningTranslator()
    mt.run()

