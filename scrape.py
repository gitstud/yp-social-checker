import csv
import requests
from bs4 import BeautifulSoup

# installation:
# $virtualenv env
# $pip install requests
# $pip install bs4
# $source env/bin/activate
# enter locations to be scraped in the locations list (format: 'this+has+spaces')
# $python scrape.py

def facebook(name):
	form = name.split(' ')
	formal = ''.join(form)
	facebook_url = 'https://www.facebook.com/' + formal + '/'
	facebook_page = requests.get(facebook_url)
	if facebook_page.status_code == 404:
		return False
	elif facebook_page.status_code == 200:
		return True

def instagram(name):
	form = name.split(' ')
	formal = ''.join(form)
	instagram_url = 'https://www.instagram.com/' + formal + '/'
	instagram_page = requests.get(instagram_url)
	if instagram_page.status_code == 404:
		return False
	elif instagram_page.status_code == 200:
		return True

def yelp(name, location):
	name_form = name.split(' ')
	location_form = location.split(' ')
	form = name_form + location_form
	formal = '-'.join(form)
	yelp_url = 'https://www.yelp.com/biz/' + formal + '/'
	yelp_page = requests.get(yelp_url)
	if yelp_page.status_code == 404:
		return False
	elif yelp_page.status_code == 200:
		return True

def pinterest(name):
	form = name.split(' ')
	formal = ''.join(form)
	pinterest_url = 'https://www.pinterest.com/' + formal + '/'
	pinterest_page = requests.get(pinterest_url)
	try:
		soup = BeautifulSoup(pinterest_page, 'html.parser')
		search = soup.find('h3', attrs={'class': 'antialiased bold mb0 mt0 sans-serif display-md _2d break-word'})
		return True
	except:
		return False

def twitter(name):
	form = name.split(' ')
	formal = ''.join(form)
	twitter_url = 'https://www.twitter.com/' + formal + '/'
	twitter_page = requests.get(twitter_url)
	if twitter_page.status_code == 404:
		return False
	elif twitter_page.status_code == 200:
		return True

		# rstoutarch@aol.com

def getEmail(url_for_email):
	email_response = requests.get(url_for_email)
	email_html = email_response.content
	try:
		email_soup = BeautifulSoup(email_html, 'html.parser')
		find_email = email_soup.find('a', attrs={'class': 'email-business'})['href']
		return find_email[7:len(find_email)]
	except:
		return 'not found'

def getListings(url):

	response = requests.get(url)
	html = response.content

	try:
		soup = BeautifulSoup(html, 'html.parser')
		search = soup.find('div', attrs={'class': 'search-results organic'})
		results = search.find_all('div', attrs={'class': 'result'})
	except:
		pass

	for result in results:
		business = {}
		try:
			name = result.find('a', attrs={'class': 'business-name'})
			business['name'] = name.text
			link = name['href']
			url_for_email = 'https://www.yellowpages.com' + link
			business['email'] = getEmail(url_for_email)
				
		except:
			business['name'] = 'not found'

		try:
			street_address = result.find('span', attrs={'class': 'street-address'})
			business['street_address'] = street_address.text
		except:
			business['street_address'] = 'not found'

		try:
			locality = result.find('span', attrs={'class': 'locality'})
			business['locality'] = locality.text.split(',')[0]
		except:
			business['locality'] = 'not found'

		try:
			region = result.find('span', attrs={'itemprop': 'addressRegion'})
			business['region'] = region.text
		except:
			business['region'] = 'not found'

		try:
			phone = result.find('div', attrs={'itemprop': 'telephone'})
			business['phone'] = phone.text
		except:
			business['phone'] = 'not found'

		flag = True
		business['facebook'] = facebook(business['name'])
		if business['facebook'] == False:
			flag = False
		business['instagram'] = instagram(business['name'])
		if business['instagram'] == False:
			flag = False
		business['yelp'] = yelp(business['name'], business['locality'])
		if business['yelp'] == False:
			flag = False
		business['pinterest'] = pinterest(business['name'])
		if business['pinterest'] == False:
			flag = False
		business['twitter'] = twitter(business['name'])
		if business['twitter'] == False:
			flag = False

		print(business)
		writer.writerow(business.values())

	if (soup.find('a', attrs={'class': 'next ajax-page'})):
		try:
			next_page = soup.find('a', attrs={'class': 'next ajax-page'})
			next_url = 'https://www.yellowpages.com' + next_page['href']
			return getListings(next_url)
		except:
			pass
	else:
		return

searchTerms = '0123456789abcdefghijklmnopqrstuvwxyz'
locations = ['riverside']
keys = ['name', 'yelp', 'locality', 'region', 'pinterest', 'twitter', 'phone', 'facebook', 'email', 'street_address', 'instagram']

with open('./dict.csv', 'wb') as csv_file:
    writer = csv.writer(csv_file)
    writer.writerow(keys)
    for l in locations:
		for s in searchTerms:
			try:
				url = 'https://www.yellowpages.com/search?search_terms=' + s + '&geo_location_terms=' + l + '%2C+CA'
				getListings(url)
			except:
				pass