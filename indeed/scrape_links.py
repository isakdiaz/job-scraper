import requests
from bs4 import BeautifulSoup
import time
import numpy as np

# First run this file with the LinkedIN job search url. Make sure to be signed out or the page that the requests packages accesses will be different

# url = "https://www.indeed.com/q-visa-sponsor-jobs.html"
baseUrl = "https://www.indeed.com/jobs?q=visa+sponsor+developer&start="
numJobs = 0
job_links  = []

# Website displays 10 jobs per page
for pageNum in range(0,500,10):
    url = baseUrl + str(pageNum)

    #Request Page
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')

    # Run through the search URL and copy the links to all the jobs
    result_cards = soup.find_all('a', class_='jobtitle turnstileLink')
    print("Processed {} job links".format(pageNum))
    for item in result_cards:
        if ("rc/clk" in item.attrs['href']):
            full_link = "https://www.indeed.com" + item.attrs['href']
            job_links.append(full_link)
            numJobs += 1
            print(full_link)

print("Finished scraping {} Links".format(numJobs))
np.save("job_links.npy", job_links)
