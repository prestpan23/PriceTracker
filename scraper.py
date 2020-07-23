import sys
import os
import subprocess
import time
import json
import threading

try:
    from bs4 import BeautifulSoup
    import requests
    import smtplib
    from email.message import EmailMessage
except ImportError:
    subprocess.run(['pip', 'install', 'beautifulsoup4'])
    subprocess.run(['pip', 'install', 'smtplib'])
    subprocess.run(['pip', 'install', 'requests'])
finally:
    from bs4 import BeautifulSoup
    import requests
    import smtplib
    from email.message import EmailMessage

try:
    with open('url.json', 'r') as f:
        data = json.load(f)
except EnvironmentError:
    print('Make a url.json. See the example config file.')
    sys.exit(0)

# settings to change:

# Environment variables.
EMAIL = os.environ.get('AutomatedEmail')
PASSWORD = os.environ.get('EmailPass')

# URLs to track
URLS = list(data.keys())

# specify the URLS and their prices.
URL_KEY = data

# to find your user agent, simply type in 'my user agent' into your default web browser.
HEADERS = {"User-Agent": 'Mozilla/5.0 (X11; Linux x86_64; rv:77.0) Gecko/20100101 Firefox/77.0'}

# don't change:
_THREADS = []


def scrape(integer):
    r = requests.get(URLS[integer], headers=HEADERS)
    soup = BeautifulSoup(r.content, 'html.parser')
    price = soup.find(id="priceblock_ourprice").get_text()
    print(price.strip())
    try:
        int_price = int(price[4:])
    except ValueError:
        print("Something went wrong. Lol.")
        sys.exit(0)
    if URL_KEY[URLS[integer]] >= int_price:
        msg = EmailMessage()
        msg['Subject'] = 'The Price is Right!'
        msg['From'] = EMAIL
        msg['To'] = EMAIL
        msg.set_content(f'The price dropped below {URL_KEY[URLS[integer]]}. Check this link: {URLS[integer]}')
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            try:
                smtp.login(EMAIL, PASSWORD)
                smtp.send_message(msg)
            except smtplib.SMTPAuthenticationError:
                print("password not valid.")
                sys.exit(0)


if __name__ == '__main__':
    while True:
        try:
            for i in range(len(URLS)):
                t = threading.Thread(target=scrape, args=[i - 1])
                t.start()
                _THREADS.append(t)

            for thread in _THREADS:
                thread.join()

            time.sleep(10000)
        except KeyboardInterrupt:
            sys.exit(0)
