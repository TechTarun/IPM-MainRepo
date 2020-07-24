import nltk
from nltk.stem import PorterStemmer
from nltk.stem import SnowballStemmer
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

# ps = SnowballStemmer("english")
ps = PorterStemmer()

def extract(text):
    stop_words = stopwords.words('english')
    stop_words = set(stop_words)
    msg = text
    words = word_tokenize(msg.lower())
    filtered_words = set()

    for word in words:
        if word not in stop_words and word.isalnum():
            stemmed_word = ps.stem(word)
            filtered_words.add(stemmed_word)
    return list(filtered_words)
