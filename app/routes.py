from app import app
from flask import render_template
import gspread
import urllib2
from bs4 import BeautifulSoup
import re
from oauth2client.service_account import ServiceAccountCredentials

scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('./app/client_secret.json', scope)
client = gspread.authorize(creds)
sheet = client.open('kindlez').sheet1
urls = sheet.col_values(4)

def getPageText(url):
    # given a url, get page content
    data = urllib2.urlopen(url).read()
    # parse as html structured document
    bs = BeautifulSoup(data, features="html.parser")
    # kill javascript content

    txt = bs.find(id='kp-quote').getText()
    # remove multiple linebreaks and whitespace
    return re.sub("\s\s+" , " ", txt)

def getQuotes():
	quotes = [getPageText(url) for url in urls]

	return quotes


@app.route('/')
def index():
    quotes = getQuotes()
    times = sheet.col_values(1)
    data = dict(zip(times, quotes))
    return render_template('index.html', title="shaurya ka blog", data=data)
