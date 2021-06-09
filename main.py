import os
import requests
import json
from dotenv import load_dotenv, find_dotenv
import time
from graphql import GraphqlClient

load_dotenv(find_dotenv())

GD_USERNAME = os.environ.get("GD_USERNAME")
GD_PASSWORD = os.environ.get("GD_PASSWORD")

HEADERS = {
    'authority': 'www.glassdoor.de',
    'sec-ch-ua': '" Not;A Brand";v="99", "Google Chrome";v="91", "Chromium";v="91"',
    'apollographql-client-name': 'job-search',
    'gd-csrf-token': 'UKvBGWgGpe2krtC_dZY6Zw:03hNdxpCJfncjZ3uag21R6WCJUqh0wx0nkrybh3Y9cVRaUI_zPIw0x0i6pE8bZblAe4ojq1NOOJjVdvLFn8kTA:DptRLODgcKOZmpA7ZPe8Ia4ZDUGdXJL8A9RKyGv1VgE',
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
    'cookie': 'gdId=c77c7a0d-1867-4568-a4e0-cd5bf4b6887f; trs=https%3A%2F%2Fwww.google.com%2F:SEO:SEO:2021-06-09+06%3A51%3A15.487:undefined:undefined; _gid=GA1.2.1259183532.1623246679; G_ENABLED_IDPS=google; fpvc=1; OptanonAlertBoxClosed=2021-06-09T13:51:30.439Z; _optionalConsent=true; _gcl_au=1.1.1658861872.1623246691; _fbp=fb.1.1623246690902.370312596; __gads=ID=ebaab3dacb72eeeb:T=1623246691:S=ALNI_MYXvefDJxK8vgqBBKG0FsnNYffmIQ; ht=%7B%22quantcast%22%3A%5B%22D%22%5D%7D; indeedCtk=1f7ohumvj3oah001; ki_r=; ki_u=243d60fe-cc57-5525-e71e-90a3; JSESSIONID_UP_APP=4E1BA8258E1EFBE77870070E6CAE60BE; uc=44095BCBCAA84CA8D083AA33D0C199178AE8F35E9AD7F8C96075743956155E8B7639D64B8B3F63695F77B0FBAF5F06A3C4DA4682142FBDBA3FC6A7D3378C3A4E6FC7692571A8CF3499237648299ADA7B3EFA9081DD1A095CDDF0DE101785CAE097D523ED94F3B235D920FB3E6E3FB5964AD7208E146B8D97DBA9E75AAA5C08C38B2219EC613DB9E761C71275C1DC27D0; JSESSIONID_KYWI_APP=CC50061AF0B7C4B63A0D49BF1F82B8FF; ki_t=1623248074564%3B1623248074564%3B1623256439526%3B1%3B2; ki_s=198467%3A1.0.0.0.2%3B209117%3A1.0.0.1.2; asst=1623267026.0; SameSite=None; JSESSIONID_JX_APP=4D6D83A7C8F14948585D86479455EC0F; GSESSIONID=c77c7a0d-1867-4568-a4e0-cd5bf4b6887f+1623246675455; cass=2; gdsid=1623246675455:1623268293513:6D77BA06B0FB9DB020E27067FF9E7CFE; at=4OlUnSWMvu5UOuEodpZ1pGN-ka1EkXp_KGAazeMrZh4GR2Fx7DjW_arv7uA1Bqh4WIKLtxkzGuneJ5wwhfYvbwQjPCUqKxW6jm7O8w5zwEdTRjs44AKL-eilvtsnTGAECJrQga5UUvbUss7dRl8K52NF1BLWfVmUr8kq_BBJO9R0XgjAAAnlOiv17J2dFyHMJIaxbCyehEILa_80f9UFLLcZJn66BpvEeuk_C8i2fPKem1YDvsriN6CeK0jngFd_bD1SfWGdlAzsM9Z1KqFh_I24dCddJ7phfgAMZkAygZyKdv72lRDC0eiisQsu6fY-IrPpQNjgtnq7EWz5VwdgogTsfsky3ANUN4iphAyw4J2V-bPfy7C5cOUraYSqwb_WFHuOQeRTxlHqCBJGBU3AlUoaWZ0LMiHv6AJUsyvrphj3FG7NtNsJxuuYvBePCxvQkvi_8yclvKTONRfePbyH3DmjCy8R3px59ZAzOfHdj-MxabA1kosCWVYBL1xbMPc34mFSXs8nCLLR6464pjlpu2nTPbr7AlImbfNHezH6IwxqVzmbgimIEBJQWt2uDnXUOEWF4u6FnmgUcuRsk1A16DPFmUdAwnS67_Sm8M2eBDD7GPT6UDbaEMKWCmwCWacdTgiZh-moWorpCibOyengCNp_gHJSTo_PtlDUtbQI_qk1i_gda9yiT2Z24YMIAR4ISdg5xKdgj27NI_X1pMmk48Z0WqHJM9CeLkgToUO28iB6nRzbPYxavHpLvwFS3hrRZs0Rd4HZfcDDifakK_qVQrlyGVY9zl-Rd43y8eF6V-y4zx_yg4DZZYzyaThdhFZwvX-90RZKgtTmBAg7iuzPK3SqwNlLNPVc-IgeD5WlehbJMjtE4oBay1zaNy_XdWKiW10; bs=3LStbCPMWQs4zKPvtE9P5g:m3JK7pnFDIYYMKSd_3j7rwg1nEyG96HsyFOOLYmO0ozCidahYh6TNcIySOme1guCBox86RyTkHeUvV2BDgicmG-YwIyDPf_OHRZUMO6BoBM:_hxTJ-RcMTP8ZCLvPoMfJRVLa5_HHzbIJPVqbxIZrDU; __cf_bm=a12db5563b1084e7ed3e5e311f61a4484705cc98-1623268298-1800-AVVxp2vbSAcVgm/izOANpxtoPQ7BEqH7ljE80UkZw6QuePvvhTxPEm6mdvMtWEJ0NU66ro9zeNFLh6IMdF/TVHE=; JSESSIONID=D719434186B4589183B0CE950D62D36B; _ga=GA1.2.1343046783.1623246679; _dc_gtm_UA-2595786-1=1; _GA_Job_Session=true; _gat_UA-2595786-1=1; _ga_RC95PMVB3H=GS1.1.1623268298.4.1.1623268308.50; AWSALB=ZG66G6eLB/gObWNgb3CQ3cgvGW4dHXG7HUZd2ZJ49R9KCsBp+Wbz0doxDLkS7cQifGXNzktHoAqA5qYrGtyspg/olXvSIkpBrnNGMuNtWzu7o8sxThEvl8jCDrjcsBqrLzb1n9L0gU4I13jsmabLb69lNlIJR2GkeSCBCWBKWKFBNTX9L9sGFwV94P75tH5onMe9uKcl3N8DKV4QetBYXtOwkaAido7OYl7heVhiguFbzhmq7U2MSZfVbUFpCDk=; AWSALBCORS=ZG66G6eLB/gObWNgb3CQ3cgvGW4dHXG7HUZd2ZJ49R9KCsBp+Wbz0doxDLkS7cQifGXNzktHoAqA5qYrGtyspg/olXvSIkpBrnNGMuNtWzu7o8sxThEvl8jCDrjcsBqrLzb1n9L0gU4I13jsmabLb69lNlIJR2GkeSCBCWBKWKFBNTX9L9sGFwV94P75tH5onMe9uKcl3N8DKV4QetBYXtOwkaAido7OYl7heVhiguFbzhmq7U2MSZfVbUFpCDk=; OptanonConsent=isIABGlobal=false&datestamp=Wed+Jun+09+2021+21%3A51%3A49+GMT%2B0200+(Central+European+Summer+Time)&version=6.8.0&hosts=&consentId=2053cc3e-86db-45c8-96fd-996656693761&interactionCount=2&landingPath=NotLandingPage&groups=C0001%3A1%2CC0003%3A1%2CC0002%3A1%2CC0004%3A1%2CC0017%3A1&geolocation=DE%3BBE&AwaitingReconsent=false',
}

def main():
    job_title = 'data science'#input('Job search input: ')
    location = ''#input('Location: ')

    tstamp = round(time.time() * 1000)
    print(tstamp)
    data = {
        'query': '"__schema": { "types": { "name" }'
    }
    res = requests.post('https://www.glassdoor.de/graph', headers=HEADERS, data=data)
    print(res, res.reason)

def tidyJson():
    f = open('misc/graph_request', 'r')
    s = f.read().replace('\\\\n', '').replace('\\"', '"')
    s = ' '.join(s.split())
    return json.loads(s)

def graphQLTest():
    headers = { 'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36' }
    client = GraphqlClient(endpoint="https://anilist.co/graphiql", headers=headers)
    query = """
        {
          __schema {
            types {
              name
            }
          }
        }
    """
    data = client.execute(query=query)
    outF = open("output/test.html", "wb")
    outF.write(data)
    outF.close()

def getPage():

    res = requests.get('https://www.glassdoor.de/Job/berlin-data-science-jobs-SRCH_IL.0,6_IC2622109_KO7,19.htm', headers=HEADERS)

    outF = open("output/myOutFile.html", "wb")
    outF.write(res.content)
    outF.close()

if __name__ == "__main__":
    graphQLTest()
