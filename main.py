import requests
from bs4 import BeautifulSoup
import gspread
import time

def request():
    #Grabs HTML
    URL = "http://aqwwiki.wikidot.com/classes"
    page = requests.get(URL)
    #Translates HTML
    soup = BeautifulSoup(page.text, 'html.parser')
    return soup

def parse(soup):
    #Grabs Classes
    htmlcode = soup.find_all('div', class_='list-pages-item')
    base_url = "http://aqwwiki.wikidot.com"
    classlist = []
    wikilist = []
    for item in htmlcode:
        ClassName = item.text.strip()
        for a in item.find_all('a', href=True):
            wikiurl = (base_url + a['href'])
            classlist.append(ClassName)
            wikilist.append(wikiurl)
    return classlist, wikilist

def output(classlist, wikilist):
    gc = gspread.service_account(filename='aqwclass-j.json')
    sh = gc.open('AQW Classes').sheet1
    for key,value in zip(classlist, wikilist):
        sh.append_row([str(key), str(value)])
        time.sleep(1.2)

data = request()
classlist, wikilist = parse(data)
output(classlist, wikilist)