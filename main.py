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
    'gd-csrf-token': 'qbZ7acvPDn8NAXK6NhAyfg:1gdpXQSYnmjya-dkjlv_nhNEK8R5h_F7mQsuspkl2Ls17Ifbzx7NDfqmmDy-jWRxeLyQ4B9Jni1EvSLS-dPH1A:P8XM_8QOyRX9CIPUJ3dV5UpevV_p4FZDPqFnNpHI9EM',
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
    'cookie': 'gdId=c77c7a0d-1867-4568-a4e0-cd5bf4b6887f; trs=https%3A%2F%2Fwww.google.com%2F:SEO:SEO:2021-06-09+06%3A51%3A15.487:undefined:undefined; _gid=GA1.2.1259183532.1623246679; G_ENABLED_IDPS=google; fpvc=1; OptanonAlertBoxClosed=2021-06-09T13:51:30.439Z; _optionalConsent=true; _gcl_au=1.1.1658861872.1623246691; _fbp=fb.1.1623246690902.370312596; __gads=ID=ebaab3dacb72eeeb:T=1623246691:S=ALNI_MYXvefDJxK8vgqBBKG0FsnNYffmIQ; ht=%7B%22quantcast%22%3A%5B%22D%22%5D%7D; indeedCtk=1f7ohumvj3oah001; ki_r=; ki_u=243d60fe-cc57-5525-e71e-90a3; JSESSIONID_UP_APP=4E1BA8258E1EFBE77870070E6CAE60BE; uc=44095BCBCAA84CA8D083AA33D0C199178AE8F35E9AD7F8C96075743956155E8B7639D64B8B3F63695F77B0FBAF5F06A3C4DA4682142FBDBA3FC6A7D3378C3A4E6FC7692571A8CF3499237648299ADA7B3EFA9081DD1A095CDDF0DE101785CAE097D523ED94F3B235D920FB3E6E3FB5964AD7208E146B8D97DBA9E75AAA5C08C38B2219EC613DB9E761C71275C1DC27D0; JSESSIONID_KYWI_APP=CC50061AF0B7C4B63A0D49BF1F82B8FF; ki_t=1623248074564%3B1623248074564%3B1623256439526%3B1%3B2; ki_s=198467%3A1.0.0.0.2%3B209117%3A1.0.0.1.2; asst=1623267026.0; GSESSIONID=c77c7a0d-1867-4568-a4e0-cd5bf4b6887f+1623246675455; cass=2; JSESSIONID=D719434186B4589183B0CE950D62D36B; _ga=GA1.2.1343046783.1623246679; OptanonConsent=isIABGlobal=false&datestamp=Wed+Jun+09+2021+22%3A05%3A43+GMT%2B0200+(Central+European+Summer+Time)&version=6.8.0&hosts=&consentId=2053cc3e-86db-45c8-96fd-996656693761&interactionCount=2&landingPath=NotLandingPage&groups=C0001%3A1%2CC0003%3A1%2CC0002%3A1%2CC0004%3A1%2CC0017%3A1&geolocation=DE%3BBE&AwaitingReconsent=false; __cf_bm=67156806a2b9273cb13a180ce9ca44d73c96e755-1623274350-1800-ARtVGJTdj+n3u7Y5F7JnCrRR1VKxI4/wJ6zjCyKut2915vvbYU+WGMkxvi7iwj1tjupuGQ/ZKF3cSNUjvUjc44s=; _gat_UA-2595786-1=1; AWSALB=2PKnDS+ztHHr+HdHocQr09oyVDWhas0m2XPulL1sAnn7WwBne4n9lEnp8Zw0+LdsphvymwwCSmgr+hCoSD17ykgG3WL5GdjkcdfA9OQxMohdC1VzXPAmFq8gANNdGLfUQD/jCV2PAPORQZwTggi6BxXiqw/98VMV4EJKaE+QhAySnP+N5wcItT8swyUvtSV8j+ChInT0xoJsx9U8SGEjxzbJ+hwFUAo/Fk1D88j1PqKp8LNSDE0U80ithVkw3F4=; AWSALBCORS=2PKnDS+ztHHr+HdHocQr09oyVDWhas0m2XPulL1sAnn7WwBne4n9lEnp8Zw0+LdsphvymwwCSmgr+hCoSD17ykgG3WL5GdjkcdfA9OQxMohdC1VzXPAmFq8gANNdGLfUQD/jCV2PAPORQZwTggi6BxXiqw/98VMV4EJKaE+QhAySnP+N5wcItT8swyUvtSV8j+ChInT0xoJsx9U8SGEjxzbJ+hwFUAo/Fk1D88j1PqKp8LNSDE0U80ithVkw3F4=; ADRUM_BTa=R:0|g:e57e9ff0-2e16-494f-ade4-b9f0f262a4b0|n:glassdoor_17d346a0-2ec1-4454-86b0-73b3b787aee9; SameSite=None; JSESSIONID_JX_APP=75ABBF3AAE49501BDCC549978BF4D3DD; ADRUM_BT1=R:0|i:1188649|e:118|d:149; ADRUM_BT2=R:0|i:1188650|e:168; gdsid=1623246675455:1623274359488:B73042C81AF9F61D4372EC36926729D2; at=PUFBo_R2j_fzLMA96bdFN9V6fSoK9HB2c8iTTSEx4dSYNNb3l0fl12hBOY-UMTCYDoQu4_w0gpEWVnI-KM3Okto9zH8-v2wvzmq6quQ944VWxwJrdOK--5B_FuBU9gy0Pb2I1Vepwifri104q_HSWXzsb4gH0KxzyHs267mbcE1VH9QDRACVIyVmBLVVjCigBc3PHhNUr3OhyvRlb-g1V0kO_Igg3CL_m0fZofCacetp7v8QpQ_zHHioQL5bcc2O6NpmvvAH7m4n4KTogRm0Znl2b0e_owh42nBPVcu1dyFlXcRj8zSR3b5j6Ju-Kxp16C3ZanUhJyUck-l-FKnJlszCnBAca5P8eEyCvOqqHfSoLqpE76rhuFS9SUU8aE5bDSIH1ckN2v5U2rO4W-MT4miBuCxg6y_4pgcrfwdQ_MJ-JLe8ggD1OdS1QWvs-YtXasPVt8HZ4SiMgsKJdjUahHLmdL-I3ubdhqv0hOxnemsjyaDu4IG67DX6dzcMM65XQW7XhCXx8m8g9v7Ptu3Qx0ezThtDXlsxJ3HiT5FQ7oUCWrSsy4EpMCiPcSQiOkT55Cj6DHcFoS1ZjMTJT9Wdt4zfEFAa4joRuaM_L7GRC_aHmuKtHN5UVdyv9ocWyNmnxwoMcBnzhy2h3t61JUIcPef_lxTAOTT1g1xAT8PgeSxu-_skUClRCfnmRc4Xze-0IxJgYbXEP3jDY5emMILOXK3NOeaKThpty1PvnOoIaYt6wUXEGT_p-LMRYQFBmuCY4qbowegzCGf3FUWmutmnZpNjH4XSGrVuSNksB27rWle-gXH9iQRSv7U0wV0POHfgKNzeuSbUujKmn9yXKjz3lewQsJszDp1p-Jgyvus8cdTsQOVbnX24rmen06JhdO9f9Pk; bs=AKYIHM8Aa_wXWlXjZVT8Kg:wlzoKGl0qEkqG5Sbh5cYQDb8GJD3SL133wZo9e-c4giGfl2MafGIvyZifc8ILYif7piYKxT7iloZV_Jfhctu7B26Rq6GH9ef3eeCuntVVhY:rJ-AVkig9swPl4mtiMmw9Rfnx_kF9351VKWhXlSwbmM; _ga_RC95PMVB3H=GS1.1.1623274352.5.1.1623274364.48',
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
    variables = {'enableReviewSummary':False, 'jl':4074701403, 'queryString': 'pos=101&ao=1044074&s=149&guid=00000179f2b11edb8d68c1103c7985a9&src=GD_JOB_AD&t=SRFJ&vt=w&uido=E72EB9FF023BC985E69A0D4700D2593A&cs=1_73c42787&cb=1623274365290&jobListingId=4074701403' }
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
          employerBenefits {
            benefitsOverview {
              benefitsHighlights {
                benefit {
                  commentCount
                  icon
                  name
                  __typename
                }
                highlightPhrase
                __typename
              }
              overallBenefitRating
              employerBenefitSummary {
                comment
                __typename
              }
              __typename
            }
            benefitReviews {
              benefitComments {
                id
                comment
                __typename
              }
              cityName
              createDate
              currentJob
              rating
              stateName
              userEnteredJobTitle
              __typename
            }
            numReviews
            __typename
          }
          employerContent {
            featuredVideoLink
            managedContent {
              id
              type
              title
              body
              captions
              photos
              videos
              __typename
            }
            diversityContent {
              goals {
                id
                workPopulation
                underRepresentedGroup
                currentMetrics
                currentMetricsDate
                representationGoalMetrics
                representationGoalMetricsDate
                __typename
              }
              __typename
            }
            __typename
          }
          employerAttributes {
            attributes {
              attributeName
              attributeValue
              __typename
            }
            __typename
          }
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
          similarJobs {
            relatedJobTitle
            careerUrl
            __typename
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
          map {
            address
            country
            employer {
              id
              name
              __typename
            }
            locationName
            postalCode
            __typename
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
          photos {
            photos {
              caption
              photoId
              photoId2x
              photoLink
              photoUrl
              photoUrl2x
              __typename
            }
            __typename
          }
          rating {
            ceoApproval
            ceoRatingsCount
            employer {
              name
              __typename
            }
            recommendToFriend
            starRating
            __typename
          }
          reviews {
            reviews {
              advice
              cons
              countHelpful
              employerResponses {
                response
                responseDateTime
                userJobTitle
                __typename
              }
              employmentStatus
              featured
              isCurrentJob
              jobTitle {
                text
                __typename
              }
              lengthOfEmployment
              pros
              ratingBusinessOutlook
              ratingCareerOpportunities
              ratingCeo
              ratingCompensationAndBenefits
              ratingCultureAndValues
              ratingOverall
              ratingRecommendToFriend
              ratingSeniorLeadership
              ratingWorkLifeBalance
              reviewDateTime
              reviewId
              summary
              __typename
            }
            __typename
          }
          salary {
            currency {
              code
              numOfDecimals
              negativeFormat
              positiveFormat
              symbol
              __typename
            }
            lastSalaryDate
            salaries {
              count
              maxBasePay
              medianBasePay
              minBasePay
              jobTitle {
                id
                text
                __typename
              }
              payPeriod
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
