import requests
from bs4 import BeautifulSoup
import time
import numpy as np
import json 
import hashlib
import sys
# insert at 1, 0 is the script path (or '' in REPL)
sys.path.insert(1, '../')
from utils import convertPositionToCategory, convertDescToTags, formatTags, formatCountry

# First run scrape_links.py to save the job description links that have been scraped from the website.
# All job listings from the same company will have the two digit source number preceding the ID.

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
jobsJSON = {}
jobsJSON['listings'] = []


# job_links = job_links[:1]

for url in job_links:
    print(url)
    page = requests.get(url)

    soup = BeautifulSoup(page.content, 'html.parser')

    position = soup.find("h3", class_="jobsearch-JobInfoHeader-title").get_text()
    company = soup.find_all("div", class_="icl-u-lg-mr--sm icl-u-xs-mr--xs")[0].get_text()
    locationString = soup.find_all("div", class_="jobsearch-InlineCompanyRating")[0].get_text().split("-")[-1]
    location =  locationString.split(",")
    description = locationString = soup.find_all("div", class_="jobsearch-jobDescriptionText")[0]

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
    print(tags)

    epoch = round(time.time())
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

print("Completed processing {} jobs from {}!".format(numJobs, SOURCE_WEBSITE))

