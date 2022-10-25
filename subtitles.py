import requests, sys, subprocess
from bs4 import BeautifulSoup
from pathlib import Path
from tqdm import tqdm




headers = {
    'Host' : 'subscene.com',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    # 'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'en-GB',
    'cache-control': 'max-age=0',
    'content-type': 'application/x-www-form-urlencoded',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-user': '?1',
    'sec-gpc': '1',
    'upgrade-insecure-requests': '1',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.54 Safari/537.36'
                  'Safari/537.36',
    'cookie': 'cf_clearance=ZOyVSyurTg.xVXaDpbJsZGJqcZRCOQeqMKKRg65xAf8-1654519231-0-250; __cf_bm=TbWS1guCxB3wbtAO24uc3fPM6S.XSTOHXc0qJl9ej2g-1655096422-0-AYAMxCUpHjyFCrC+eSOwKoWWxWrqpfsWKc2F0NknTkR9JDqWRoH27I0XoUU9crM/CpSR2CuhjQz/N75WYt+Q71PbfEmJxwRiTLjcblG8ioOpzZsv/DeapKDyJj0vYAclQQ==',
    'referer': 'https://subscene.com/',
    'origin': 'https://subscene.com'
}

# proxies = {'https': 'socks5h://127.0.0.1:9050'}
numbers = {'1': 'first', '2': 'second', '3': 'third', '4': 'fourth', '5': 'fifth', '6': 'sixth', '7': 'seventh', '8': 'eight', '9': 'nineth'}
sublink = ''
searchUrl = 'https://subscene.com/subtitles/searchbytitle'

# p = subprocess.Popen("protonvpn-cli c -f", stdout=subprocess.PIPE, shell=True)
# print(p.communicate())

def connect(url, data):
    
    r = requests.post(url, headers=headers, data=data)
    print('Accessing Subscene.com...')
    print(r.status_code, r.reason)
    return r



def series(obj, data, filt):
    for link in obj.find_all('a'):
        if str(link.get('href')).__contains__('/subtitles'):
            if str(link.text).lower().__contains__(data.get('query').split(' ')[0]):
                if numbers.get(data.get('query').split(' ')[-1]) in str(link.text).lower():
                    print(link.text)
                    sublink = link.get('href')
                    break

    r = requests.get('https://subscene.com'+sublink, headers=headers)
    print(r.status_code, r.reason)

    english(BeautifulSoup(r.text, 'html.parser'), filt)



def movies(obj, year, filt):
    for link in obj.find_all('a'):
        if str(link.get('href')).__contains__('/subtitles'):
            if str(link.text).__contains__(year):
                print(link.text)
                sublink = link.get('href')
                break

    r = requests.get('https://subscene.com'+sublink, headers=headers)
    print('Accessing Subscene.com...')
    print(r.status_code, r.reason)
    
    english(BeautifulSoup(r.text, 'html.parser'), filt)



def english(obj,filt):
    subs = []
    # filters = []
    count = 0
    for link in obj.find_all('a'):
        if str(link.get('href')).__contains__('english'):
            clean = str(link.text).split()
            clean.remove('English')
            subs.append(''.join(clean))

    print('Subtitles found: '+ str(len(subs)))

    # filter = input('enter filters: ')
    # filters = re.split('\.| |_|-', filt)
    print(filt)

    for sub in subs:
        if any(fil in sub for fil in filt) and not str(sub).__contains__('E0'):
            print('['+str(count)+']' + sub)
        count += 1
    content = input('Found ?? : ')

    if content != 'Y':
        ugh = 0 
        for sub in subs:
            print('['+str(ugh)+']'+sub)
            ugh += 1


    choice = input('Enter subtitle to download: ')
    choice = int(choice)
    for link in obj.find_all('a'):
        if str(link.get('href')).__contains__('english'):
            if subs[choice] in str(link.text):
                print('subs: '+subs[choice])
                print(link.get('href'))
                download(link.get('href'))

    # WEB.H264.tbs[eztv]
    


def execute(query, type, fil):
    data = {'query': query}
    
    if type == 'm':
        year = data.get('query').split(' ')[-1]
        data['query'] = str(data.get('query')).replace(year, '').strip()
        soup = BeautifulSoup(connect(searchUrl, data).text, 'html.parser')

        movies(soup, year, fil)
    else:
        soup = BeautifulSoup(connect(searchUrl, data).text, 'html.parser')
        series(soup, data, fil)




def download(link):
    lonk = ''
    r = requests.get('https://subscene.com'+link, headers=headers)
    soup = BeautifulSoup(r.text, 'html.parser')

    for deet in soup.find_all('a'):
        if deet.get('id') == 'downloadButton':
            lonk = deet.get('href')
            break
    
    d = requests.get('https://subscene.com'+ lonk, headers=headers, stream=True)
    total = int(d.headers.get('content-length', 0))
    progress_bar = tqdm(total=total, unit='iB', unit_scale=True)
    
    with open(str(Path.home()) + '/Downloads/sub', 'wb') as file:
        for dat in d.iter_content(1024):
            progress_bar.update(len(dat))
            file.write(dat)
        progress_bar.close()

    # p = subprocess.Popen("protonvpn-cli d", stdout=subprocess.PIPE, shell=True)
    # print(p.communicate())
    z = subprocess.Popen('unzip ~/Downloads/sub -d ~/Downloads/subtitles', stdout=subprocess.PIPE, shell=True)
    print(z.communicate())




print('arguments order: srch, type, filters')
try:
    search = sys.argv[1]
    option = sys.argv[2]
    fil = sys.argv[3]
    execute(search, option, fil)

except:
    print('no user input received')