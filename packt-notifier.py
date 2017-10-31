#! /usr/bin/python3

import requests
import smtplib

from email.mime.text import MIMEText
from lxml import html

sender = 'sender@example.com'
recipient = 'recipient@example.com'
password = 'smtp_password'
smtp_address = 'smtp_server_address'
smtp_port = 465


headers = {'User-Agent': 'curl/7.56.0'}
page = requests.get("https://www.packtpub.com//packt/offers/free-learning", headers=headers)
tree = html.fromstring(page.content)
title = tree.xpath('//*[@id="deal-of-the-day"]/div/div/div[2]/div[2]/h2/text()')
clean_title = title[0].replace('\n', '').replace('\t', '')


msg = MIMEText("Todays free book: {}".format(clean_title))
msg['Subject'] = "Daily PACKT free book"
msg['From'] = sender
msg['To'] = recipient

server = smtplib.SMTP_SSL(smtp_address, smtp_port)

server.login(sender, password)
server.sendmail(sender, [recipient], msg.as_string())
server.quit()
