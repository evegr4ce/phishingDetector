# URL Feature Extraction -> Sept. 9th

import pandas as pd
from urllib.parse import urlparse, urlencode
import ipaddress
from bs4 import BeautifulSoup
import whois
import urllib
import urllib.request
import re
from datetime import datetime
import time

# important features: @ symbols, length of url, depth (amt of /), redirection, https certificate, url shorteners, unusual symbols, # of periods
# LIVE SCRAPING: DNS history, ip address, web traffic, DNS age, DNS expiration, page text

# url analysis

def hasAt(url):
    if '@' in url:
        return 1
    return 0

def getLen(url):
    return len(url)

def getDepth(url):
    depth = 0
    split = url.split('/')

    for i in range(len(split)):
        depth += 1

    return depth - 2

def hasRedirection(url):
    return url.count("//") - 1

def checkDomain(url):
    dom = urlparse(url).netloc
    if 'https' in url:
        return 1
    return 0

def checkShort(url):
    # list of common services
    shortening_services = r"bit\.ly|goo\.gl|shorte\.st|go2l\.ink|x\.co|ow\.ly|t\.co|tinyurl|tr\.im|is\.gd|cli\.gs|" \
                      r"yfrog\.com|migre\.me|ff\.im|tiny\.cc|url4\.eu|twit\.ac|su\.pr|twurl\.nl|snipurl\.com|" \
                      r"short\.to|BudURL\.com|ping\.fm|post\.ly|Just\.as|bkite\.com|snipr\.com|fic\.kr|loopt\.us|" \
                      r"doiop\.com|short\.ie|kl\.am|wp\.me|rubyurl\.com|om\.ly|to\.ly|bit\.do|t\.co|lnkd\.in|db\.tt|" \
                      r"qr\.ae|adf\.ly|goo\.gl|bitly\.com|cur\.lv|tinyurl\.com|ow\.ly|bit\.ly|ity\.im|q\.gs|is\.gd|" \
                      r"po\.st|bc\.vc|twitthis\.com|u\.to|j\.mp|buzurl\.com|cutt\.us|u\.bb|yourls\.org|x\.co|" \
                      r"prettylinkpro\.com|scrnch\.me|filoops\.info|vzturl\.com|qr\.net|1url\.com|tweez\.me|v\.gd|" \
                      r"tr\.im|link\.zip\.net"

    check = re.search(shortening_services, url)

    if check:
        return 1
    return 0

def oddCharacters(url):
    count = 0
    for char in url:
        if not char.isalnum():
            count += 1

    return count

def numPeriods(url):
    return url.count('.')

# live scraping

def hasIP(url):
  try:
    ipaddress.ip_address(url)
    return 1
  except:
    return 0

def hasTraffic(url):
  try:
    url = urllib.parse.quote(url)
    rank = BeautifulSoup(urllib.request.urlopen("http://data.alexa.com/data?cli=10&dat=s&url=" + url).read(), "xml").find(
        "REACH")['RANK']
    rank = int(rank)
    if rank <100000:
        return 1
    else:
        return 0
  except:
    return 1


def domainAge(domain_name):
  creation_date = domain_name.creation_date
  expiration_date = domain_name.expiration_date
  if (isinstance(creation_date,str) or isinstance(expiration_date,str)):
    try:
      creation_date = datetime.strptime(creation_date,'%Y-%m-%d')
      expiration_date = datetime.strptime(expiration_date,"%Y-%m-%d")
    except:
      return 1
  if ((expiration_date is None) or (creation_date is None)):
      return 1
  elif ((type(expiration_date) is list) or (type(creation_date) is list)):
      return 1
  else:
    ageofdomain = abs((expiration_date - creation_date).days)
    if ((ageofdomain/30) < 6):
      age = 1
    else:
      age = 0
  return age

def pageText(url):
    try:
        url = url_entry.get()

        if url:
            response = requests.get(url)

            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                extracted_data = soup.get_text()
                return str(extracted_data)
        else:
            return 0
    except:
        return 0

def featureExtraction(url, label=0):

  features = []

  # url analysis
  features.append(url)
  features.append(hasAt(url))
  features.append(getLen(url))
  features.append(getDepth(url))
  features.append(hasRedirection(url))
  features.append(checkDomain(url))
  features.append(checkShort(url))
  features.append(oddCharacters(url))
  features.append(numPeriods(url))

  # live scraping
  dns = 0
  try:
    domain_name = whois.whois(urlparse(url).netloc)
  except:
    dns = 1

  features.append(hasIP(url))
  features.append(hasTraffic(url))
  features.append(1 if dns == 1 else domainAge(domain_name))
  features.append(pageText(url))
  features.append(label)

  return features

# DO NOT RUN / MAIN TRAINING DATA LOOP
def mainScraping():
    feature_names = ['URL', 'HasAt', 'URLLen', 'URLDepth', 'Redirection', 'domainType', 'ShortURL',
                      'OddChar', 'numPer', 'HasIP', 'Web_Traffic', 'DomainAge', 'Text',
                      'Label']

    legit = pd.read_csv("./DataFiles/benign_list.csv")
    phish = pd.read_csv("./DataFiles/online-valid.csv")

    legit.columns = ["url"]

    randLegit = legit.sample(n = 10000, random_state = 1234).copy()
    phishLegit = phish.sample(n = 10000, random_state = 1234).copy()

    randLegit = randLegit.reset_index(drop=True)
    randPhish = phishLegit.reset_index(drop=True)

    legitFeat = []
    label = 0
    for i in range(10000):
        legitFeat.append(featureExtraction(randLegit["url"][i], label))
        time.sleep(1)

    legitimate = pd.DataFrame(legitFeat, columns=feature_names)

    phishFeat = []
    label = 1
    for i in range(10000):
        phishFeat.append(featureExtraction(randPhish["url"][i], label))
        time.sleep(1)

    phishing = pd.DataFrame(phishFeat, columns=feature_names)

    urldata = pd.concat([legitimate, phishing]).reset_index(drop=True)

    urldata.to_csv('urldata.csv', index=False)
