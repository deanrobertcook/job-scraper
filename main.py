import os
import requests
import json
import itertools
from datetime import datetime
from python_graphql_client import GraphqlClient
from bs4 import BeautifulSoup
from tools import flatten_json

HEADERS = {
    'authority': 'www.glassdoor.de',
    'sec-ch-ua': '" Not;A Brand";v="99", "Google Chrome";v="91", "Chromium";v="91"',
    'apollographql-client-name': 'job-search',
    'gd-csrf-token': 'CiDpuEBSBDlnZUboJhdJLw:92B31tqUh7di9I9Ti_QKJU87pGVN103ihnhAinC5y0oNzwjkZl_W3bkm3cMj6FRTFajngO-czAMqIwe3rwvTpg:O5CHbzbipGu-evb3sbUVnenviYs_fOnPfNHcjgbc2ts',
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
    'cookie': 'gdId=c77c7a0d-1867-4568-a4e0-cd5bf4b6887f; trs=https%3A%2F%2Fwww.google.com%2F:SEO:SEO:2021-06-09+06%3A51%3A15.487:undefined:undefined; _gid=GA1.2.1259183532.1623246679; G_ENABLED_IDPS=google; fpvc=1; OptanonAlertBoxClosed=2021-06-09T13:51:30.439Z; _optionalConsent=true; _gcl_au=1.1.1658861872.1623246691; _fbp=fb.1.1623246690902.370312596; __gads=ID=ebaab3dacb72eeeb:T=1623246691:S=ALNI_MYXvefDJxK8vgqBBKG0FsnNYffmIQ; indeedCtk=1f7ohumvj3oah001; ki_r=; ki_u=243d60fe-cc57-5525-e71e-90a3; uc=44095BCBCAA84CA8D083AA33D0C199178AE8F35E9AD7F8C96075743956155E8B7639D64B8B3F63695F77B0FBAF5F06A3C4DA4682142FBDBA3FC6A7D3378C3A4E6FC7692571A8CF3499237648299ADA7B3EFA9081DD1A095CDDF0DE101785CAE097D523ED94F3B235D920FB3E6E3FB5964AD7208E146B8D97DBA9E75AAA5C08C38B2219EC613DB9E761C71275C1DC27D0; ki_s=198467%3A1.0.0.0.2%3B209117%3A1.0.0.1.2; ki_t=1623248074564%3B1623248074564%3B1623279774455%3B1%3B3; SameSite=None; JSESSIONID_JX_APP=D2959C64ED3BCD626B377D908CA0F3D6; GSESSIONID=c77c7a0d-1867-4568-a4e0-cd5bf4b6887f+1623318105007; cass=2; gdsid=1623318105007:1623343223988:A6264C857AE5174F3C5A68E43BDAD5AD; at=kPKSqf2f9AeSVzBX8ovs-NwfrMDWsxDPXtH1afCiI1SQLY7NMLYl2X3lrMSX_IkIO49hpRmcLpJi3t4G44a-TbrFQiCw6sN3AJ7dsA7Ey2yx93r3JEC0okg4kJBNHSeeHDpjLvBpAdG23tiWnQ8jJD0jepGfaQ193W9EEyu9cdKfmegG8P-5A5G5R6Sl_WeyVewrdwI2R3M_r4fNl9tWDX0LbYhoiiMdaVDxnx7Sgph90UQO0thHopWNBjCs9nS8E6i9-_gZAGBe2KYBPupJjqZu-yvgIMdSv4p0ClwPSijwqgKgVJ63RJGLeukDNCy-7xHgT_Wc_M0cWDq9s7R4wfzEcurNc2TbJxkcidiHWsat2IG_9PvjsNoeX0rdi8X8D2hzXZJ3MLjqH1zCd1OH5GDwEl0qiqVqyvwPdTxawjrUBGeZ6qrzZexNFTA3dAA5gMK9QJk5ZW_NW1wkAz4MFeL7cmexeqv3bPQHIRJbUp0EKNtt5K0c6MGBWxXNMhyP7tF8akoGdM5osA6kWs_lsxbZWEscsixTkQQj7ArLA6TvChFt62_r9YYFyQfmIRVBjYyf2ieL27owom3OaqQ3lRRf3l8ILlTUkYPkyuuYWCCxqGYKw27KltHiSbsHk46Oy-ESmqrypEsbENtZmfVfc00V_TzSoXyugbjGP0E9v8H9DOhUxYAcwejAZ99CLmeOhkh4Ywj2vLYpPSk08vy1pQ0BuQrseVgb0vcCvqmizLjrUXEWPhsZ9QrBAaY2R5hHxAGZTaMMXAqe7ysBTmr9XAubcad7K-g1vRMefwqvzvGJooNOgUzEKD95ZgiybuMsF2zCffenKbki_ZT9rLm54DvMz7rcivMs4tOebqblc3Nxn7hVAtMocMwbQschOt9mkQA; asst=1623343223.0; bs=xHMV5EtYJe0zPRCKv6Y5Vw:HjQcyRAyEZFd6ia1rQ0HGagoJTB3pv6Tj1XcmPUZ7-tt_YSePC0SnX7vtfC8g5xuAs8KbYsmdX0qJsjwgfcba-HvHwbjMcISsJM9yPycoIc:8IQ_PZWwqK9ecZYIEObRvoigerTuBa4S2L8yGNlElyU; __cf_bm=650a5937b0bc98fe431adb6038003005b38eccd7-1623343224-1800-AWVgK2J7qQmqYwDLnB5hhmeNHpWdhb2wDnwdnBZYAXG6Gp2K13fkBYN/MHzcfkhBhN7xxbISj9OfbHLSVW7tNN4=; JSESSIONID=4B820A8E37D8FA35A4A10C321ADFAC00; _ga=GA1.2.1343046783.1623246679; _dc_gtm_UA-2595786-1=1; _GA_Job_Session=true; _gat_UA-2595786-1=1; OptanonConsent=isIABGlobal=false&datestamp=Thu+Jun+10+2021+18%3A40%3A28+GMT%2B0200+(Central+European+Summer+Time)&version=6.8.0&hosts=&consentId=2053cc3e-86db-45c8-96fd-996656693761&interactionCount=2&landingPath=NotLandingPage&groups=C0001%3A1%2CC0003%3A1%2CC0002%3A1%2CC0004%3A1%2CC0017%3A1&geolocation=DE%3BBE&AwaitingReconsent=false; _ga_RC95PMVB3H=GS1.1.1623343226.10.1.1623343229.57; ADRUM_BTa=R:25|g:5d7c4cf2-0d3a-4cc3-b00b-4d512ec5327d|n:glassdoor_17d346a0-2ec1-4454-86b0-73b3b787aee9; AWSALB=e25YerL4+QhD0Tu9AZfftTw2n1yP67D01k8tX2BAqNCkFwQyNdQrObZzqlQKgKaEqyMwL6+qEx8t3k86RMUZIJ8a8R5AAk/r49j2KZuDW6plaXd8FzYe668p62nFu7f+evYIOONtWqeZGTo4aKDbBC/uKkZiYuEDvVC9RX1blgsj+Pj78OtK/5KwMW/ed0OE3Jr7PcnQ7hXAzUIMUyWX6O/XcUfuaSByq93JtfyrM2DUzrhANOG2ZKCfjCAT11g=; AWSALBCORS=e25YerL4+QhD0Tu9AZfftTw2n1yP67D01k8tX2BAqNCkFwQyNdQrObZzqlQKgKaEqyMwL6+qEx8t3k86RMUZIJ8a8R5AAk/r49j2KZuDW6plaXd8FzYe668p62nFu7f+evYIOONtWqeZGTo4aKDbBC/uKkZiYuEDvVC9RX1blgsj+Pj78OtK/5KwMW/ed0OE3Jr7PcnQ7hXAzUIMUyWX6O/XcUfuaSByq93JtfyrM2DUzrhANOG2ZKCfjCAT11g=',
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
    res = requests.get('https://www.glassdoor.de/Job/berlin-data-science-jobs-SRCH_IL.0,6_IC2622109_KO7,19{}.htm'.format(page_num), headers=HEADERS)
    return res.content.decode('utf-8')

def jobids_from_page(html, page_num):
    print('processing html with len: {}'.format(len(html)))
    soup = BeautifulSoup(html, 'html.parser')
    job_els = soup.find_all(attrs={"data-id": True})
    return list(map(lambda x: x['data-id'], job_els))

def scrape(num_pages):
    pages = [get_page(p) for p in range(num_pages)]
    jobids = itertools.chain.from_iterable([jobids_from_page(html, i) for i,html in enumerate(pages)])
    job_infos = [job_info(jl) for jl in jobids]

    with open(get_filename(), 'w') as f:
        f.write(json.dumps([flatten_json(job_i) for job_i in job_infos]))

def get_filename():
    return 'output/glassdoor-jobs_{}.json'.format(datetime.now().strftime("%Y-%m-%d_%H:%M:%S"))

if __name__ == "__main__":
    scrape(1)
