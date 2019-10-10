url = "https://jp.linkedin.com/jobs/view/senior-data-scientist-at-agoda-1442563106?refId=3b5ed275-d1f6-4b1b-af77-b3a85fb8aa46&position=2&pageNum=0&trk=guest_job_search_job-result-card_result-card_full-click"
headers = {"Accept-Language": "en-US,en;q=0.5"}
page = requests.get(
    url,
    headers=headers,
)

soup.find_all("span", "posted-time-ago__text")[0].get_text()