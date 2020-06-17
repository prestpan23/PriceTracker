from bs4 import BeautifulSoup
import requests
import smtplib
import sys
import os
from email.message import EmailMessage
import time

# settings to change:
EMAIL = os.environ.get('AutomatedEmail')
PASSWORD = os.environ.get('EmailPass')
URL = 'https://www.amazon.ca/Asus-GA502DU-PB73-Zephyrus-Gaming-Laptop/dp/B07QQ9LZZK/ref=sr_1_2?dchild=1&keywords=rog' \
      '+zephyrus+g14&qid=1592334468&sr=8-2 '
HEADERS = {"User-Agent": 'Mozilla/5.0 (X11; Linux x86_64; rv:77.0) Gecko/20100101 Firefox/77.0'}
PRICE = 1111
CONTENT = f'The price dropped below {PRICE}. Check this link: {URL}'

# Don't change:


def send_mail():
    msg = EmailMessage()
    msg['Subject'] = 'The Price is Right!'
    msg['From'] = EMAIL
    msg['To'] = EMAIL
    msg.set_content(CONTENT)
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        try:
            smtp.login(EMAIL, PASSWORD)
            smtp.send_message(msg)
        except smtplib.SMTPAuthenticationError:
            print("password not valid.")
            sys.exit(0)


def scrape():
    while True:
        r = requests.get(URL, headers=HEADERS)
        soup = BeautifulSoup(r.content, 'lxml')
        price = soup.find(id='priceblock_ourprice').get_text()

        print(price.strip())

        int_price = int(price[4:])
        print(int_price)
        if PRICE > int_price:
            send_mail()
            sys.exit(0)
        else:
            # Change the time in seconds:
            time.sleep(1000)


if __name__ == '__main__':
    scrape()
