from bs4 import BeautifulSoup
import requests

headers = {
    # ':authority': '1337x.to',
    # ':method': 'GET',
    # ':path': '/search/sherlock/1/',
    # ':scheme': 'https',
    'accept' : 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    # 'accept-encoding' : 'gzip, deflate, br',
    'accept-language' : 'en-GB;q=0.7',
    # 'cache-control' : 'max-age=0',
    'cookie' : '__cf_bm=C3AofcOuck3Yz.LUMvDGBTrGth1xvJ2h2hTZr7TesNI-1655131678-0-AXdea+1LUFBjeQCRpI2OAI5fmF63PonKHn9DrAQ4A5TBoHjxK94UhFSWEvgorjKQrhHyZIyyu7Jx7dgx57I5Qnter4yR1A6u3YqN0/Bqs9ZCKrTrXePtsXUUOyFKeCJXgA==',
    # 'referer' : 'https://1337x.to/',
    'Sec-Fetch-Dest' : 'document',
    'Sec-Fetch-Mode' : 'navigate',
    'Sec-Fetch-Site' : 'none',
    'Sec-Fetch-User' : '?1',
    'Sec-Gpc' : '1',
    'Upgrade-Insecure-Requests' : '1',
    'User-Agent' : 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.61 Safari/537.36'
}


def search(query):
    result = []
    results = []
    r = requests.get('https://1337x.to/search/'+query.replace(' ','+')+'/1/', headers=headers)
    print(r.status_code, r.reason)
    soup = BeautifulSoup(r.text, 'html.parser')

    for info in soup.find_all('td'):
        if 'name' in str(info.get('class')):
            result.append(info.text)
            result.append(info.find_all('a')[1].get('href'))
            continue
        if 'seeds' in str(info.get('class')):
            result.append(info.text)
            continue
        if 'leeches' in str(info.get('class')):
            result.append(info.text)
            continue
        if 'size' in str(info.get('class')):
            info.span.clear()
            result.append(info.text)
            results.append(result)
            result = []
            continue


    for index, entry in enumerate(results):
        if any(substring in entry[0] for substring in query.split(' ')):
            print('['+str(index)+']'+entry[0])
            print('seeders: '+entry[2])
            print('leechers: '+entry[3])
            print('size: '+entry[4]+'\n')
            p = input('-------------------------------------------------------------------------- \n ')
            if p != '':
                break

    i = input('Enter selected torrent: ')
    return results[int(i)]




def magnet(url):
    r = requests.get('https://1337x.to'+url, headers=headers)
    print(r.status_code, r.reason)
    soup = BeautifulSoup(r.text, 'html.parser')

    for li in soup.find_all('li'):
        if 'magnet' in str(li):
            return str(li.find('a').get('href'))
            

# magnet(search(query)[1])

# fix the unknown character termination

