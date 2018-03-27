from textblob import Word
import pandas as pd
# from translate import Translator
# translator = Translator(to_lang="uk")

from mtranslate import translate

df = pd.read_csv("in.csv", header=None)
demo = df[1].dropna()


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


words = demo
meanings = get_meanings(demo)
translations = get_translations(demo)

out = dict()
out['words'] = words
out['meanings'] = meanings
out['translations'] = translations

df = pd.DataFrame.from_dict(out)
print(df)
df.to_csv('out.csv')
