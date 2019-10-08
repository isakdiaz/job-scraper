import numpy as np
from nltk.corpus import stopwords
import nltk
from nltk.tokenize import sent_tokenize
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.svm import LinearSVC
import pickle
from classify_desc import preprocess_desc
import os
# nltk.download('stopwords')
# nltk.download('wordnet')



def train_classifer():
    # print("Training Classifier...")

    # Load positive & negative samples for keyword
    dirname = os.path.dirname(__file__)
    posFilename = os.path.join(dirname, 'assets/pos_desc.npy')
    negFilename = os.path.join(dirname, 'assets/neg_desc.npy')
    pos =  np.load(posFilename)
    neg =  np.load(negFilename)


    # Y Values for training & Testing
    y_train = [1 if i < len(pos) else 0 for i in range(len(pos) + len(neg))]
    X_train =  np.concatenate((pos,neg))

    # Comment out when using all data for testing
    # X_train, X_val, y_train, y_val = train_test_split(
    #     X_train, y_train, train_size = 0.9
    # )

    stop_words = ['in', 'of', 'at', 'a', 'the']
    ngram_vectorizer = CountVectorizer(binary=True, ngram_range=(1, 3), stop_words=stop_words)
    ngram_vectorizer.fit(X_train)
    X_train = ngram_vectorizer.transform(X_train)

    # Comment out when using all data for testing
    # X_test = ngram_vectorizer.transform(X_val)
    # for c in [0.001, 0.005, 0.01, 0.05, 0.1]:
    #     svm = LinearSVC(C=c)
    #     svm.fit(X_train, y_train)
    #     print ("Accuracy for C=%s: %s" 
    #         % (c, accuracy_score(y_val, svm.predict(X_test))))
            
    final = LinearSVC(C=0.1)
    final.fit(X_train, y_train)


    return(final, ngram_vectorizer)


def classify_array(textArr):
    cleanJobDescs = []
    for jobDesc in textArr:
        tempDesc = preprocess_desc(jobDesc)
        if(tempDesc): cleanJobDescs.append(tempDesc)
    
    if(len(cleanJobDescs) < 1): return [0] #Visa not found in job description

    final, ngram_vectorizer = train_classifer()
    X_test = ngram_vectorizer.transform(cleanJobDescs)

    return final.predict(X_test)


if __name__ == '__main__':
    textArr = [ "cant sponsor visas at this time", "benefits can sponsor your visa", 'will sponsor green card h1b visa card ', 'willing to sponsor eligible candidates for employment visas ', 'unfortunately we cannot sponsor any employment visas now or in the future for this position ',
           'we cannot currently sponsor new work visas but we can transfer existing h1bs ', 'we sponsor work visas for right candidate', 'will sponsor h1b visa and green card ']

    print(classify_array(textArr))