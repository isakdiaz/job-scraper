import requests
from bs4 import BeautifulSoup
import time
import numpy as np


url = "https://www.linkedin.com/jobs/search/?currentJobId=1365739043&keywords=visa%20sponsor"
page = requests.get(url)


soup = BeautifulSoup(page.content, 'html.parser')

# Run through the search URL and copy the links to all the jobs
numJobs = 0
job_links  = []
result_cards = soup.find_all('a', class_='result-card__full-card-link')
print("Job Links found:")
for item in result_cards:
    job_links.append(item.attrs['href'])
    numJobs += 1
    print(item.attrs['href'])

print("Finished scraping {} Links".format(numJobs))
np.save("assets/job_links.npy", job_links)
