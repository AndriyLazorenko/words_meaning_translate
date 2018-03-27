from textblob import Word
from textblob.wordnet import VERB
from nltk.corpus import wordnet as wn

word = Word("bribe", pos_tag='v')
v = word.get_synsets(pos=VERB)
print(word.synsets[:5])
print(word.definitions[0])
print(v[0].definition())