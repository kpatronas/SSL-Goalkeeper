SSL Goalkeeper: email alerts when an SSL Certificate is about to expire

Usage:
python ./ssl_goalkeeper.py -h
usage: ssl_goalkeeper.py [-h] [--config CONFIG] [--nomail]

SSL goalkeeper

optional arguments:
  -h, --help       show this help message and exit
  --config CONFIG
  --nomail

# Configuration sections
[email]                              <- configure an email server to sent email alerts, smtp is currently only supported
smtp_server=smtp_server.example.com
smtp_port=587
username=username
sender_email=sender_email@example.com
to_email=receiver_email@example.com
password=password

[DOMAIN_www.google.com] <- each domain section to be check must start with "DOMAIN_"
host=www.google.com     <- domain to check
days=500                <- sent an email when the number of days for the cert to expire are less or equal than the day number

[DOMAIN_www.in.gr]
host=www.in.gr
days=500
