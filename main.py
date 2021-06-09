import os
import requests
import json
from dotenv import load_dotenv, find_dotenv
import time
from python_graphql_client import GraphqlClient


load_dotenv(find_dotenv())

GD_USERNAME = os.environ.get("GD_USERNAME")
GD_PASSWORD = os.environ.get("GD_PASSWORD")

HEADERS = {
    'authority': 'www.glassdoor.de',
    'sec-ch-ua': '" Not;A Brand";v="99", "Google Chrome";v="91", "Chromium";v="91"',
    'apollographql-client-name': 'job-search',
    'gd-csrf-token': '0HpLnx4PbKRisulxK22bUA:6Plt5OBEGCQmz2DHw6S8_-YYC8qNarNOfnphFAGQ-ZIzQApltc8y6GuS_pZ1Vtzr0MyBlrQpNAOlmMZQm7MTSQ:3A7k4h5lET76f0tSNWSdM7y580ZT6nRTAJZOEXQRmZk',
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
    'cookie': 'gdId=c77c7a0d-1867-4568-a4e0-cd5bf4b6887f; trs=https%3A%2F%2Fwww.google.com%2F:SEO:SEO:2021-06-09+06%3A51%3A15.487:undefined:undefined; _gid=GA1.2.1259183532.1623246679; G_ENABLED_IDPS=google; fpvc=1; OptanonAlertBoxClosed=2021-06-09T13:51:30.439Z; _optionalConsent=true; _gcl_au=1.1.1658861872.1623246691; _fbp=fb.1.1623246690902.370312596; __gads=ID=ebaab3dacb72eeeb:T=1623246691:S=ALNI_MYXvefDJxK8vgqBBKG0FsnNYffmIQ; ht=%7B%22quantcast%22%3A%5B%22D%22%5D%7D; indeedCtk=1f7ohumvj3oah001; ki_r=; ki_u=243d60fe-cc57-5525-e71e-90a3; uc=44095BCBCAA84CA8D083AA33D0C199178AE8F35E9AD7F8C96075743956155E8B7639D64B8B3F63695F77B0FBAF5F06A3C4DA4682142FBDBA3FC6A7D3378C3A4E6FC7692571A8CF3499237648299ADA7B3EFA9081DD1A095CDDF0DE101785CAE097D523ED94F3B235D920FB3E6E3FB5964AD7208E146B8D97DBA9E75AAA5C08C38B2219EC613DB9E761C71275C1DC27D0; ki_t=1623248074564%3B1623248074564%3B1623256439526%3B1%3B2; ki_s=198467%3A1.0.0.0.2%3B209117%3A1.0.0.1.2; GSESSIONID=c77c7a0d-1867-4568-a4e0-cd5bf4b6887f+1623246675455; cass=2; asst=1623276646.0; __cf_bm=b9c827b074a990bf3a853ca53a709b67dfec200f-1623278357-1800-AXPPP0gI/zd8aMuky/kjhMPykRw4XiwrkzS33HwIbemsNRKeN+cUIRIgkhwq9uDdry3Q0qUZZjbjgaPoPDeIpJU=; _gat_UA-2595786-1=1; SameSite=None; JSESSIONID_JX_APP=90986EBC0E5779D63BE2CD4DCC1408CD; gdsid=1623246675455:1623278367436:0FF338DACD978C41E8AE905E31391EBF; at=hm14fcp-NY4kRKj2FwXdr2lpxTVu4bNCYGVdkBaF57Mqan0vbKOsKFaCnB0LP1QzWta6LfrJhDd0LVsAbmphTcaaW9GIJ7E0FCamRbhkJXw0ZoqNO2RmDYyzpnpOJW135IBb9tzItt3RbfJYW49u2_u6qTaBsZiQREyM7cuhAItjGNBHp0jpk5aBHRFBzfWe-Pjw6WULJlIHcAYf9qYWhx01NCr6Geobgzd1C9WTEwF_Y9BtjZxueMv4QY-rnLGutXwC1SvRTY2x-sSFojFgzXEtdDz5RRF6FEH6LHy9QUCUdtYcMHvQsmC-PuUYm68KSU_h5UqlsfGZYcelUT50Bke-AU26WvcCc0L4PzuvwQRbj4DYmd9oKNX42gyVFObcORp96n99gaHEIhWKGazQN1FpICb7BhEDNtmJk2YpAwWfB5vAbNjCjZRv9aVD_XkhUeUI9Fz9sSkrx9S7XjgdMSQquDb36mSvfR_o9NPOHrBJD89mx7qh-SHJyy-rtTegHUxRY0ePoOV4xy8NZY_GXRnyBoEA9udIWOoZHt0_v8jzzo6KlexYJfmd0kaW-KkU21x00xAnoyH80v8WNu12awQTlvagohfylDNSRMVwfEMv_-V_Ch7PeSZcb8a3kBK8bS_wvDOjUPmdrYFC07i114EskQ2opA29Qfy5iU-P2GpJp9k-uSdNAgvcHjYT-etkWf8eCRA9wcN9-7p9LwzhLvEX_I9HBKlON0BPiW2uS1QEScHz2UmJaanfTzxiUXUu-XENguseVyDzQ6s1WWp6JrWRxxeX56OZeR4uMx5UcGNLB9QJVDew7MhxbHmWjMcKXcIbbLeko4NzTeGn0pilp2bykwTQDZqOdmiR-dHO9bHCyXJJuq6T2XTXec811yiCwug; bs=0oz7ib6dhWDCPfzw-Vuzmw:YYaoxRRLmxmQTDtfkjY73zbI7n5trHT7XXC8QsSoviJD6l7olR3FK1_SoPtisL_3erIR5WLEm-Sg_ObRMzwFKUtkrTFVv8Ob0fpBICTUe_c:sIkwLSEstafqmn00zGBhIkDYtRYd_8iinDPVURO9TXw; JSESSIONID=305563EFA9A3CF56AAD1F4FC4690D8B2; _ga=GA1.2.1343046783.1623246679; _dc_gtm_UA-2595786-1=1; _GA_Job_Session=true; OptanonConsent=isIABGlobal=false&datestamp=Thu+Jun+10+2021+00%3A39%3A37+GMT%2B0200+(Central+European+Summer+Time)&version=6.8.0&hosts=&consentId=2053cc3e-86db-45c8-96fd-996656693761&interactionCount=2&landingPath=NotLandingPage&groups=C0001%3A1%2CC0003%3A1%2CC0002%3A1%2CC0004%3A1%2CC0017%3A1&geolocation=DE%3BBE&AwaitingReconsent=false; AWSALB=qAQu7H0JJYLMoOzz07XdxDufajgYtVd4AVlOvw4lVNbMiSmMwCpPTTTtFzpTWzyOCSMjQYJ2xpL6V0hMztK3aQnrpN1mDKdokIsYOPgM1eGX+jJCCsFwKeVQ0NJ/ew90M32cNeNgW4PxkXDpsOBqc1eboe/Qq85EIeWAY3VDB17m6HuL2I2IvQPCT426ep98SWKZkwEa2+WbJm5AwUbrov7s0i3JT+v+SOydEQLQODzjL4F8ghzar8VQiZtemi8=; AWSALBCORS=qAQu7H0JJYLMoOzz07XdxDufajgYtVd4AVlOvw4lVNbMiSmMwCpPTTTtFzpTWzyOCSMjQYJ2xpL6V0hMztK3aQnrpN1mDKdokIsYOPgM1eGX+jJCCsFwKeVQ0NJ/ew90M32cNeNgW4PxkXDpsOBqc1eboe/Qq85EIeWAY3VDB17m6HuL2I2IvQPCT426ep98SWKZkwEa2+WbJm5AwUbrov7s0i3JT+v+SOydEQLQODzjL4F8ghzar8VQiZtemi8=; _ga_RC95PMVB3H=GS1.1.1623278358.6.1.1623278388.30',
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
    client = GraphqlClient(endpoint='https://www.glassdoor.de/graph', headers=HEADERS)
    variables = {'enableReviewSummary':False, 'jl':4105061587, 'queryString': 'pos=102&ao=1044074&s=149&guid=00000179f2ee36b89cc87c68dd88fcdd&src=GD_JOB_AD&t=SRFJ&vt=w&uido=E72EB9FF023BC985E69A0D4700D2593A&cs=1_09fd0108&cb=1623278368915&jobListingId=4105061587' }
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
            jobLink
            adOrderId
            advertiserType
            ageInDays
            applicationId
            appliedDate applyUrl
            applyButtonDisabled
            blur
            coverPhoto {
              url
              __typename
            }
            divisionEmployerName
            easyApply
            easyApplyMethod
            employerNameFromSearch
            employer {
              id
              name
              size
              squareLogoUrl
              __typename
            }
            expired
            goc
            hideCEOInfo
            indeedApplyMetadata
            indeedJobAttribute {
              education
              skills
              __typename
            }
            jobTitleText
            jobTypeKeys
            jobCountryId
            jobResultTrackingKey
            locId
            locationName
            locationType
            normalizedJobTitle
            organic
            payCurrency
            payPercentile90
            payPercentile50
            payPercentile10
            hourlyWagePayPercentile {
              payPercentile90
              payPercentile50
              payPercentile10
              __typename
            }
            payPeriod
            rating
            salarySource
            savedJobId
            sgocId
            sponsored
            categoryMgocId
            urgencySignal {
              labelKey
              messageKey
              normalizedCount
              __typename
            }
            __typename
          }
          __typename
        }
    """
    data = client.execute(query=query, variables=variables)
    print(data)

def getPage():

    res = requests.get('https://www.glassdoor.de/Job/berlin-data-science-jobs-SRCH_IL.0,6_IC2622109_KO7,19.htm', headers=HEADERS)

    outF = open("output/myOutFile.html", "wb")
    outF.write(res.content)
    outF.close()

if __name__ == "__main__":
    graphQLTest()
