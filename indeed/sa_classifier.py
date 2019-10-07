import numpy as np
from nltk.corpus import stopwords
import nltk
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.svm import LinearSVC
import pickle

# nltk.download('stopwords')
# nltk.download('wordnet')
def train_classifer():
    print("WOW")
    pos =  np.load('pos_desc.npy')
    neg =  np.load('neg_desc.npy')


    # Y Values for training & Testing
    target = [1 if i < len(pos) else 0 for i in range(len(pos) + len(neg))]
    X =  np.concatenate((pos,neg))


    X_train, X_val, y_train, y_val = train_test_split(
        X, target, train_size = 0.9
    )

    stop_words = ['in', 'of', 'at', 'a', 'the']
    ngram_vectorizer = CountVectorizer(binary=True, ngram_range=(1, 3), stop_words=stop_words)
    ngram_vectorizer.fit(X_train)
    X = ngram_vectorizer.transform(X_train)
    X_test = ngram_vectorizer.transform(X_val)

    for c in [0.001, 0.005, 0.01, 0.05, 0.1]:
        svm = LinearSVC(C=c)
        svm.fit(X, y_train)
        print ("Accuracy for C=%s: %s" 
            % (c, accuracy_score(y_val, svm.predict(X_test))))
            
    final = LinearSVC(C=0.1)
    final.fit(X, y_train)

    return(final, ngram_vectorizer)


def classify_array(textArr):
    final, ngram_vectorizer = train_classifer()
    X_test = ngram_vectorizer.transform(textArr)
    return final.predict(X_test)

textArr = [ "cant sponsor visas at this time", "benefits can sponsor your visa", 'will sponsor green card h1b visa card ', 'willing to sponsor eligible candidates for employment visas ', 'unfortunately we cannot sponsor any employment visas now or in the future for this position ',
       'we cannot currently sponsor new work visas but we can transfer existing h1bs ', 'we sponsor work visas for right candidate', 'will sponsor h1b visa and green card ']

print(classify_array(textArr))