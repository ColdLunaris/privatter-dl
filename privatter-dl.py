import requests, argparse, os
from termcolor import colored
from bs4 import BeautifulSoup

def parse_args():
    p = argparse.ArgumentParser()

    p.add_argument("-d", dest="directory", required=False, help="destination where all images will be saved")
    p.add_argument("-u", dest="url", required=True, help="url for profile to be downloaded")
    p.add_argument("-v", dest="verbose", required=False, default=True, help="specifies verbosity to true or false. Default true")
    p.add_argument("-U", dest="username", required=True, help="Username for login to Privatter")
    p.add_argument("-P", dest="password", required=True, help="Password for login to Privatter")

    return p.parse_args()

def create_directory(url, dir):
    p = os.getcwd() if dir is None else dir
    if not p.endswith('/'):
        p = p + '/'

    # Get username from supplied url. Create destination directory with it
    p = p + url.split('/')[-1].split('#')[0]

    if not os.path.exists(p):
        os.makedirs(p)

    return p

def save_image(link, path, v):
    name = link.rsplit('/', 1)[-1]
    path = path + '/' + name

    # Privatter, unlike poipiku, does not host images themselves. No auth needed once URLs have been found
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

def create_session(username, password):
    s = requests.Session()

    s.headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36',
        'Host': 'privatter.net'
    }

    # Probably a really bad way to handle passwords... But we need to generate a unique login per session.
    # Cookies CAN be used, but it's much easier to just use plain username and password
    payload = {
        'mode': 'login',
        'login_id': username,
        'password': password
    }

    s.post('https://privatter.net/login_pass', data=payload)

    return s

def get_image_sites(s, url):
    r = s.get(url)

    soup = BeautifulSoup(r.text, 'html.parser')
    pages = soup.findAll(class_="pull-left")

    links = ['https://privatter.net' + str(page).split('href="')[1].split('">')[0] for page in pages]

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

    with create_session(a.username, a.password) as s:
        path = create_directory(a.url, a.directory)
        links = get_image_sites(s, a.url)
        
        for link in links:
            get_image_direct_link(s, link, path, a.verbose)