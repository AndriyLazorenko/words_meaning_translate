from googletrans import Translator
from textblob import Word
import pandas as pd
# from translate import Translator
# translator = Translator(to_lang="uk")

from mtranslate import translate


def get_meanings(words):
    ret = list()
    for word in words:
        w_list = word.split()
        if len(w_list) == 1:
            w = Word(word)
            try:
                ret.append(w.definitions[0])
            except:
                ret.append('NO MEANING FOUND')
        else:
            ret.append('NOT IMPLEMENTED FOR 2 OR MORE WORDS')
    return ret


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


def get_google_translations(words, translator):
    res = list()
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
        print(f'word: {word}')
        transl = translator.translate(word, 'uk')
        print(f'transl: {transl.text}')
        res.append(transl.text)

    return res


if __name__ == '__main__':
    df = pd.read_csv("in.csv", header=None)
    demo = df[1].dropna()

    translator = Translator()

    words = demo
    meanings = get_meanings(demo)
    translations = get_translations(demo)
    google_translations = get_google_translations(demo, translator)

    out = dict()
    out['words'] = words
    out['meanings'] = meanings
    out['translations'] = translations
    out['translations_google'] = google_translations

    df = pd.DataFrame.from_dict(out)
    print(df)
    df.to_csv('out.csv')
