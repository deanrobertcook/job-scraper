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
    'gd-csrf-token': 'M2ck4KmAke_mJsEoP8vhJg:lfGZxlvjqEQZg5XQQy7YzUFgC0HGGP0rPaLA8zZBP-HL0tWFbDiRX9dbKeP62wrdbYdKsLtSuYDBaDwB70BNQQ:5UJfmZvmVf66A3LChc0DMCwtqhF2oGUNW4fKU5-y2Z8',
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
    'cookie': 'gdId=c77c7a0d-1867-4568-a4e0-cd5bf4b6887f; trs=https%3A%2F%2Fwww.google.com%2F:SEO:SEO:2021-06-09+06%3A51%3A15.487:undefined:undefined; _gid=GA1.2.1259183532.1623246679; G_ENABLED_IDPS=google; fpvc=1; OptanonAlertBoxClosed=2021-06-09T13:51:30.439Z; _optionalConsent=true; _gcl_au=1.1.1658861872.1623246691; _fbp=fb.1.1623246690902.370312596; __gads=ID=ebaab3dacb72eeeb:T=1623246691:S=ALNI_MYXvefDJxK8vgqBBKG0FsnNYffmIQ; ht=%7B%22quantcast%22%3A%5B%22D%22%5D%7D; indeedCtk=1f7ohumvj3oah001; ki_r=; ki_u=243d60fe-cc57-5525-e71e-90a3; uc=44095BCBCAA84CA8D083AA33D0C199178AE8F35E9AD7F8C96075743956155E8B7639D64B8B3F63695F77B0FBAF5F06A3C4DA4682142FBDBA3FC6A7D3378C3A4E6FC7692571A8CF3499237648299ADA7B3EFA9081DD1A095CDDF0DE101785CAE097D523ED94F3B235D920FB3E6E3FB5964AD7208E146B8D97DBA9E75AAA5C08C38B2219EC613DB9E761C71275C1DC27D0; ki_s=198467%3A1.0.0.0.2%3B209117%3A1.0.0.1.2; ki_t=1623248074564%3B1623248074564%3B1623279774455%3B1%3B3; JSESSIONID_JX_APP=AACDB58B496DD272B52EF9D4DCC2205C; GSESSIONID=c77c7a0d-1867-4568-a4e0-cd5bf4b6887f+1623318105007; cass=2; asst=1623318104.0; JSESSIONID=B48BD4E7F084756BBC1FE3CF72F4A022; _ga=GA1.2.1343046783.1623246679; OptanonConsent=isIABGlobal=false&datestamp=Thu+Jun+10+2021+12%3A08%3A14+GMT%2B0200+(Central+European+Summer+Time)&version=6.8.0&hosts=&consentId=2053cc3e-86db-45c8-96fd-996656693761&interactionCount=2&landingPath=NotLandingPage&groups=C0001%3A1%2CC0003%3A1%2CC0002%3A1%2CC0004%3A1%2CC0017%3A1&geolocation=DE%3BBE&AwaitingReconsent=false; AWSALB=FWIqStuGFofLLvNDk4WQsHcvBFnYQBdfWjQtHDqycOQxEmnE5MKRbVxknhWlq66S+6h+RfyFiqfuvFFPlkk9Evm+omsS826lmkv6doycgGYwVp2NAhB0xX+wT3aFXs6XRLBbQtndB/q0AceDDuXemTxUbrtCQ2Qw2G2MUKVolJ0dLI2c+vsa+NN+UQ+wGrJ71UtzLA63yCPDFLWiQVy2VygT08vkjqW4Ab0IlJ7UoHcoWbGg9/VRIR6dmwr58aE=; AWSALBCORS=FWIqStuGFofLLvNDk4WQsHcvBFnYQBdfWjQtHDqycOQxEmnE5MKRbVxknhWlq66S+6h+RfyFiqfuvFFPlkk9Evm+omsS826lmkv6doycgGYwVp2NAhB0xX+wT3aFXs6XRLBbQtndB/q0AceDDuXemTxUbrtCQ2Qw2G2MUKVolJ0dLI2c+vsa+NN+UQ+wGrJ71UtzLA63yCPDFLWiQVy2VygT08vkjqW4Ab0IlJ7UoHcoWbGg9/VRIR6dmwr58aE=; ADRUM_BTa=R:0|g:9c3557d5-5202-4049-a6c4-3996f682b920|n:glassdoor_17d346a0-2ec1-4454-86b0-73b3b787aee9; SameSite=None; ADRUM_BT1=R:0|i:1188649|e:57|d:20; ADRUM_BT2=R:0|i:1188650|e:172; gdsid=1623318105007:1623321909743:4EC81BB5281DFC760B2DC09071AC2C8A; at=7dC2i9uZEoYgh0G8RGIUfzmc0GOOrujYAdQqL6zVSoTn5DoH_DLaNnAWgE_MXSLcHcxGCz9tCOCz7wof5V5WJ3VaahYLbtZoB35uCi6opqB5fw6KDJ4_epsD2w13HEiaLvNCQI0nXOZXSBf5NPE3xFATUV3s5-jnqCC0lmwvkQS0104HxoRtsNtQ8MEw_SaC8mcb8aTdbxV0Swl6zX9Nv30Q_SDFyuOML5B2XtbfOWgIX5bKs5teKoqoRtucljtmYhKvbT4yV63FoipSH5PB9zCNF0rhwtqJ2g3fTWdgsI8CjWQpfRgif_Vyp3seLWWaEkYmCIDTAmyLFPxXSzzlpmPfVeEFTzX2_WA8uZo6Dv4LpBQ2GIrJFCc-SbR78AOEFrW5Pova0MhZMxnESZN8agj5IS5mQFvqDi_xnqBEDY417gy5vqGusb9RVHVrXKCk22jZ-loN3U5ShAty3YPQgnV7-QYCXraJawDGKqXIoU5aUJerZeDDUpvo5914_VekSrPHccAGY0fXCJfr2irYfAVemK7HXBdjqc-Bw_5jBnJruO5fSKeHLKdtHjpbIgyPLrOiBual0dzwlBn1mBdn-dwjoj5gM6SGrbYkwS93zNpvSOorlqIE-QpR67EqvNfwzoyPw1pr8D_N83Etq-JOiGXK6plIX7uzxEjYx7c4hbR0thDsV3prRQ88lUImOWedOsK5V56t6Edx5bv5GRVBwubcNXjrRPdt-T_oJtXyybaBid1mmWkTFdbInDEexXIi3e9zDs9mNCVYyjWA1Clqu7Yeyc1lwKWPETIJxJ4bASlqCP6s6R2bmP8P7Vv2gJlV44LMmJlzRaqtgDQZA8koA4kp02XR15uILVilC279BmujCkG9j44X9teOyryyUUz3Eko; bs=eQeolFHQJ-0ruSYEaAf7Mw:manry7VeWqznl7QxgxC5U0xhXR28MbOsjXMnWmuxINv4SYYStmQ6F_GvgND5HweYTqQnWLpuVuDZysvceDk9eL_o37BDOGqZqcVUP-VKUIQ:di9RTo0xB9S0dzLwPqk_WfgFXoPFv0kBpK_t_tfrASc; __cf_bm=44ea7f723bcc8e43a12c0ed2b521a56ff109fe1e-1623321910-1800-AZxY0msuDXrfV6/ZMiAzgbLnUDU8kjNByTASGaWonr5gHmbuekXKWmn/+z6MFSZTY9GBHJEuylHUBPcTXT6phhM=; _ga_RC95PMVB3H=GS1.1.1623321913.8.0.1623321913.60',
}

def main():
    pass

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
    html = get_page(2)
    jobids = jobids_from_page(html)
    out = open('output/page2.json', 'w')
    jobs_arr = list(map(job_info, jobids))
    out.write(json.dumps(jobs_arr))
    out.close()

if __name__ == "__main__":
    f = open('output/page2.json', 'r')
    flattened = list(map(flatten_json, json.loads(f.read())))
    f_out = open('output/page2_flat.json', 'w')
    f_out.write(json.dumps(flattened))
    f_out.close()
    f.close()
