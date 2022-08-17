import requests, sys
from bs4 import BeautifulSoup

headers = {
    'authority': 'piratebay.party',
    'method': 'GET',
    'path': '/',
    'scheme': 'https',
    'accept': 'accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,'
              '*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
    'cache-control': 'max-age=0',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'none',
    'sec-fetch-user': '?1',
    'sec-gpc': '1',
    'upgrade-insecure-requests': '1',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.87 '
                  'Safari/537.36 '
}

# q = sys.argv[1]

def connect(search):
    data = []
    i = 0
    r = requests.get('https://piratebay.party/search/' + search.replace(' ', '%20') + '/1/99/0')
    print('Accessing PirateBay.....')
    print(r.status_code, r.reason)
    
    soup = BeautifulSoup(r.text, 'html.parser')

    for info in soup.find_all('td'):
        i = info.find('a')
        if i and '/torrent' in str(i.get('href')):
            data.append(i.text)
            continue

        if i and 'magnet' in i.get('href'):
            data.append(i.get('href'))
            continue

        if 'right' in str(info.get('align')):
            data.append(info.text)
            continue

        if len(data) == 5:
            print(data[0])
            print('size: '+data[2])
            print('seeders: '+data[3])
            print('leechers: '+data[4])
            p = input('---------------------------------------------------'+ '\n')
            if p == 'f':
                print('found torrent')
                return data
            elif p == 'c':
                print('quitting')
                return ''
            data = []


# print(connect(q))
    
