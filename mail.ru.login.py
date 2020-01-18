import pprint
import re
import time
import re
import requests
import sys
import urllib.parse
import json
import os
import subprocess
parser = argparse.ArgumentParser()


parser.add_argument('els', nargs='*', default=os.getcwd())



tempArgs = parser.parse_args().els


class Params:
    email = ""
    password = ""


args = Params()

args.email=tempArgs[0]
args.password=tempArgs[1]





headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36",
}

params = {
    'account_host': 'account.mail.ru',
    'email': args.email,
}

response = requests.get(
    url='https://account.mail.ru/login/',
    headers=headers,
    params=params
)


def findToken(regex, text):
    m = re.findall(regex, text, re.IGNORECASE)
    if m:
        return m[0]
    else:
        return None


csrf_token = findToken('(?<=act=)(.*?)(?=;)',
                       json.dumps(response.headers['Set-Cookie']))


mrcu = findToken('(?<=mrcu=)(.*?)(?=;)',
                 json.dumps(response.headers['Set-Cookie']))


resp = requests.post(
    url='https://auth.mail.ru/api/v1/pushauth/info',
    data={
        'email': args.email,
        'login': args.email,
        'utm': '',
        'htmlencode': 'false'
    }
)

# make login

headers = {
    "Content-type": "application/x-www-form-urlencoded",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36",
    "origin": "https://account.mail.ru",
    "host": "auth.mail.ru",
    "referer": 'https://account.mail.ru/',
    "Cache-Control": "no-cache",
    "DNT": "1",
    "accept-encoding": 'gzip, deflate, br',
    'accept-language': 'en-US,en;q=0.8,it-IT;q=0.5,it;q=0.3',
    'Cookie': f'mrcu={mrcu}; act={csrf_token}'
}

params = {
    "act_token": csrf_token,
    "saveauth": 1,
    "new_auth_form": 1,
    "FromAccount": 'opener=mail.login&allow_external=1&twoSteps=1',
    "Login": args.email,
    "Password": args.password,
    "page": 'https://e.mail.ru/messages/inbox?authid=k4fryx0k.w7&back=1&from=mail.login'
}


resp = requests.post(
    url="https://auth.mail.ru/cgi-bin/auth",
    data=params,
    headers=headers
)