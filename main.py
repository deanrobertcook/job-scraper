import os
import requests
import json
import itertools
from datetime import datetime
from python_graphql_client import GraphqlClient
from bs4 import BeautifulSoup
from tools import flatten_json

DS_SEARCH_URL = 'https://www.glassdoor.de/Job/berlin-data-science-jobs-SRCH_IL.0,6_IC2622109_KO7,19_IP{}.htm'

#Go to
HEADERS = {
    'authority': 'www.glassdoor.de',
    'sec-ch-ua': '" Not;A Brand";v="99", "Google Chrome";v="91", "Chromium";v="91"',
    'apollographql-client-name': 'job-search',
    'gd-csrf-token': 'XnHnRBpecsnltwfSsuUq7w:1Nj0DE0ZKlMyfApYdSb6GMgmVywB33JaM5jY0tWH5Q8HXg0rkG6oSVwTq2XiHyN23z5EJhwyzHq214TFP9mBMg:_X86EbGAcpomAyIzTTM1nNB6PXTHTmPf43Q6Sk0-6TQ',
    'sec-ch-ua-mobile': '?0',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36',
    'content-type': 'application/json',
    'accept': '*/*',
    'apollographql-client-version': '0.10.102',
    'origin': 'https://www.glassdoor.de',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-mode': 'cors',
    'sec-fetch-dest': 'empty',
    'referer': 'https://www.glassdoor.de/',
    'accept-language': 'en-US;q=0.9,en;q=0.8',
    'cookie': 'SameSite=None; JSESSIONID_JX_APP=89A2B9C2383C5E7B0E86200AD53765FD; GSESSIONID=9b71847a-29df-4b62-84bc-ffd277682f95+1623578164102; gdId=9b71847a-29df-4b62-84bc-ffd277682f95; trs=direct:direct:direct:2021-06-13+02%3A56%3A04.116:undefined:undefined; cass=2; gdsid=1623578164102:1623578164102:881D4A0A153BA160041333511B18A694; asst=1623578164.0; bs=0KyxbgWiOoyrxAatILnvOg:upq3cdAY-ogmm_Z4rNYRfJ1CHT_1mJxhNwEqeFZIWfjKGhrbnOAzG9pzBQDDvYmDA6kijEnIavaD52c01_35d5kZrMHJdZ0zsFj4N556-Eo:Bg6WqsDs0Er_f-74bkbo7XO7z896-8srlWDQAluEBww; __cf_bm=7d4ebef69d65784899ca07bd53c649b09da973ac-1623578164-1800-AeTtqTXksgKApYCGR/5ALOPoBmtg57id8jlALlcNGN63e/DDC6kwnspfXnsyt6WH2JlgIDotPlgVudSYlTJ39Sk=; indeedCtk=1f82cpfbou2ct801; JSESSIONID=60D3B2D90A1EE8C98CF44F30859419BA; _ga=GA1.2.787950244.1623578167; _gid=GA1.2.686091598.1623578167; _dc_gtm_UA-2595786-1=1; _GA_Job_Session=true; _gat_UA-2595786-1=1; AWSALB=jYekfAJCughC9hJV9dGQxVXOwhosZF/8uAGh8bMz4oloGhCVKyLxKllS6f2/vuCbdJXAqiYtrr/VoxiWJXDj16Mo4vFvQVxBNOr0G56USMIfCzaeOHYIFPCyQJwheXpjfHhyt6sPf2b1GzFvVRTDT+zobtbbomInjPIcD8WLNEMSa8KH3b6cpN9AkaQxpQ==; AWSALBCORS=jYekfAJCughC9hJV9dGQxVXOwhosZF/8uAGh8bMz4oloGhCVKyLxKllS6f2/vuCbdJXAqiYtrr/VoxiWJXDj16Mo4vFvQVxBNOr0G56USMIfCzaeOHYIFPCyQJwheXpjfHhyt6sPf2b1GzFvVRTDT+zobtbbomInjPIcD8WLNEMSa8KH3b6cpN9AkaQxpQ==; _optionalConsent=false; OptanonConsent=isIABGlobal=false&datestamp=Sun+Jun+13+2021+11%3A56%3A08+GMT%2B0200+(Mitteleurop%C3%A4ische+Sommerzeit)&version=6.8.0&hosts=&consentId=4d858633-6e93-4812-bcf0-bc1b15b82aa9&interactionCount=0&landingPath=https%3A%2F%2Fwww.glassdoor.de%2FJob%2Fberlin-data-science-jobs-SRCH_IL.0%2C6_IC2622109_KO7%2C19.htm&groups=C0001%3A1%2CC0003%3A0%2CC0002%3A0%2CC0004%3A0%2CC0017%3A0; g_state={"i_p":1623585371407,"i_l":1}; G_ENABLED_IDPS=google; _ga_RC95PMVB3H=GS1.1.1623578166.1.1.1623578175.51',
}

def job_info(jobListingId):
    print('fetching job info for: {}'.format(jobListingId))
    client = GraphqlClient(endpoint='https://www.glassdoor.de/graph', headers=HEADERS)
    variables = {'enableReviewSummary':False, 'jl':jobListingId, 'queryString': 'jobListingId={}'.format(jobListingId) }
    with open('glassdoor_used.graphql','r') as f:
        query = f.read()
        return client.execute(query=query, variables=variables)

def get_page(page_num):
    print('fetching page: {}'.format(page_num))
    res = requests.get(DS_SEARCH_URL.format(page_num), headers=HEADERS)
    return res.content.decode('utf-8')

def jobids_from_page(html, page_num):
    print('processing html with len: {}'.format(len(html)))
    soup = BeautifulSoup(html, 'html.parser')
    job_els = soup.find_all(attrs={"data-id": True})
    return list(map(lambda x: x['data-id'], job_els))

def scrape(page_range):
    filename = get_filename()
    os.makedirs(os.path.dirname(filename), exist_ok=True)

    for p in page_range:
        jobids = jobids_from_page(get_page(p), p)
        job_infos = [job_info(jl) for jl in jobids]

        json_data = []
        if os.path.isfile(filename):
            with open(filename) as f:
                json_data = json.load(f)

        json_data.extend([flatten_json(job_i) for job_i in job_infos])

        with open(filename, 'w') as f:
            json.dump(json_data, f)

def get_filename():
    return 'output/glassdoor-jobs_{}.json'.format(datetime.now().strftime("%Y-%m-%d_%H:%M:%S"))

if __name__ == "__main__":
    scrape(range(1, 11))
