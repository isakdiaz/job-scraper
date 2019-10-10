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

SLEEP_PER_REQUEST = 2
SOURCE_WEBSITE = "linkedin"
SOURCE_NUMBER = 11
ID_SIG_FIGS = 6
LINK_LOCATION = "job_links.npy"
OUT_FILE = SOURCE_WEBSITE + "_data.json"
job_links = np.load(LINK_LOCATION)
random.shuffle(job_links) # Shuffle randomly links to prevent same server from timing out



print("Processing {} links from {}".format(len(job_links), LINK_LOCATION))

numJobs = 0
companyErrors = 0
jobsJSON = {}
jobsJSON['listings'] = []
descArr = []
totalJobs = len(job_links)

count = 0
visaCount = 0
badLocation = 0
badPosition = 0
badCompany = 0
badTime = 0
for url in job_links[:30]:
    count += 1

    try:
        page = requests.get(url, timeout=3)
        time.sleep(SLEEP_PER_REQUEST) 
    except requests.exceptions.Timeout:
        print("Timeout occurred")
        continue
    except:
        print("Other Exception Occured!")
        continue

    soup = BeautifulSoup(page.content, 'html.parser')


    try:
        position = soup.find_all("h1", class_='topcard__title')[0].get_text()
    except:
        print("Bad Company/Position/Location Skipping")
        badPosition += 1
        continue
                
    try:
        company = soup.find_all("span", class_='topcard__flavor')[0].get_text()
    except:
        print("Bad Company")
        badCompany += 1
        continue
    try:
        locationString = soup.find("span", class_="topcard__flavor topcard__flavor--bullet").get_text()
        # locationString = soup.find_all("div", class_="jobsearch-InlineCompanyRating")[0].get_text().split("-")[-1]  
    except:
        print("Bad Location Skipping")
        badLocation +=1
        continue

    # Determine if this job sponsor visas using sentiment analysis
    description =  soup.find_all("div", class_='description__text')[0]
    descriptionText = description.get_text()
    visa_job = classify_array([descriptionText])[0] # 1 indicates job 
    # print(visa_job)
    if not visa_job:
        # print("Not a visa job")
        continue

    print(url)
    print("VisaJobs: ", visaCount, " Total: ", count, "/", totalJobs)

    visaCount += 1
    location =  locationString.split(",")

    #Save Desc Array
    descArr.append(descriptionText)

    # Calculate Location
    location = soup.find_all("span", class_='topcard__flavor topcard__flavor--bullet')[0].get_text().split(",")
    numLocations = len(location)

    if(numLocations == 0):
        city = ""
        country = "United States"
    elif(numLocations == 1):
        city = ""
        country = location[0].strip()
    elif(numLocations == 2):
        city = location[0]
        country = location[1].strip()
    else:
        city = location[0] + "," + location[1]
        country = location[-1].strip()

    country = formatCountryFromUrl(url, country)     # Country is actually countries list, so include single country in the list so that front end processes it correctly
    country = [formatCountry(country)] # Change abbrvs to full names
    
    # Special case for Agoda who likes to SPAM bangkok listings
    if("bangkok" in position.lower() or 'bangkok' in descriptionText.lower()): 
        city = "Bangkok"
        country = ["Thailand"]

    tags = convertDescToTags(descriptionText)
    print(tags)
    # criteria =  soup.find_all("span", class_='job-criteria__text job-criteria__text--criteria')
    # tags = [tag.get_text() for tag in criteria if tag.get_text() != "Not Applicable"]
    # tags =  formatTags(tags)
    # category =  soup.find_all("li", class_='job-criteria__item')[2].get_text()
    category = convertPositionToCategory(position)
    url = url
    # Calculate Epoch time Stamp
    timeText = soup.find_all("span", "posted-time-ago__text")[0].get_text()

    epoch = calculateEpoch(timeText.lower())
    numJobs += 1
    
    hash_multipler = 10 ** ID_SIG_FIGS
    jobHash = int(hashlib.md5((position+company+city).encode("utf-8")).hexdigest(), 16)
    databaseId = (jobHash % hash_multipler + SOURCE_NUMBER * hash_multipler)


    
    jobsJSON['listings'].append({
        "id": databaseId,
        "source": "linkedin",
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
        "imgUrl": "linkedin",
        "description": str(description)
    })


    print(position)
    print("location: ", location)
    print("city: ", city)
    print("country: ", country[0])
    # print('Job ID', databaseId)
    
with open(OUT_FILE, 'w') as outfile:
    json.dump(jobsJSON, outfile)

np.save('linkedinDesc.npy', descArr)

print("Completed processing {} jobs from {}!".format(numJobs, SOURCE_WEBSITE))
print("Bad Position {}, Bad Company {}, Bad Location {}, Bad Time {}".format(badPosition, badCompany, badLocation, badTime))
