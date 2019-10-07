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

pos =  np.load('pos_desc.npy')
neg =  np.load('neg_desc.npy')


# Y Values for training & Testing
target = [1 if i < len(pos) else 0 for i in range(len(pos) + len(neg))]
X =  np.concatenate((pos,neg))


X_train, X_val, y_train, y_val = train_test_split(
    X, target, train_size = 0.80
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
    
final = LinearSVC(C=0.01)
final.fit(X, y_train)


# save the model to disk
# import time
filename = 'sa_model.sav'
pickle.dump(final, open(filename, 'wb'))
 

# # TOP WORDS
# feature_to_coef = {
#     word: coef for word, coef in zip(
#         ngram_vectorizer.get_feature_names(), final.coef_[0]
#     )
# }

# for best_positive in sorted(
#     feature_to_coef.items(), 
#     key=lambda x: x[1], 
#     reverse=True)[:30]:
#     print (best_positive)
    
# print("\n\n")
# for best_negative in sorted(
#     feature_to_coef.items(), 
#     key=lambda x: x[1])[:30]:
#     print (best_negative)