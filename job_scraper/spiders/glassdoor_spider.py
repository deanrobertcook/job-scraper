import scrapy
import json
from http.cookies import SimpleCookie

# TODO allow different search terms
BASE_URL = 'https://www.glassdoor.de/Job/berlin-data-science-jobs-SRCH_IL.0,6_IC2622109_KO7,19_IP{}.htm'

GRAPHQL_URL = 'https://www.glassdoor.de/graph'

# The only headers actually needed are 'gd-csrf-token', 'cookie', 'user-agent' and 'content-type',
# however, the latter two are handled automatically by Scrapy and the GraphQlRequest.
# I'll leave the rest in so that the request looks more authentic, plus it makes the copy and paste easier.
# To get the headers: inspect the network sources on chrome and copy the curl request
# Then go to the curl-to-python converter and paste it in there. The headers appear as
# a python dict on the side.
HEADERS = {
    'authority': 'www.glassdoor.de',
    'sec-ch-ua': '" Not;A Brand";v="99", "Google Chrome";v="91", "Chromium";v="91"',
    'apollographql-client-name': 'job-search',
    'dnt': '1',
    'gd-csrf-token': '83Gwn-2ndeB4q3JCRqJoRQ:_Xxrxa-YkvUR_V8MnJePlmvc4URgNu1YB9uAP75YNtoA6v8L13i_fetrt7wmnyX0el0Ha5Awwoq8dBktBOT3qA:s7ZL2fim-PVX7SU-FGpb33haIcyoryqH_LVAkOB-unw',
    'at': 'undefined',
    'sec-ch-ua-mobile': '?0',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36',
    'content-type': 'application/json',
    'accept': '*/*',
    'apollographql-client-version': '0.11.25',
    'origin': 'https://www.glassdoor.de',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-mode': 'cors',
    'sec-fetch-dest': 'empty',
    'referer': 'https://www.glassdoor.de/',
    'accept-language': 'de-DE,de;q=0.9',
    'cookie': 'gdId=cbd08604-ac5d-4a9d-9099-9f927ed8104a; trs=direct:direct:direct:2021-07-24+11%3A52%3A07.346:undefined:undefined; indeedCtk=1fbctofgkn58p802; _gid=GA1.2.782148673.1627152731; OptanonAlertBoxClosed=2021-07-24T18:52:28.871Z; _optionalConsent=true; _gcl_au=1.1.370839451.1627152749; _fbp=fb.1.1627152749421.813588567; __gads=ID=f76e0adf55c9693c-226d94ec8bc80086:T=1627159124:S=ALNI_MaLvF1pZ9SB71Tvc7K__E2vEvaYtw; ki_t=1627159125263%3B1627159125263%3B1627159125263%3B1%3B1; ki_s=209117%3A1.0.0.0.2; GSESSIONID=cbd08604-ac5d-4a9d-9099-9f927ed8104a+1627198395799; cass=2; JSESSIONID_JX_APP=758850EEBD16B4C865A3102AD9D7454B; JSESSIONID=B795D999A4E154E52538E86F1057C7AC; _ga=GA1.2.2147455236.1627152730; OptanonConsent=isIABGlobal=false&datestamp=Sun+Jul+25+2021+10%3A47%3A50+GMT%2B0200+(Mitteleurop%C3%A4ische+Sommerzeit)&version=6.8.0&hosts=&consentId=205b381b-92a6-4d87-87ed-f958d8e8dca5&interactionCount=1&landingPath=NotLandingPage&groups=C0001%3A1%2CC0003%3A1%2CC0002%3A1%2CC0004%3A1%2CC0017%3A1&geolocation=DE%3BBE&AwaitingReconsent=false; _ga_RC95PMVB3H=GS1.1.1627202868.4.1.1627202872.56; AWSALB=A5lh3+bRyh9pLUBbzxowQ6Q13iTY1+BN3M3Haxp1b0z1MxtR+nMC2GgCB6DMcm97RLEM2TG9Tl6W2cFdwVgyxv2kQqHFIuhhqiZkYX5R70+DaRweTBrKdCFAhgEn73uiA1HbFdTSE/yl+i2saeEeupUPhay5eNmxpQryl/rWK2oxkN+vIO0dCnI9WMxxSg==; AWSALBCORS=A5lh3+bRyh9pLUBbzxowQ6Q13iTY1+BN3M3Haxp1b0z1MxtR+nMC2GgCB6DMcm97RLEM2TG9Tl6W2cFdwVgyxv2kQqHFIuhhqiZkYX5R70+DaRweTBrKdCFAhgEn73uiA1HbFdTSE/yl+i2saeEeupUPhay5eNmxpQryl/rWK2oxkN+vIO0dCnI9WMxxSg==; ADRUM_BTa=R:0|g:6ca20ae3-ac81-4de7-b5ec-6039da8c4791|n:glassdoor_17d346a0-2ec1-4454-86b0-73b3b787aee9; SameSite=None; ADRUM_BT1=R:0|i:1188649|e:20|d:4; ADRUM_BT2=R:0|i:1188650|e:244; gdsid=1627198395799:1627206554815:7D5F7771A8C66FF3EB9535FBC50AAF3E; asst=1627206554.0; bs=m1xPwcX871ES-KRqZQOwIA:02y8sljjnn0CSFFjG2X4JDWUGjh9WApFQFq5ONIa7_J35A4N9u9IOIg2jd4lw0M-ORROG5qwYEbXC0JShLgSYJDxuYQLhB8VBk3yqhu5Uyw:Jkk2sCUC67SqFnYMJj9tyiJSi-5y8QzfRk9AKs5nNqQ; __cf_bm=ff6832b0f0b7b09d5ff9346eea41c21c832d8c3a-1627206555-1800-AUMrmc/WpktNuI+s+ERxjk3/TJqwIRdtO167PNSo+S1yijsQ400U3+gDcfqw78CQuA+h2R9zk9acEZl7u+N8I8A=',
}

class GlassdoorSpider(scrapy.Spider):
    name = 'glassdoor'

    def start_requests(self):
        page = 1
        yield scrapy.Request(BASE_URL.format(page), callback=self.parse, meta={'page': page})
            

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Cookies placed manually in the header seem to get overridden by the CookiesMiddleware
        # So we need to put them back into the Request.cookies field as a proper dict.
        cookie = SimpleCookie()
        cookie.load(HEADERS['cookie'])
        self.cookies = {}
        for key, morsel in cookie.items():
            self.cookies[key] = morsel.value

    def parse(self, response, **kwargs):
        for id in response.css('li.react-job-listing::attr(data-id)').getall():
            variables = {'enableReviewSummary': False, 'jl': id,
                         'queryString': 'jobListingId={}'.format(id)}
            yield GraphQlRequest(GRAPHQL_URL, self.parse, QUERY, variables=variables,
                                 headers=HEADERS, cookies=self.cookies)

        #Now try and parse individual graphql(json) requests
        try:
            js = json.loads(response.text)
            #TODO - include scraped time and job post date (if applicable)
            yield {
                'company_name': js['data']['jobView']['header']['employer']['name'],
                'job_title': js['data']['jobView']['header']['jobTitleText'],
                'job_description': js['data']['jobView']['job']['description'],
            }
        except ValueError:
            #Not valid json, do nothing
            pass

        # Look for next pages:
        if response.css('div#FooterPageNav a[data-test="pagination-next"]::attr(href)').get() is not None:
            page = (response.meta['page'] + 1)
            yield scrapy.Request(BASE_URL.format(page), callback=self.parse, meta={'page': page})

#TODO move this somewhere more generic - will come in handy for other graphql operations
class GraphQlRequest(scrapy.Request):

    # TODO attribute python_graphql_client for this method
    def __request_body(
        self, query: str, variables: dict = None, operation_name: str = None
    ) -> dict:
        json = {"query": query}
        if variables:
            json["variables"] = variables
        if operation_name:
            json["operationName"] = operation_name
        return json

    def __init__(self, url, callback, query: str, variables: dict = None, headers: dict = None,
                 operation_name: str = None, cookies: dict = {}, errback=None):
        if 'content-type' not in headers:
            headers['content-type'] = 'application/json'
        
        request_body = json.dumps(self.__request_body(
            query=query, variables=variables, operation_name=operation_name
        ))

        super().__init__(url, callback=callback, method='POST', headers=headers, body=request_body,
                         errback=errback, cookies=cookies)


QUERY = """
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
        locationName
        normalizedJobTitle
        jobTitleText
    }
    job {
        description
        listingId
    }
}
"""

