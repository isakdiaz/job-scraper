import requests
from bs4 import BeautifulSoup
import time
import numpy as np

# First run this file with the LinkedIN job search url. Make sure to be signed out or the page that the requests packages accesses will be different

url = "https://www.indeed.com/q-visa-sponsor-jobs.html"
usaUrl = "https://www.indeed.com/jobs?q=visa+sponsor+developer&start="
auUrl = 'https://au.indeed.com/jobs?q=Visa+Sponsor+Developer&start='
nzUrl = 'https://nz.indeed.com/jobs?q=Visa+Sponsor+Developer&start='
nzUrl = 'https://nz.indeed.com/jobs?q=Visa+Sponsor+Developer&start='
nzUrl = 'https://nz.indeed.com/jobs?q=Visa+Sponsor+Developer&start='

countriesAbbr = ['www','ca','au','nz','ar']
countries = ['United States', 'Canada', 'Australia', 'New Zealand', 'Argentina']
numJobs = 0
job_links  = []
baseUrl = '.indeed.com'

# Website displays 10 jobs per page
for countryStr in countriesAbbr:
    prev_Links = []
    curr_Links = []
    for pageNum in range(0,500,10):
        prev_links = curr_Links
        url = "https://" + countryStr + baseUrl
        searchPageUrl =  url +"/jobs?q=visa+sponsor+developer&start=" + str(pageNum)

        #Request Page
        page = requests.get(searchPageUrl)
        soup = BeautifulSoup(page.content, 'html.parser')

        # Run through the search URL and copy the links to all the jobs
        result_cards = soup.find_all('a', class_='jobtitle turnstileLink')
        # Continue once at end of page
        if len(result_cards) == 0:
            break
        print("Country: {} Page Number: {}".format(countryStr, pageNum))
        print("Processed {} job links".format(numJobs))
        for item in result_cards:
            if ("rc/clk" in item.attrs['href']):
                full_link = url + item.attrs['href']
                job_links.append(full_link)
                curr_Links.append(full_link)
                numJobs += 1
                print(full_link)
        
        if curr_Links == prev_links:
            print("No more new links for country: ", countryStr)
            break

print("Finished scraping {} Links".format(numJobs))
np.save("job_links.npy", job_links)
