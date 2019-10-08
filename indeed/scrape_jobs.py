import requests
from bs4 import BeautifulSoup
import time
import numpy as np
import json 
import hashlib
import sys
import re
import asyncio


# insert at 1, 0 is the script path (or '' in REPL)
sys.path.insert(1, '../')
from sa_classifier import classify_array
from utils import convertPositionToCategory, convertDescToTags, formatTags, formatCountry

# First run scrape_links.py to save the job description links that have been scraped from the website.
# All job listings from the same company will have the two digit source number preceding the ID.

SLEEP_PER_REQUEST = 0
SOURCE_WEBSITE = "indeed"
SOURCE_NUMBER = 13
ID_SIG_FIGS = 6
LINK_LOCATION = "job_links.npy"
OUT_FILE = SOURCE_WEBSITE + "_data.json"
job_links = np.load(LINK_LOCATION)



print("Processing {} links from {}".format(len(job_links), LINK_LOCATION))

# Use individual job links to scrape data

# url = "https://www.indeed.com/viewjob?jk=1e13a99883628de9&from=serp&vjs=3"
numJobs = 0
companyErrors = 0
jobsJSON = {}
jobsJSON['listings'] = []
descArr = []
totalJobs = len(job_links)

# job_links = job_links[:1]
count = 0
visaCount = 0
for url in job_links[460:]:
    count += 1

    try:
        page = requests.get(url, timeout=1)
    except requests.exceptions.Timeout:
        print("Timeout occurred")

    soup = BeautifulSoup(page.content, 'html.parser')
    # Reduce number of requests by sleeping
    time.sleep(SLEEP_PER_REQUEST) 


    # Error with not finding company name
    try:
        position = soup.find("h3", class_="jobsearch-JobInfoHeader-title").get_text()
        company = soup.find_all("div", class_="icl-u-lg-mr--sm icl-u-xs-mr--xs")[0].get_text()
        print(position)
    except:
        print("Bad Company Name, skipping: {}".format(url))
        companyErrors += 1
        continue


    # Determine if this job sponsor visas using sentiment analysis
    description = soup.find_all("div", class_="jobsearch-jobDescriptionText")[0]
    visa_job = classify_array([description.get_text()])[0] # 1 indicates job 
    # print(visa_job)
    if not visa_job:
        # print("Not a visa job")
        continue

    print(url, "VisaJobs: ", visaCount, " Total: ", count, "/", totalJobs)

    visaCount += 1
    locationString = soup.find_all("div", class_="jobsearch-InlineCompanyRating")[0].get_text().split("-")[-1]
    location =  locationString.split(",")


    #Save Desc Array
    descArr.append(description.get_text())

    # Calculate Time Posted   
    timeText = soup.find("div", class_="jobsearch-JobMetadataFooter").get_text().split(" - ")[1].lower()
    timeText = re.sub('\W+',' ', timeText ) # Remove Special characters (ussually + e.g "30+ Days")
    timeArr = timeText.split(" ")

    timeInt = [int(i) for i in timeText.split(" ") if i.isdigit()]
    timeInt = 1 if(len(timeInt) == 0) else timeInt[0]

    


    if("today" in timeText):
        timeMultiplier = 60 * 60 * 24
        timeMultiplierText = "today"
    elif("hour" in timeText):
        timeMultiplier = 60 * 60
        timeMultiplierText = "hour"
    elif("day" in timeText):
        timeMultiplier = 60 * 60 * 24 
        timeMultiplierText = "day"
    elif("week" in timeText):
        timeMultiplier = 60 * 60 * 24 * 7
        timeMultiplierText = "week"
    elif("month" in timeText):
        timeMultiplier = 60 * 60 * 24 * 7 * 30
        timeMultiplierText = "month"
    else:
        timeMultiplier = 0
        timeMultiplierText = "Not Available"
        print("No Time multiplier", timeText)

    # print(timeMultiplierText)
    
    epoch = round(time.time()) - timeMultiplier * timeInt

    # print(timeText)
    # print("time int : ", timeInt, "time X", timeMultiplierText)
    # print(epoch)

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
    country = [formatCountry(country)]     # Country is actually countries list, so include single country in the list so that front end processes it correctly
    city = "" if city == country[0] else city
    category = convertPositionToCategory(position)
    tags = convertDescToTags(description.get_text())
    tags.append(SOURCE_WEBSITE)
    # print("city: ", city, " country: ", country)

    numJobs += 1
    
    hash_multipler = 10 ** ID_SIG_FIGS
    jobHash = int(hashlib.md5((position+company+city).encode("utf-8")).hexdigest(), 16)
    databaseId = (jobHash % hash_multipler + SOURCE_NUMBER * hash_multipler)

    
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
        "description": str(description)
    })



    
with open(OUT_FILE, 'w') as outfile:
    json.dump(jobsJSON, outfile)

np.save('indeedDesc.npy', descArr)

print("Completed processing {} jobs from {}! With {} Errors".format(numJobs, SOURCE_WEBSITE, companyErrors))

