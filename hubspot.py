import requests
import requests_cache
import logging
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import datetime, json, string

# Config
requests_cache.install_cache()
logging.basicConfig(level=logging.INFO,format='[%(asctime)s] %(message)s', datefmt='%d-%b-%y %H:%M:%S')
GOOGLESHEET = ''
HAPIKEY = ''
EXPORTABLES = {
	'deals': True,
	'engagements': True
}

def _unix2Date(unixString):
	date = datetime.datetime.fromtimestamp(int(unixString/1000)).strftime('%Y-%m-%d')
	return date

def _calculateA1Notation(dataTable):
	letter = string.ascii_lowercase[len(dataTable[0])-1]
	number = str(len(dataTable))
	return letter + number

def updateGoogleSheets(targetSheet,table):
	scope = ['https://spreadsheets.google.com/feeds']
	targetURL = GOOGLESHEET
	creds = ServiceAccountCredentials.from_json_keyfile_name('modl-sheets-access.json', scope)
	client = gspread.authorize(creds)
	sheet = client.open_by_url(targetURL)
	worksheet = sheet.worksheet(targetSheet)
	sheetEnd = _calculateA1Notation(table)
	worksheet.update('A1:{}'.format(sheetEnd), table)

def _getContacts(hapikey, contactIDs):
	contacts = []
	for i in contactIDs:
		r = requests.get('https://api.hubapi.com/contacts/v1/contact/vid/{}/profile?hapikey={}'.format(i, hapikey))
		response = json.loads(r.text)
		firstname = response['properties'].get('firstname',{}).get('value')
		lastname = response['properties'].get('lastname',{}).get('value')
		contact = {
			'name' : f"{firstname} {lastname}",
			'company' : response.get('associated-company',{}).get('properties',{}).get('name',{}).get('value','Unknown'),
			'lifecyclestage' : response['properties'].get('lifecyclestage',{}).get('value'),
		}
		contacts.append(contact)
	return contacts

def _getCompanies(hapikey, companyIDs):
	companies = []
	if 2846783068 in companyIDs: companyIDs.remove(2846783068) #remove modl.api
	for i in companyIDs:
		r = requests.get('https://api.hubapi.com/companies/v2/companies/{}?hapikey={}'.format(i, hapikey))
		properties = json.loads(r.text)['properties']
		company = {
			'name' : properties['name']['value'],
			'website' : properties['domain']['value'],
			'description' : properties.get('description',{}).get('value'),
			'hs_total_deal_value' : properties.get('hs_total_deal_value',{}).get('value'),
			'type' : properties.get('type',{}).get('value','')
		}
		companies.append(company)
	return companies

def _getDeals(hapikey):
	url = "https://api.hubapi.com/crm/v3/objects/deals"
	queryString = {
		"limit":"100",
		"hapikey":hapikey,
		"properties":[
			"dealname",
			"dealstage",
			"amount",
			"days_to_close",
			"closedate",
			"pipeline",
			"hs_date_entered_appointmentscheduled",
			"hs_date_entered_qualifiedtobuy",
			"hs_date_entered_presentationscheduled",
			"hs_date_entered_decisionmakerboughtin",
			"hs_date_entered_contractsent",
			"hs_date_entered_closedlost",
			"hs_date_entered_closedwon",
		]
	}
	headers = {'accept': 'application/json'}
	paging = True
	dealList = []
	while paging:
		r = requests.request("GET", url, headers=headers, params=queryString)
		payload = json.loads(r.text)
		for d in payload['results']:
			dealList.append(d['properties'])
		if 'paging' in payload:
			queryString['after'] = payload['paging']['next']['after']
		else:
			paging = False
		logging.info(f'Found {len(dealList)} deals')
	return dealList

def exportDealsTable(hapikey):
	logging.warning('Retrieving deals...')
	table = [[
		'Deal Name',
		'Deal Stage',
		'Days to Close',
		'Amount',
		'Pipeline',
		'Create Date',
		'First meeting', #Appt scheduled
		'Qualified',
		'Quote sent', #Presentation scheduled
		'Negotiations', #Decision maker
		'Contract sent',
		'Closed (Lost)',
		'Closed (Won)',
		'Close Date'
	]]
	for deal in _getDeals(hapikey):
		row = [
			deal['dealname'],
			deal['dealstage'],
			deal['days_to_close'],
			deal['amount'],
			deal['pipeline'],
			str(deal['createdate'])[:10],
			str(deal['hs_date_entered_appointmentscheduled'])[:10],
			str(deal['hs_date_entered_qualifiedtobuy'])[:10],
			str(deal['hs_date_entered_presentationscheduled'])[:10],
			str(deal['hs_date_entered_decisionmakerboughtin'])[:10],
			str(deal['hs_date_entered_contractsent'])[:10],
			str(deal['hs_date_entered_closedlost'])[:10],
			str(deal['hs_date_entered_closedwon'])[:10],
			str(deal['closedate'])[:10]
		]
		table.append(row)
	logging.warning('Uploading deals...')
	updateGoogleSheets('Deals',table)
	return

def _parseEngagement(engType, metadata):
	if engType == 'NOTE':
		content = metadata.get('body')
	elif 'EMAIL' in engType:
		content = f"{metadata.get('subject','BLANK')} - {metadata.get('text', metadata.get('html'))}"
	elif engType == 'TASK':
		content = f"{metadata.get('subject')} - {metadata.get('body')}"
	elif engType == 'MEETING':
		content = f"{metadata.get('title')} - {metadata.get('body')}"
	elif engType == 'CALL':
		content = f"{metadata.get('body')}"
	else:
		content = str(metadata)
	return content[:1000] # arbitrary limit
		
def _getEngagements(hapikey):
	url = "https://api.hubapi.com/engagements/v1/engagements/paged"
	queryString = {"limit":"250","hapikey":hapikey}
	headers = {'accept': 'application/json'}
	paging = True
	engList = []
	recordCount = 0
	while paging:
		r = requests.request("GET", url, headers=headers, params=queryString)
		payload = json.loads(r.text)
		for e in payload['results']:
			engList.append(e)
		if payload['hasMore'] == True:
			queryString['offset'] = payload['offset']
		else:
			paging = False
		logging.info(f'Found {len(engList)} engagements')
	return engList

def exportEngTable(hapikey):
	table = [['ID','Engagement Type','Timestamp','Company','Company Type','Attendees','Information']]
	logging.warning('Retrieving engagements...')
	engagements = _getEngagements(hapikey)
	logging.warning('Formatting engagements...')
	for eng in engagements:
		companies = _getCompanies(hapikey, eng['associations']['companyIds'])
		contacts = _getContacts(hapikey, eng['associations']['contactIds'])
		row = [
			eng['engagement']['id'],
			eng['engagement']['type'],
			_unix2Date(eng['engagement']['timestamp']),		
			', '.join([c['name'] for c in companies]),
			', '.join([c['type'] for c in companies]),
			', '.join([f"{c['name']} - {c['company']}" for c in contacts]),
			_parseEngagement(eng['engagement']['type'], eng['metadata'])
		]
		table.append(row)
	logging.warning('Uploading engagements...')
	updateGoogleSheets('Engagements',table)
	return table


if __name__ == '__main__':
	logging.warning('Beginning hubspot export...')
	if EXPORTABLES['deals']: exportDealsTable(HAPIKEY)
	if EXPORTABLES['engagements']: exportEngTable(HAPIKEY)
	logging.warning(f"Exported {', '.join(k for k in EXPORTABLES.keys() if EXPORTABLES[k])} to {GOOGLESHEET}")