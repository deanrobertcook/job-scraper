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
    'gd-csrf-token': 'uIaW6I5aCn5g0BD9F64KOA:_B_vXQgrCOpQjhLOZGZ24959kx_hHS3jb6xYDPJ2USAdFLuadLC5Hi_JtKvUysvf_rqj7bvgzLSteGbwAuydYA:zoXH6b_y2hGrv_2YeGHHr8Tyz9XoY9Tr8Iiacs3Ahtg',
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
    'cookie': 'gdId=9b71847a-29df-4b62-84bc-ffd277682f95; trs=direct:direct:direct:2021-06-13+02%3A56%3A04.116:undefined:undefined; indeedCtk=1f82cpfbou2ct801; _optionalConsent=false; G_ENABLED_IDPS=google; JSESSIONID_JX_APP=6B26178413145BD4356858ACAD4D6548; GSESSIONID=9b71847a-29df-4b62-84bc-ffd277682f95+1623677229683; cass=2; gdsid=1623677229683:1623677229683:1B4C97995A6F7FF2698FE7A17BA4DFE7; asst=1623677229.0; bs=1LPPFNwuXl2uNnqkzLdPEQ:gSM6468bX3SltOPr-rVvIWRbEP0sjvCEcF2Wcnc7-yKeobOiPKUhFRA-IxX6C74mS7q6bDOUMODbdp4umUQ0pumK7WxGZcKMLVt0iANCBIc:XUHI8e85z8b0qEZtEukOro98FTykzw2_2wrbnc1JWTE; __cf_bm=d01a969f37110764047eeae2ea88a41695fa673d-1623677233-1800-ATm7pjhXdX29rW+iWHfsWF3Vua7JnDsoJFnd14ooAkgnS6IqL1g9NqXTibsWuvOm5AVkohucRz6y/yq18A3iGLY=; _ga=GA1.2.787950244.1623578167; _gid=GA1.2.1077055335.1623677240; _dc_gtm_UA-2595786-1=1; _GA_Job_Session=true; _gat_UA-2595786-1=1; OptanonConsent=isIABGlobal=false&datestamp=Mon+Jun+14+2021+15%3A27%3A21+GMT%2B0200+(Mitteleurop%C3%A4ische+Sommerzeit)&version=6.8.0&hosts=&consentId=4d858633-6e93-4812-bcf0-bc1b15b82aa9&interactionCount=1&landingPath=NotLandingPage&groups=C0001%3A1%2CC0003%3A0%2CC0002%3A0%2CC0004%3A0%2CC0017%3A0&AwaitingReconsent=false; JSESSIONID=943C03706C9CB9873C9BF4A79E96B7D5; g_state={"i_p":1623763644954,"i_l":2}; _ga_RC95PMVB3H=GS1.1.1623677233.3.1.1623677261.32; AWSALB=nAXEY2KDPoK/8LKy/CntC7X+//IwnX1FB7Xo1z6at/JLTzNT0xJ48XnMWNEcp4zTB2pgeC6w+n32qOZ3EgGST0k5eWMNdqyaH0AzYmz2irMJFpe9dHU/XFO10jLXYLS4yjQDT+sDxFuA1nw8IJKyGIcQKwZdT3zaactjW+iDcHk3DLJtFJIrZY9V8W8k3w==; AWSALBCORS=nAXEY2KDPoK/8LKy/CntC7X+//IwnX1FB7Xo1z6at/JLTzNT0xJ48XnMWNEcp4zTB2pgeC6w+n32qOZ3EgGST0k5eWMNdqyaH0AzYmz2irMJFpe9dHU/XFO10jLXYLS4yjQDT+sDxFuA1nw8IJKyGIcQKwZdT3zaactjW+iDcHk3DLJtFJIrZY9V8W8k3w==',
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
    scrape(range(11, 31))
