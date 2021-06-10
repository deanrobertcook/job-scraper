import os
import requests
import json
import time
from python_graphql_client import GraphqlClient
from bs4 import BeautifulSoup

HEADERS = {
    'authority': 'www.glassdoor.de',
    'sec-ch-ua': '" Not;A Brand";v="99", "Google Chrome";v="91", "Chromium";v="91"',
    'apollographql-client-name': 'job-search',
    'gd-csrf-token': '6TRKQ53TNLxIhmRSOeuaAg:GXX-dfqB5-5bnjOKE1nOKDFLaSZaMOhAbYcQq7Evox5tQ9Q1hEnPxCYv7Bbb9EsGedwae6iOy1kcB9zZXNGQ7Q:L6L0hJIIrL7Si13IsSqwNQg1iG8teaJK0IFrd8ClnWY',
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
    'cookie': 'gdId=c77c7a0d-1867-4568-a4e0-cd5bf4b6887f; trs=https%3A%2F%2Fwww.google.com%2F:SEO:SEO:2021-06-09+06%3A51%3A15.487:undefined:undefined; _gid=GA1.2.1259183532.1623246679; G_ENABLED_IDPS=google; fpvc=1; OptanonAlertBoxClosed=2021-06-09T13:51:30.439Z; _optionalConsent=true; _gcl_au=1.1.1658861872.1623246691; _fbp=fb.1.1623246690902.370312596; __gads=ID=ebaab3dacb72eeeb:T=1623246691:S=ALNI_MYXvefDJxK8vgqBBKG0FsnNYffmIQ; ht=%7B%22quantcast%22%3A%5B%22D%22%5D%7D; indeedCtk=1f7ohumvj3oah001; ki_r=; ki_u=243d60fe-cc57-5525-e71e-90a3; uc=44095BCBCAA84CA8D083AA33D0C199178AE8F35E9AD7F8C96075743956155E8B7639D64B8B3F63695F77B0FBAF5F06A3C4DA4682142FBDBA3FC6A7D3378C3A4E6FC7692571A8CF3499237648299ADA7B3EFA9081DD1A095CDDF0DE101785CAE097D523ED94F3B235D920FB3E6E3FB5964AD7208E146B8D97DBA9E75AAA5C08C38B2219EC613DB9E761C71275C1DC27D0; ki_s=198467%3A1.0.0.0.2%3B209117%3A1.0.0.1.2; ki_t=1623248074564%3B1623248074564%3B1623279774455%3B1%3B3; GSESSIONID=c77c7a0d-1867-4568-a4e0-cd5bf4b6887f+1623318105007; cass=2; SameSite=None; JSESSIONID_JX_APP=473C677B452325B1FBA07617246F8FFE; gdsid=1623318105007:1623326588706:C20ED7DB38E549B547A277AC941FA931; at=SJE_btfP25_hvjPtNenJ1_8fOhCfnST9xM7NQPrANzc3mPAWrk8Ro1gfjJV-WUthrXJ7PKe8EAmT8KpxbHWO791WdhxFg5KepChUIDJjAlTszWVkPS1zSKTMOZQKk28x4oJm-0tL2dNDIVRKK7N_ZjBQbz9gduG0-Va7QNEiac86DXp9_yPhWJ7bCirb7oIaWEQCBattZ3qOXJ5pxSjT2VnTZ_CuKH8hewTJaPuj0LeXkYDjTDedBXWRdkBYwDMOHORQJjG7eJUCgOtdDjjtlHZRfpd1yoisCYY_KXW_YXzRbHjhJ57qVl_73Cn59qEKTIShVsno3umRvd1uB7qBI2-8SGsnZdSr0zPcbtcse_Hv9X0sxrSc8wORHvYh2g-qvxFCKI2rNTNIr_D0aWcXqhFEU5WEy03Hs23NYfrKKeCnNGT_7EsY57vjIrAzuj8FfDI972BiBPdgTgGPM04em6vEgG6cVOFptbUgiMl1fm70mAtRhLzKTfyqpJP-8pFnowysQBBttq13By6f-8Eq4SZSKOEazq6m-3VoEsAVr9f2MTd638L7llDkVLtNC7bAwRSP1NaVhXnR_Fpza6pSQfqD01yQ8-x_cLrBmdr_Dgy57shf1il4eW4ZIJb44yOsyfPLkQhkrB_hmeYfUcVi4iE2n5jdAAx9JeCuu8sb4kt-h_uUFs_VoW7wTizcBBScEuQKfdzLu7u8MlqBJHx18YVlUod2ikSzBG3YOgezEtpZEZQxa3PS1derQQWoXDOSIoksOrzrreUd3kSuc8GIk4dzxLZezzx2SdkYqqdHEtwGCtrjEatpQJNrpm9Rle44RYm817X2OtKjpdiE_lOK4PE7npqit778bvxIJBkX4RYKWllbb6VAehpfeesWT60Svf4; asst=1623326588.0; bs=K2GN96pYDLexo2E3vcOgkQ:tXpdAHPN6xZCEm0PyawbB0R50sdzY2Q5wevDru1pCWJ-4aUa-cwUs_QMdvs-IF5sRErP5ujsH5HxwwSNFcYsyl-O5m4ZXpzH4lAuKH4sZoA:6a5d4qXcQOC9Uid4mi-tIsar2_H-J6ikUSVfZ-9VjHM; __cf_bm=e701bd47bd983f5566f69bc4a7ff303a69616fe6-1623326589-1800-AfeapBuWul3WhwBUxDJo+wlNQ2vwrKFgncH3pOSR/ZFXpQuVQlMxgy2iOQirDFY6M0sSFbltkPEvxpkcFuHNBYk=; JSESSIONID=895E9865C44B76E3E2743B3C2F545FDC; AWSALB=duBYBHNJEPAolqZqkI7ZXurtQxtiHBs2Z43nFJzbtA1CC/KxDUS9lCZOzA36LHGP6SJAtw/04dGM4a7OMR/kvEJZCpdS7zVyPPOTVIHt+xOMTmtEhlxPIj+S55bTzSvf1taj6r0lkDVB6cgV3qntwOPVDMFDUCoQLTo51PsmVq9vcoUrxo+5uVGGv0B63lMviApfKGeuAwN/QgXQZaf04xhCdxe2W2xf/8sMWQqsNZ9sF/+SSt33JJmDk4n5B64=; AWSALBCORS=duBYBHNJEPAolqZqkI7ZXurtQxtiHBs2Z43nFJzbtA1CC/KxDUS9lCZOzA36LHGP6SJAtw/04dGM4a7OMR/kvEJZCpdS7zVyPPOTVIHt+xOMTmtEhlxPIj+S55bTzSvf1taj6r0lkDVB6cgV3qntwOPVDMFDUCoQLTo51PsmVq9vcoUrxo+5uVGGv0B63lMviApfKGeuAwN/QgXQZaf04xhCdxe2W2xf/8sMWQqsNZ9sF/+SSt33JJmDk4n5B64=; _ga=GA1.2.1343046783.1623246679; _dc_gtm_UA-2595786-1=1; _GA_Job_Session=true; _gat_UA-2595786-1=1; OptanonConsent=isIABGlobal=false&datestamp=Thu+Jun+10+2021+14%3A03%3A21+GMT%2B0200+(Central+European+Summer+Time)&version=6.8.0&hosts=&consentId=2053cc3e-86db-45c8-96fd-996656693761&interactionCount=2&landingPath=NotLandingPage&groups=C0001%3A1%2CC0003%3A1%2CC0002%3A1%2CC0004%3A1%2CC0017%3A1&geolocation=DE%3BBE&AwaitingReconsent=false; _ga_RC95PMVB3H=GS1.1.1623326595.9.1.1623326604.51',
}

def main():
    with open('output/page1a.json', 'r') as f:
        flattened = list(map(flatten_json, json.loads(f.read())))
        with open('output/page1a_flat.json', 'w') as f2:
            f2.write(json.dumps(flattened))

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
            jobTitleText
            locationName
            normalizedJobTitle
          }
          job {
              description
              discoverDate
              jobTitleText
              listingId
            }
          overview {
              ceo {
                name
                photoUrl
                __typename
              }
              id
              name
              shortName
              squareLogoUrl
              headquarters
              links {
                overviewUrl
                benefitsUrl
                photosUrl
                reviewsUrl
                salariesUrl
                __typename
              }
              primaryIndustry {
                industryId
                industryName
                sectorName
                sectorId
                __typename
              }
              ratings {
                compensationAndBenefitsRating
                cultureAndValuesRating
                careerOpportunitiesRating
                workLifeBalanceRating
                __typename
              }
              overview {
                description
                __typename
              }
              revenue
              size
              type
              website
              yearFounded
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

def flatten_json(nested_json, exclude=['']):
    """Flatten json object with nested keys into a single level.
        Credit: https://stackoverflow.com/a/57334325/1751834
        Args:
            nested_json: A nested json object.
            exclude: Keys to exclude from output.
        Returns:
            The flattened json object if successful, None otherwise.

    """
    out = {}

    def flatten(x, name='', exclude=exclude):
        if type(x) is dict:
            for a in x:
                if a not in exclude: flatten(x[a], name + a + '_')
        elif type(x) is list:
            i = 0
            for a in x:
                flatten(a, name + str(i) + '_')
                i += 1
        else:
            out[name[:-1]] = x

    flatten(nested_json)
    return out

def scrape():
    #html = get_page(2)
    with open('output/myOutFile.html','r') as f:
        html = f.read()
        jobids = jobids_from_page(html)
        with open('output/page1a.json', 'w') as f2:
            jobs_arr = list(map(job_info, jobids))
            f2.write(json.dumps(jobs_arr))

if __name__ == "__main__":
    main()
