import os
import requests
import json
from dotenv import load_dotenv, find_dotenv
import time
from python_graphql_client import GraphqlClient
from bs4 import BeautifulSoup

load_dotenv(find_dotenv())

GD_USERNAME = os.environ.get("GD_USERNAME")
GD_PASSWORD = os.environ.get("GD_PASSWORD")

HEADERS = {
    'authority': 'www.glassdoor.de',
    'sec-ch-ua': '" Not;A Brand";v="99", "Google Chrome";v="91", "Chromium";v="91"',
    'apollographql-client-name': 'job-search',
    'gd-csrf-token': '1KOKqDiKjreTWi6-dTR9tA:hFhtlTj1BCQifkTPQ4gf1ppWbpdy3ZM8DFS_6b9A_4tvXAXtpUHzoH2AO0j32dAYD8BQ2gdyStZ3vnpEqZ9oCA:jb3ywoolvtXzMU9NVldxPcBJWHGHeWT4xteeDc9Kr4Y',
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
    'cookie': 'gdId=c77c7a0d-1867-4568-a4e0-cd5bf4b6887f; trs=https%3A%2F%2Fwww.google.com%2F:SEO:SEO:2021-06-09+06%3A51%3A15.487:undefined:undefined; _gid=GA1.2.1259183532.1623246679; G_ENABLED_IDPS=google; fpvc=1; OptanonAlertBoxClosed=2021-06-09T13:51:30.439Z; _optionalConsent=true; _gcl_au=1.1.1658861872.1623246691; _fbp=fb.1.1623246690902.370312596; __gads=ID=ebaab3dacb72eeeb:T=1623246691:S=ALNI_MYXvefDJxK8vgqBBKG0FsnNYffmIQ; ht=%7B%22quantcast%22%3A%5B%22D%22%5D%7D; indeedCtk=1f7ohumvj3oah001; ki_r=; ki_u=243d60fe-cc57-5525-e71e-90a3; uc=44095BCBCAA84CA8D083AA33D0C199178AE8F35E9AD7F8C96075743956155E8B7639D64B8B3F63695F77B0FBAF5F06A3C4DA4682142FBDBA3FC6A7D3378C3A4E6FC7692571A8CF3499237648299ADA7B3EFA9081DD1A095CDDF0DE101785CAE097D523ED94F3B235D920FB3E6E3FB5964AD7208E146B8D97DBA9E75AAA5C08C38B2219EC613DB9E761C71275C1DC27D0; ki_s=198467%3A1.0.0.0.2%3B209117%3A1.0.0.1.2; ki_t=1623248074564%3B1623248074564%3B1623279774455%3B1%3B3; SameSite=None; JSESSIONID_JX_APP=AACDB58B496DD272B52EF9D4DCC2205C; GSESSIONID=c77c7a0d-1867-4568-a4e0-cd5bf4b6887f+1623318105007; cass=2; gdsid=1623318105007:1623318105007:BEF66E73CDBFCDA70F959126A1EC8F82; at=8b_AWYlMmEkDDu4JOS5NhU6nzFNUtSKF_GG4vkAKvnF_rWm3wCWHjf31um7ZF3JkAjs23KBqtNfJwvHZI9bni5JCbAymtbKFo4F-DvlHnDb7aktKP8PR7xkhDeJzeLbBoy7tYmhQ5q61XJPSL5hecEh1mjdG5QbIZpuw6R3m9t4Gy4d1g0hr4tWw4EWtI5L7HGlg0VqjlbT3SJAOzav4C3-ITjDj3bMbbgO_9vyMVgc3sxx_b9NrVgXgEXESmI-eil5brtA2oNSZRaXetfyiffunuFTAC4j8pmSt4jbKSrN31D8XxizWIUS6VLw47sGDKgPH4j5VlSQUFR5fpLu4w3E2wGWn_eDO2XNkjyl3IR92vS-HklldKBVkQB-Pibe91_zXWrkzngSLeZeMXueByc_eYMSQDiRNR8mI-gTXriVDbN01x21-wHuG6ZG4-iIMjR0jtGJZpVEeJWghOFgEaAW5i_si1Ix_OP3ObGWHc3xZfCI61dnYpQqRzsu2L_hs3kY46P9dp1Z_EFmK_mGLpl5rXzpEC1fWQJ2dVzRk9PPmFR2laaEqmIZW3Y42Sn3vTs0LpytEx0r5BqZL6wrPCHha2-K4BU_eduivP1WAlZ7zsvYa37qxZRWVzhLw2o3Sv1PVwuNtILpxcXYyv7BDdcXfdehua0BFPdlWjmI3iYCdk6bqjQQGz4Y0yEm5Ss7clBo5Zf0UvuP6LOAuyeAmrXPWqi3S8MMjy3bgWuHjHorPYFnkjAkQBBdgongqVJ1V1x8a_T_djZb3DKJ0pxICNIQvGLjwsXiwPdenqcDMEcipxbjZNqGp8NbF0BahxSd0-h9aOrh6TiDTBD1V2XuOmP_CclrxVGf_9OrC3Lbg268nIv49qpJZoXan-bvWS55xML8; asst=1623318104.0; bs=lRkjM510PQKugHkMbIfHnA:OBWhGztHiqH3zv3WLnoHV-tP_R_SY5_l1GCRNTy3XYDOYYcrzJJMD9xFp8SI4axmgUMK-w-Vkfc0nCcWKvBkILCtrZ94y6wXPp7hrLPI5tM:DGwV9fEvyTltnZ_sVvgTk41LHoVNSmd3LlWoe6BPcwc; __cf_bm=34ca0ac2478e6480ea64bceb2dea1d77ca1ce44b-1623318105-1800-ARn1H/wDwjtNLr/WKJmmcjLooXot8sY8t4rt24+AtB/ti4fTFTM9qB4OhrqKGbvkJOIKLNRShuKXcX0uJ/DZyoo=; JSESSIONID=B48BD4E7F084756BBC1FE3CF72F4A022; _ga=GA1.2.1343046783.1623246679; _dc_gtm_UA-2595786-1=1; _GA_Job_Session=true; _gat_UA-2595786-1=1; OptanonConsent=isIABGlobal=false&datestamp=Thu+Jun+10+2021+11%3A41%3A54+GMT%2B0200+(Central+European+Summer+Time)&version=6.8.0&hosts=&consentId=2053cc3e-86db-45c8-96fd-996656693761&interactionCount=2&landingPath=NotLandingPage&groups=C0001%3A1%2CC0003%3A1%2CC0002%3A1%2CC0004%3A1%2CC0017%3A1&geolocation=DE%3BBE&AwaitingReconsent=false; AWSALB=IDmOIz5nBq9bK99LQ5z5vNhD+S4Woeu3RfAgbiyl61LOJGEkhxbyzrMoDtYB6eYOlEwDWT0JQoQmi+etp40AUSfr+x/SDS972P7hvlpp1EBeA8Bg9n+hQGlgUGouFW+4hgwE+ebLhM/KxJeo6Zmbk114tT+NenMVGHfjSfD1tTnx5vbe7mIFUYP4GfHAu+Qbp3lC9sDBgddNa5Y9Bg8FrczWMrhp2IbV5rNggbl9VtzOj1wqLx4rXcJk6BVtk2U=; AWSALBCORS=IDmOIz5nBq9bK99LQ5z5vNhD+S4Woeu3RfAgbiyl61LOJGEkhxbyzrMoDtYB6eYOlEwDWT0JQoQmi+etp40AUSfr+x/SDS972P7hvlpp1EBeA8Bg9n+hQGlgUGouFW+4hgwE+ebLhM/KxJeo6Zmbk114tT+NenMVGHfjSfD1tTnx5vbe7mIFUYP4GfHAu+Qbp3lC9sDBgddNa5Y9Bg8FrczWMrhp2IbV5rNggbl9VtzOj1wqLx4rXcJk6BVtk2U=; _ga_RC95PMVB3H=GS1.1.1623318078.7.1.1623318130.8',
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

def tidy_json():
    f = open('misc/graph_request', 'r')
    s = f.read().replace('\\\\n', '').replace('\\"', '"')
    s = ' '.join(s.split())
    return json.loads(s)

def job_info(jobListingId):
    client = GraphqlClient(endpoint='https://www.glassdoor.de/graph', headers=HEADERS)
    variables = {'enableReviewSummary':False, 'jl':jobListingId, 'queryString': 'jobListingId={}'.format(jobListingId) }
    query = """
        query JobDetailQuery($jl: Long!, $queryString: String, $enableReviewSummary: Boolean!) {
          jobView(listingId: $jl, contextHolder: { queryString: $queryString }) {
            ...DetailFragment
              employerReviewSummary @include(if: $enableReviewSummary) {
                  reviewSummary {
                      highlightSummary {
                          sentiment
                          sentence
                          categoryReviewCount
                          __typename
                       }
                       __typename
                  }
                  __typename
              }
              __typename
           }
        }

        fragment DetailFragment on JobView {
          header {
            ageInDays
            employer {
              name
              size
            }
            expired
            goc
            jobTitleText
            jobTypeKeys
            locationName
            normalizedJobTitle
          }
          job {
              description
              discoverDate
              eolHashCode
              importConfigId
              jobReqId
              jobSource
              jobTitleId
              jobTitleText
              listingId
              __typename
            }
        }
    """
    return client.execute(query=query, variables=variables)

def query_graphql_schema():
    client = GraphqlClient(endpoint='https://www.glassdoor.de/graph', headers=HEADERS)
    #query = 'query{__schema{types{name,fields{name}}}}'
    query = 'query{__schema{queryType{name}}}'
    data = client.execute(query=query)
    print(data)

def get_page(page_num):
    res = requests.get('https://www.glassdoor.de/Job/berlin-data-science-jobs-SRCH_IL.0,6_IC2622109_KO7,19{}.htm'.format(page_num), headers=HEADERS)
    return res.content

def jobids_from_page(html):
    soup = BeautifulSoup(html, 'html.parser')
    job_els = soup.find_all(attrs={"data-id": True})
    return list(map(lambda x: x['data-id'], job_els))

def scrape():
    html = get_page(2)
    jobids = jobids_from_page(html)
    out = open('output/page1.json', 'w')
    #jobs_info = []
    for id in jobids:
        info_js = job_info(id)
        print(info_js)
        out.write(json.dumps(info_js))
    out.close()

if __name__ == "__main__":
    json = map(lambda x: { 'a' : x, 'b': { 'c': x*x } }, range(3))
    out = open('output/page1.json', 'w')
