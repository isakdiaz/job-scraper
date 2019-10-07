import numpy as np
import re

jobDescArr = np.load('indeedDesc.npy')

for jobDesc in jobDescArr:
    cleanDesc = re.sub(r'\W+', ' ', jobDesc)
    visaInd = cleanDesc.find('visa')
    if(visaInd == -1):
        print("Visa String not found!")
        continue

    totalChars = 200
    charsBefore = visaInd - int(totalChars/2)
    charsAfter = visaInd + int(totalChars/2)

    charsBefore = charsBefore if (charsBefore > 0) else 0
    charsAfter = charsAfter if (charsAfter < len(cleanDesc)) else len(cleanDesc)
    print(charsBefore, charsAfter)
    print(cleanDesc[charsBefore:charsAfter])

