from nltk.tokenize import sent_tokenize
import numpy as np
import re
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from textblob import TextBlob

import nltk
nltk.download('vader_lexicon')

jobDescArr = np.load('indeedDesc.npy')

def clipSentence(sentence, totalChars):
    visaInd = sentence.find('visa')
    if(visaInd == -1):
        print("Visa String not found!")
        return "Visa string not found!"

    charsBefore = visaInd - int(totalChars/2)
    charsAfter = visaInd + int(totalChars/2)

    charsBefore = charsBefore if (charsBefore > 0) else 0
    charsAfter = charsAfter if (charsAfter < len(cleanDesc)) else len(cleanDesc)

    return cleanDesc[charsBefore:charsAfter]


pos = []
neg = []
count = 0
total = len(jobDescArr)
seen = 0
for jobDesc in jobDescArr:
    count += 1
    jobDescWithPeriods = jobDesc.replace("e.g.", "eg").replace("-", "").replace("\n", ". ") # Replace line breaks with periods
    sid = SentimentIntensityAnalyzer()
    for sentence in sent_tokenize(jobDescWithPeriods):
        
        cleanDesc = re.sub(r'\W+', ' ', sentence).lower()
        if("visa" in cleanDesc):
            if(len(cleanDesc) > 200):
                finalDesc = clipSentence(cleanDesc, 200)
            else:
                finalDesc = cleanDesc
            
            if(finalDesc in pos):
                print("[----------------Positive--------------] {}".format(seen))
                print(finalDesc)
                print("[----------------Positive--------------]")
                seen += 1
                continue
            elif(finalDesc in neg):
                print("[----------------Negative--------------] {}".format(seen))
                print(finalDesc)
                print("[----------------Negative--------------]")
                seen += 1
                continue
            else:
                print("++++++++++++++++++++++++++++")
                print(finalDesc)
                print("++++++++++++++++++++++++++++")

            result = input("{}/{}: Type [Enter] for Negative and [SPACE][ENTER] for Positive: ".format(count, total))
            if(result == 'y' or result == ' '):
                pos.append(finalDesc)
            elif(result == '' or result == 'n'):
                neg.append(finalDesc)
            else:
                print("Wrong return type, skipping!")
                continue
                      
            print("\n")

print("Pos Hits: ")
print(pos)
print("neg Hits: ")
print(neg)
np.save("pos_desc.npy", pos)
np.save("neg_desc.npy", neg)