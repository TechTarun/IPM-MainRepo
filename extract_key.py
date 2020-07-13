import nltk
from nltk.stem import PorterStemmer
from nltk.stem import SnowballStemmer
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import krovetz

def extract(text):
    stop_words = stopwords.words('english')
    stop_words.extend(['mail', 'Mail', 'email', 'Email', 'subject', 'show', 'bring', 'fetch', 'tell', 'sender', 'get', 'many', 'find'])
    stop_words.remove('after')
    stop_words.remove('before')    
    # stop_words.remove('send')
    stop_words = set(stop_words)
    msg = text
    words = word_tokenize(msg.lower())
    stemmer = krovetz.PyKrovetzStemmer()
    filtered_words = set()

    for word in words:
        if word not in stop_words and word.isalnum():
            stemmed_word = stemmer.stem(word)
            filtered_words.add(stemmed_word)

    if('mail' in filtered_words):
        filtered_words.remove('mail')
    if('email' in filtered_words):
        filtered_words.remove('email')
    return list(filtered_words)

extract("I am tarun agarwal")