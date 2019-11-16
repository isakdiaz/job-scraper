import requests
from bs4 import BeautifulSoup
import time
import numpy as np

# First run this file with the LinkedIN job search url. Make sure to be signed out or the page that the requests packages accesses will be different


keywords = ['visa']
tags = ['developer', 'data science']
locations = ['Canada', 'Chile', 'Germany', 'Japan', 'Netherlands', 'Spain', 'Thailand', 'United Kingdom', 'United States']

# Add URL friendly spaces
tags = [tag.replace(" ","%20") for tag in tags]
keywords = [keyword.replace(" ","%20") for keyword in keywords]
locations = [location.replace(" ","%20") for location in locations]
f_TP = [1,2,3] # Page thats starts with most recent to least recent
f_TP = [1] # Page thats starts with most recent to least recent

urls = []
for key in keywords:
    for tag in tags:
        for location in locations:
            for num in f_TP:
                tempUrl = "https://www.linkedin.com/jobs/search?keywords={}%20{}&location={}&redirect=true&f_TP={}".format(key,tag,location,num)
                urls.append(tempUrl)


numJobs = 0
job_links  = []
for url in urls:
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')

    # Run through the search URL and copy the links to all the jobs
    result_cards = soup.find_all('a', class_='result-card__full-card-link')
    print("Job Links found:")
    for item in result_cards:
        job_links.append(item.attrs['href'])
        numJobs += 1
        print(item.attrs['href'])

    print("Finished scraping {} Links".format(numJobs))

np.save("job_links.npy", job_links)