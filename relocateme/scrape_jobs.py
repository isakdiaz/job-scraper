import requests
from bs4 import BeautifulSoup
import time
import numpy as np
import json
import hashlib
import sys
# insert at 1, 0 is the script path (or '' in REPL)
sys.path.insert(1, '../')
from utils import convertPositionToCategory, formatTags, formatCountry

# First run scrape_links.py to save the job description links that have been scraped from the website.
# All job listings from the same company will have the two digit source number preceding the ID.
SOURCE_WEBSITE = "relocateme"
SOURCE_NUMBER = 12
ID_SIG_FIGS = 6
LINK_LOCATION = "job_links.npy"
OUT_FILE = SOURCE_WEBSITE + "_data.json"
job_links = np.load(LINK_LOCATION)


print("Processing {} links from {}".format(len(job_links), LINK_LOCATION))

# Use individual job links to scrape data

# job_links = ["https://relocateme.eu/jobs/country-de/tech-python/senior-python-engineer-munich-germany-55022/"]
numJobs = 0
jobsJSON = {}
jobsJSON['listings'] = []

for url in job_links:
    # print(url)
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')

    #First Calculate Position & Company
    position = soup.find('h2', class_='position_title').get_text()
    company = "RelocateMe"



    location = soup.find('p', class_='position_country').get_text()
    city = location.split(",")[0]
    country = location.split(",")[1].strip()
    country = [formatCountry(country)]     # Country is actually countries list, so include single country in the list so that front end processes it correctly
    tags = [tag.get_text() for tag in soup.find_all('a', class_='btn-tag')]
    tags =  formatTags(tags)

    description = soup.find('div', class_='position_description')

    visa = True if ("Visa Sponsorship if necessary" in description.get_text()) else False
    remote = False

    # Calculate Job ID using URL
    hash_multipler = 10 ** ID_SIG_FIGS
    print(position + location)
    jobHash = int(hashlib.md5((position+company+city).encode("utf-8")).hexdigest(), 16)
    databaseId = (jobHash % hash_multipler + SOURCE_NUMBER * hash_multipler)

    # No time stamp found on website. Using current time as best guess
    # Database will have to be set not to update results or else new updates will float to top
    # with new time stamps
    epoch = round(time.time() - 60*60*24)

    numJobs += 1
    
    category =  convertPositionToCategory(position)        

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
        "language": ["Unknown"],    # TODO need to source this data
        "tags": tags,
        "category": category,
        "epoch": epoch,
        "url": url,
        "imgUrl": "relocateme",
        "visa" : visa,
        "remote" : remote,
        "description": str(description)
    })


    # print(url)
    print('Job ID', databaseId)
    
with open(OUT_FILE, 'w') as outfile:
    json.dump(jobsJSON, outfile)

print("Completed processing {} jobs from {}!".format(numJobs, SOURCE_WEBSITE))

