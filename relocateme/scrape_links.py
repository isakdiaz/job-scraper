import requests
from bs4 import BeautifulSoup
import time
import numpy as np

# First run this file with the LinkedIN job search url. Make sure to be signed out or the page that the requests packages accesses will be different

url = "https://relocateme.eu/jobs/"
page = requests.get(url)


soup = BeautifulSoup(page.content, 'html.parser')

# Run through the search URL and copy the links to all the jobs
numJobs = 0
job_links  = []
result_cards = soup.find_all('h4', class_='job_title')
print("Job Links found:")
for item in result_cards:
    job_links.append(item.find('a').attrs['href'])
    numJobs += 1
    print(item.find('a').attrs['href'])

print("Finished scraping {} Links".format(numJobs))
np.save("job_links.npy", job_links)
