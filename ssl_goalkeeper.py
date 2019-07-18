#!/usr/bin/env python
from datetime import date
import configparser
import argparse
import smtplib
import OpenSSL
import socket
import ssl

def get_arguments():
    '''
    Get command line arguments
    '''
    obj_parser = argparse.ArgumentParser(description = 'SSL goalkeeper')
    obj_parser.add_argument('--config', dest = 'config', default = 'ssl_goalkeeper.ini')
    obj_parser.add_argument('--nomail', dest = 'nomail', action='store_true', default=False)
    args = obj_parser.parse_args()
    return args

def get_configuration(configuration):
    '''
    Get configuration
    '''
    config = configparser.ConfigParser()
    config.read(configuration.config)
    return config

def validate_configuration(configuration):
    '''
    Validate configuration
    '''
    domains_to_check = []    
    for domain in configuration.sections():
        if domain.startswith('DOMAIN_'):
            domains_to_check.append(domain)
            if configuration.has_option(domain,'host') == False:
                raise ValueError('%s has no defined host'%(domain))
            if configuration.has_option(domain,'days') == False:
                raise ValueError('%s has no defined days alert'%(domain))
                
    if len(domains_to_check) == 0:
        raise ValueError('No domains have been defined at configuration file')
    
    if not configuration.has_section('email'):
        raise ValueError('No email section has been defined at configuration file')
        
    if not configuration.has_option('email','smtp_server'):
        raise ValueError('No smtp_server section has been configured properly at configuration file')
        
    return configuration

def check_domains(domains,args):
    '''
    Check domains
    '''
    alerts = []
    for domain in domains:
        try:
            if domain.startswith('DOMAIN_'):
                host = domains[domain]['host']
                if 'port' in domains[domain]:
                    port = domains[domain]['port']
                else:
                    port = 443
                days = domains[domain]['days']
                res = ssl_checker(host = host, port = port)
                if int(res[host]['days_to_expire']) <= int(days):
                    alert_msg = 'WARNING - %s valid since %s expires at %s - (%s days) - %s'%(res[host]['host'],res[host]['before_date'],res[host]['expire_date'],res[host]['days_to_expire'],res[host]['O'])
                    print(alert_msg)
                    message = 'Subject: SSL Goalkeeper: {} SSL Certificate expires in {} days \n\n{}'.format(res[host]['host'],res[host]['days_to_expire'],alert_msg)
                    sent_email_alerts(message=message,email_conf=domains,args=args)
        except Exception as ex:
            print('%s - %s'%(domain,str(ex)))
            pass
            
def sent_email_alerts(message,email_conf,args):
    '''
    Sent email alerts
    '''
    if args.nomail == False:
        context = ssl.create_default_context()
        try:
            server = smtplib.SMTP(email_conf['email']['smtp_server'],int(email_conf['email']['smtp_port']))
            server.ehlo()
            server.starttls()
            server.login(email_conf['email']['username'], email_conf['email']['password'])
            server.sendmail(email_conf['email']['sender_email'], email_conf['email']['to_email'], message)
        except Exception as ex:
            print('%s - %s'%(email_conf['email']['smtp_server'],str(ex)))

def ssl_checker(host,port):
    '''
    Extract some SSL Certificate properties
    '''
    certificate = ssl.get_server_certificate((host,port))
    x509_certificate = OpenSSL.crypto.load_certificate(OpenSSL.crypto.FILETYPE_PEM, certificate)
    
    notAfter     = x509_certificate.get_notAfter()
    notBefore    = x509_certificate.get_notBefore()
    issuer       = x509_certificate.get_issuer()
    
    before_day   = notBefore[6:8].decode('utf-8')
    before_month = notBefore[4:6].decode('utf-8')
    before_year  = notBefore[:4].decode('utf-8')
    
    after_day    = notAfter[6:8].decode('utf-8')
    after_month  = notAfter[4:6].decode('utf-8')
    after_year   = notAfter[:4].decode('utf-8')
    
    bef_date     = date(int(before_year), int(before_month), int(before_day))
    exp_date     = date(int(after_year),  int(after_month),  int(after_day))
    
    today = date.today()
    
    days_to_expire = today - exp_date
    days_to_expire = (abs(days_to_expire.days))
    
    res = {}
    res[host] = {}
    res[host]['host']           = host
    res[host]['CN']             = issuer.CN
    res[host]['O']              = issuer.CN
    res[host]['days_to_expire'] = days_to_expire
    res[host]['expire_date']    = str(exp_date)
    res[host]['before_date']    = str(bef_date)
    return res

if __name__ == '__main__':
    
    args = get_arguments()
    configuration = get_configuration(configuration = args)
    configuration = validate_configuration(configuration = configuration)
    check_domains(domains = configuration,args=args)
    #check_domains(domains = validate_configuration(config = get_configuration(configuration = get_arguments())))
