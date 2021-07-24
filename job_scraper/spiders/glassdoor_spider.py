import scrapy
from scrapy.shell import inspect_response

#TODO allow different search terms
BASE_URL = 'https://www.glassdoor.de/Job/berlin-data-science-jobs-SRCH_IL.0,6_IC2622109_KO7,19_IP{}.htm'
BASE_URL = 'https://www.glassdoor.de/Job/berlin-data-science-jobs-SRCH_IL.0,6_IC2622109_KO7,19.htm'

class GlassdoorSpider(scrapy.Spider):
    name = 'glassdoor'

    start_urls = [
        'https://www.glassdoor.de/Job/berlin-data-science-jobs-SRCH_IL.0,6_IC2622109_KO7,19.htm'
    ]

    def parse(self, response, **kwargs):
        inspect_response(response, self)

        

        for li in response.css('li.react-job-listing'):
            yield {
                'glassdoor_id': li.attrib['data-id'],
                'job_title': li.attrib['data-normalize-job-title']
            }
            
            