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

SOURCE_WEBSITE = "linkedin"
SOURCE_NUMBER = 11
ID_SIG_FIGS = 6
LINK_LOCATION = "job_links.npy"
OUT_FILE = SOURCE_WEBSITE + "_data.json"
job_links = np.load(LINK_LOCATION)



print("Processing {} links from {}".format(len(job_links), LINK_LOCATION))

# Use individual job links to scrape data

# url = "https://www.linkedin.com/jobs/view/sponsorship-coordinator-at-live-nation-entertainment-1489576317?refId=bbeb146e-4308-4316-a9b8-31fb9e75d35c&position=1&pageNum=0&trk=guest_job_search_job-result-card_result-card_full-click"
# url = "https://www.linkedin.com/jobs/view/software-engineer-web-developer-javascript-java-at-sprinklr-1484916244?refId=e6bd7943-e205-4d7e-bdec-f83b19dbf3c1&trk=guest_job_details_topcard_title"
numJobs = 0
jobsJSON = {}
jobsJSON['listings'] = []


job_links = job_links[:5]

for url in job_links:
    # print(url)
    page = requests.get(url)

    soup = BeautifulSoup(page.content, 'html.parser')

    position = soup.find_all("h1", class_='topcard__title')[0].get_text()
    # company = soup.find_all("a", class_='topcard__org-name-link')[0].get_text()
    company = soup.find_all("span", class_='topcard__flavor')[0].get_text()

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
        city = location[0] + " " + location[1]
        country = location[-1].strip()

    country = [formatCountry(country)]     # Country is actually countries list, so include single country in the list so that front end processes it correctly

    # country = location.split(",")[2].strip() 
    description =  soup.find_all("div", class_='description__text')[0]
    criteria =  soup.find_all("span", class_='job-criteria__text job-criteria__text--criteria')
    tags = [tag.get_text() for tag in criteria if tag.get_text() != "Not Applicable"]
    tags =  formatTags(tags)
    # category =  soup.find_all("li", class_='job-criteria__item')[2].get_text()
    category = [tag.get_text() for tag in criteria][2]
    url = url
    # Calculate Epoch time Stamp
    timeText = soup.find_all("span", "posted-time-ago__text")[0].get_text()
    timeInt = [int(i) for i in timeText.split(" ") if i.isdigit()][0]


    if("hour" in timeText):
        timeMultiplier = 60 * 60
    elif("day" in timeText):
        timeMultiplier = 60 * 60 * 24 
    elif("week" in timeText):
        timeMultiplier = 60 * 60 * 24 * 7
    elif("month" in timeText):
        timeMultiplier = 60 * 60 * 24 * 7 * 30
    else:
        ValueError("Could not parse time format from String!")


    # print("time text", timeText)
    # print(timeMultiplier)
    epoch = round(time.time()) - (timeInt * timeMultiplier)
    numJobs += 1

    # print(description)
    # print(tags)
    # print(position)
    # print("city ", city)
    # print("country", country)
    
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
    print(position, company, city)
    print('Job ID', databaseId)
    
with open(OUT_FILE, 'w') as outfile:
    json.dump(jobsJSON, outfile)

print("Completed processing {} jobs from {}!".format(numJobs, SOURCE_WEBSITE))

