import requests
from bs4 import BeautifulSoup
import time
import numpy as np
import json 
import hashlib
import sys
import random
import re
# insert at 1, 0 is the script path (or '' in REPL)
sys.path.insert(1, '../')
from sa_classifier import classify_array
from utils import convertPositionToCategory, convertDescToTags, formatTags, formatCountry, formatCountryFromUrl, calculateEpoch

# First run scrape_links.py to save the job description links that have been scraped from the website.
# All job listings from the same company will have the two digit source number preceding the ID.

SLEEP_PER_REQUEST = 3
SOURCE_WEBSITE = "indeed"
SOURCE_NUMBER = 13
ID_SIG_FIGS = 6
LINK_LOCATION = "job_links.npy"
OUT_FILE = SOURCE_WEBSITE + "_data.json"
job_links = np.load(LINK_LOCATION)
random.shuffle(job_links) # Shuffle randomly links to prevent same server from timing out



print("Processing {} links from {}".format(len(job_links), LINK_LOCATION))

# Use individual job links to scrape data

# url = "https://www.indeed.com/viewjob?jk=1e13a99883628de9&from=serp&vjs=3"
numJobs = 0
badCompany = 0
badPosition = 0
jobsJSON = {}
jobsJSON['listings'] = []
descArr = []
totalJobs = len(job_links)
count = 0
visaCount = 0
remote = False

for url in job_links:
    count += 1

    try:
        page = requests.get(url, timeout=SLEEP_PER_REQUEST)
        time.sleep(SLEEP_PER_REQUEST) # Reduce likelihood of timeot Error
        print("requesting page")
    except requests.exceptions.Timeout:
        print("Timeout occurred")
        continue
    except:
        print("Other Exception Occured!")
        continue

    soup = BeautifulSoup(page.content, 'html.parser')

    try:
        position = soup.find("h3", class_="jobsearch-JobInfoHeader-title").get_text()        # print(position)
    except:
        print("Bad Position Name, skipping: {}".format(url))
        badPosition += 1
        continue

    try:
        company = soup.find_all("div", class_="icl-u-lg-mr--sm icl-u-xs-mr--xs")[0].get_text()
        # print(position)  
    except:
        print("Bad Company Name, skipping: {}".format(url))
        badCompany += 1
        continue

    # Find Description
    description = soup.find_all("div", class_="jobsearch-jobDescriptionText")[0]
    descriptionText = description.get_text()

    # Determine if this job sponsor visas using sentiment analysis
    visa_job = classify_array([descriptionText])[0] # 1 indicates job 
    # print(visa_job)
    if not visa_job:
        print("Not a visa job")
        continue
    else:
        visaCount += 1


    locationString = soup.find_all("div", class_="jobsearch-InlineCompanyRating")[0].get_text().split("-")[-1]
    location =  locationString.split(",")


    # Calculate Time Posted   
    timeText = soup.find("div", class_="jobsearch-JobMetadataFooter").get_text().split(" - ")[1].lower()
    epoch = calculateEpoch(timeText)
    # timeText = re.sub('\W+',' ', timeText ) # Remove Special characters (ussually + e.g "30+ Days")


    # Calculate Location
    numLocations = len(location)
    if(locationString == 'Remote'):
        city = ""
        country = "Remote"
        remote = True
    elif(numLocations == 0):
        city = ""
        country = "United States"
    elif(numLocations == 1):
        city = location[0].strip()
        country = location[0].strip()
    elif(numLocations == 2):
        city = location[0]
        country = location[1].strip()
    else:
        city = location[0] + " " + location[1]
        country = location[-1].strip()
    
    # Functions
    print(country)
    country = [formatCountryFromUrl(url, formatCountry(country))]     # Country is actually countries list, so include single country in the list so that front end processes it correctly
    city = "" if city == country[0] else city
    print(country)
    
    category = convertPositionToCategory(position)
    tags = convertDescToTags(descriptionText)
    tags.append(SOURCE_WEBSITE)


    numJobs += 1
    
    hash_multipler = 10 ** ID_SIG_FIGS
    jobHash = int(hashlib.md5((position+company+city).encode("utf-8")).hexdigest(), 16)
    databaseId = (jobHash % hash_multipler + SOURCE_NUMBER * hash_multipler)

    # SAVE RESULTS
    descArr.append(descriptionText)
    
    jobsJSON['listings'].append({
        "id": databaseId,
        "source": SOURCE_WEBSITE,
        "position": position,
        "company": company,
        "city": city,
        "country": country,
        "maxSalary": "0",   # TODO need to source this data
        "minSalary": "0",    # TODO need to source this data
        "currency": "USD",  # TODO need to source this data
        "language": ["English"],    # TODO need to source this data
        "tags": tags,
        "category": category,
        "epoch": epoch,
        "url": url,
        "imgUrl": SOURCE_WEBSITE,
        "visa": True,
        "remote": remote,
        "description": str(description)
    })

    # PRINT STATEMENTS
    print(url, "VisaJobs: ", visaCount, " Total: ", count, "/", totalJobs)
    # print("city: ", city, " country: ", country)

    
    
    with open(OUT_FILE, 'w') as outfile:
        json.dump(jobsJSON, outfile)

    np.save('indeedDesc.npy', descArr)

print("Completed processing {} jobs from {}!".format(numJobs, SOURCE_WEBSITE))
print("Bad Position {}, Bad company {} Errors".format(badPosition, badCompany))
