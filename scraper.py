import pandas as pd 
import requests 
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
from bs4 import BeautifulSoup
import time
import cloudscraper
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

df = pd.read_csv('youtube7-13sept.csv', encoding='unicode_escape')
output_data = pd.DataFrame(columns=['urls', 'title', 'keywords'])
number_urls = df.shape[0]

i = 0

for url in df['urls']:
    print(i)
    if url.startswith('http'):
        url2 = ('http://webcache.googleusercontent.com/search?q=cache:' + url)
    elif url.startswith('https'):
        url2 = ('http://webcache.googleusercontent.com/search?q=cache:' + url)
    else:
        url2 = ('http://webcache.googleusercontent.com/search?q=cache:' + 'https://' + url)

    print(url2)
    
    try:
        # Status
        response = requests.get(url2, verify=False, timeout=5)
        status = response.status_code
        if (status == 200):
            status = "Connection Successful"
        if (status == 404):
            status = "404 Error"
            print(status)
            response = requests.get(url, verify=False, timeout=5)
        if (status == 403):
            status = "403 Error"
        if (status == 503):
            status = "503 Error"
        print(status)

        # Get Title
        def title():
            soup = BeautifulSoup(response.content, 'html.parser')
            title = soup.title
            if title == None:
                title3 = 'No Title Available'
            else:
                title2 = title.string
                print(title2)
                title3 = title2.replace(' - YouTube', '')
                print(title3)
                if title3 == 'YouTube':
                    title3 = 'Cache Unavailable'
            return str(title3)

        # Get keywords
        def keywords():
            soup = BeautifulSoup(response.content, 'html.parser')
            keywords = soup.find('meta', {'name': 'keywords'})
            if keywords == None:
                keywords = "No Keywords"
            else:
                keywords = keywords.get('content')
            print(keywords)
            return str(keywords)
        
        output_data.loc[i] = [df.iloc[i, 0], title(), keywords()]
        i += 1

    except requests.exceptions.Timeout:
        title = "N/A"
        keywords = "N/A"

        output_data.loc[i] = [df.iloc[i, 0], title]
        i += 1

    except requests.exceptions.ConnectionError:
        title = "N/A"
        keywords = "N/A"

        output_data.loc[i] = [df.iloc[i, 0], title]
        i += 1

output_data['title'] = output_data['title'].str.strip()
output_data.to_csv('output_youtube7-13sept.csv', index=False, encoding='utf-8-sig')
print('CSV file created!')
