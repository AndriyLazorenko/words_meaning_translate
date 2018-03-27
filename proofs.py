from textblob import Word
word = Word("plant", pos_tag='v')
print(word.synsets[:5])
print(word.definitions[0])
