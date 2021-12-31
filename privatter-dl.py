import requests, argparse, os
from http.cookiejar import MozillaCookieJar
from requests.sessions import session
from termcolor import colored
from bs4 import BeautifulSoup

def parse_args():
    p = argparse.ArgumentParser()

    p.add_argument("-d", dest="directory", required=False, help="destination where all images will be saved")
    p.add_argument("-c", dest="cookie", required=True, help="path to authenticated cookie-file")
    p.add_argument("-u", dest="url", required=True, help="url for profile to be downloaded")
    p.add_argument("-v", dest="verbose", required=False, default=True, help="specifies verbosity to true or false. Default true")
    
    return p.parse_args()

def create_directory(url, dir):
    p = os.getcwd() if dir is None else dir
    if not p.endswith('/'):
        p = p + '/'

    # Get username from supplied url
    p = p + url.split('/')[-1].split('#')[0]

    if not os.path.exists(p):
        os.makedirs(p)

    return p

def save_image(link, path, v):
    name = link.rsplit('/', 1)[-1]
    path = path + '/' + name
    r = requests.get(link, stream=True)

    if r.status_code == 200 and not os.path.exists(path):
        with open(path, 'wb') as f:
            for c in r:
                f.write(c)
        if v is True:
            print(colored(path, 'white'))
    else:
        if v is True:
            print(colored(path, 'green'))

def import_cookies(cookie):
    with open(cookie) as c:
        for line in c:
            if 'PHPSESSID' in line:
                return str(line.split('\t')[5] + '=' + line.split('\t')[6].replace('\n', ''))

def create_session(cookie):
    s = requests.Session()

    session_id = import_cookies(cookie)
    s.headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36',
        'Host': 'privatter.net',
        'Cookie': session_id,
    }

    return s

def get_image_sites(s, url):
    r = s.get(url)

    soup = BeautifulSoup(r.text, 'html.parser')
    pages = soup.findAll(class_="pull-left")

    links = []
    for page in pages:
        link = 'https://privatter.net' + str(page).split('href="')[1].split('">')[0]
        links.append(link)

    return links[::-1]

def get_image_direct_link(s, url, path, v):
    r = s.get(url)

    soup = BeautifulSoup(r.text, 'html.parser')
    direct_links = soup.findAll(class_="image")

    for link in direct_links:
        link = str(link).split('href="')[1].split('"')[0]
        save_image(link, path, v)

if __name__ == "__main__":
    a = parse_args()
    

    with create_session(a.cookie) as s:
        path = create_directory(a.url, a.directory)
        links = get_image_sites(s, a.url)
        
        for link in links:
            get_image_direct_link(s, link, path, a.verbose)