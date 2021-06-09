import os
import requests
from dotenv import load_dotenv, find_dotenv
from scraper import scraper

load_dotenv(find_dotenv())

GD_USERNAME = os.environ.get("GD_USERNAME")
GD_PASSWORD = os.environ.get("GD_PASSWORD")

def main():
    print('Glassdoor Job Scraper.')
    job_title = 'data science'#input('Job search input: ')
    location = ''#input('Location: ')

    s = requests.Session()
    #s.headers.update({'x-test': 'true'})
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

    url = 'https://www.glassdoor.de/graph'
    res = requests.post(url, headers=headers, data = {'key':'value'})
    print(res)



def getPage():
    res = requests.get('https://www.glassdoor.de/Job/berlin-data-science-jobs-SRCH_IL.0,6_IC2622109_KO7,19.htm', headers=headers)

    outF = open("output/myOutFile.html", "wb")
    outF.write(res.content)
    outF.close()

if __name__ == "__main__":
    main()
