import requests
from bs4 import BeautifulSoup
import time
import numpy as np


url = "https://www.linkedin.com/jobs/search/?currentJobId=1365739043&keywords=visa%20sponsor"
page = requests.get(url)



soup = BeautifulSoup(page.content, 'html.parser')

# [type(item) for item in list(soup.children)] // Find where TAG is
# html = list(soup.children)[1]


# <a class="result-card__full-card-link" href="https://www.linkedin.com/jobs/view/private-equity-analyst-triartisan-capital-advisors-at-cowen-at-onewire-1486220009?refId=6852c52c-e16e-4c6d-ad9e-25698a4db4aa&amp;position=1&amp;pageNum=0&amp;trk=guest_job_search_job-result-card_result-card_full-click" data-tracking-control-name="guest_job_search_job-result-card_result-card_full-click" data-tracking-will-navigate=""><span class="screen-reader-text">Private Equity Analyst, TriArtisan Capital Advisors at Cowen</span></a>

# Run through the search URL and copy the links to all the jobs
job_links  = []
result_cards = soup.find_all('a', class_='result-card__full-card-link')
print("Job Links found:")
for item in result_cards:
    job_links.append(item.attrs['href'])
    print(item.attrs['href'])


# Use individual job links to scrape data

# url = "https://www.linkedin.com/jobs/view/sponsorship-coordinator-at-live-nation-entertainment-1489576317?refId=bbeb146e-4308-4316-a9b8-31fb9e75d35c&position=1&pageNum=0&trk=guest_job_search_job-result-card_result-card_full-click"
url = "https://www.linkedin.com/jobs/view/software-engineer-web-developer-javascript-java-at-sprinklr-1484916244?refId=e6bd7943-e205-4d7e-bdec-f83b19dbf3c1&trk=guest_job_details_topcard_title"
page = requests.get(url)

soup = BeautifulSoup(page.content, 'html.parser')

position = soup.find_all("h1", class_='topcard__title')[0].get_text()
company = soup.find_all("a", class_='topcard__org-name-link')[0].get_text()
location = soup.find_all("span", class_='topcard__flavor topcard__flavor--bullet')[0].get_text()
city = location.split(",")[0].strip()
country = location.split(",")[1].strip()
# country = location.split(",")[2].strip() 
description =  soup.find_all("div", class_='description__text')[0]
criteria =  soup.find_all("span", class_='job-criteria__text job-criteria__text--criteria')
tags = [tag.get_text() for tag in criteria]
# category =  soup.find_all("li", class_='job-criteria__item')[2].get_text()
category = tags[2]
url = url
# Calculate Epoch time Stamp
timeText = soup.find_all("span", "posted-time-ago__text")[0].get_text()
timeInt = [int(i) for i in timeText.split(" ") if i.isdigit()][0]
timeString = [i for i in timeText.split(" ") if i]

if("hours" in timeString):
    timeMultiplier = 60 * 60
elif("days" in timeString):
    timeMultiplier = 60 * 60 * 24 
elif("weeks" in timeString):
    timeMultiplier = 60 * 60 * 24 * 7
elif("months" in timeString):
    timeMultiplier = 60 * 60 * 24 * 7 * 30
else:
    ValueError("Could not parse time format from String!")

epoch = round(time.time()) - (timeInt * timeMultiplier)

print(position)
