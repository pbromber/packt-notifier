#! /usr/bin/python3

import requests
import smtplib

from email.mime.text import MIMEText
from lxml import html

sender = 'from@example.com'
recipient = 'to@example.com'
password = 'user_password'
smtp_address = 'smtp_address'
smtp_port = 465
title_xpath = '//*[@id="deal-of-the-day"]/div/div/div[2]/div[2]/h2/text()'
cover_xpath = '//*[@id="deal-of-the-day"]/div/div/div[1]/a/img/@data-original'
packt_page = 'https://www.packtpub.com//packt/offers/free-learning'
user_agent = 'curl/7.56.0'

headers = {'User-Agent': user_agent}
page = requests.get(packt_page, headers=headers)
tree = html.fromstring(page.content)
title = tree.xpath(title_xpath)
cover = tree.xpath('//*[@id="deal-of-the-day"]/div/div/div[1]/a/img/@data-original')[0]
cover_link = 'https:{}'.format(cover)
clean_title = title[0].replace('\n', '').replace('\t', '')

msg_template = """
<html>
  <head></head>
  <body>
    <p>Todays free book: <a href=\"{packt_page}\">{clean_title}</a></p>
    <p><a href=\"{packt_page}\"><img src=\"{cover_link}\" /></a></p>
  </body>
</html>
""".format(packt_page=packt_page, clean_title=clean_title, cover_link=cover_link)

msg = MIMEText(msg_template, 'html')
msg['Subject'] = "Daily Packt free book"
msg['From'] = sender
msg['To'] = recipient

server = smtplib.SMTP_SSL(smtp_address, smtp_port)

server.login(sender, password)
server.sendmail(sender, [recipient], msg.as_string())
server.quit()
