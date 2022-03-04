
import json
import time
import sys, os
from bs4 import BeautifulSoup
import requests
import phonenumbers
import tldextract
import tel_classifier
import email_classifier_mod_light
import regex as re
import boto3
import settings
import linkedin_utils, twitter_utils, youtube_utils
import facebook_utils, instagram_utils



def validate_email(email, api_key):
    response = requests.get(
        "https://isitarealemail.com/api/email/validate",
        params = {'email': email},
        headers = {'Authorization': "Bearer " + api_key })
    try:
        status = response.json()['status']
    except:
        status = "unkown"
        
    if status == "valid":
      out = 1
    elif status == "invalid":
      out = -1
    else:
      out = 0
    return out

def getemail(text):
    a = re.findall(r'[\w\.-]+@[\w\.-]+',text)
    return a

def dom_name(url):
    ext = tldextract.extract(url)
    dom_name = ext.domain
    return dom_name


def phone_check(text): 
    out = list()
    for match in phonenumbers.PhoneNumberMatcher(text, "FR"):
        a = phonenumbers.format_number(match.number, phonenumbers.PhoneNumberFormat.E164)
        a = '0' + a[3] + ' ' + a[4:6] + ' ' + a[6:8] + ' ' + a[8:10] + ' ' +a[10:12]
        out += [a]
    return out

def extract_text_and_links_from_url(url):
    response = requests.get(url, verify=False)
    soup = BeautifulSoup(response.text, 'html.parser')
    text = soup.get_text()
    links = list()
    for link in soup.find_all('a'):
        links.append(link.get('href'))
    links = [u for u in links if u]
    text = ' '.join(text.split())
    text +=  ' '.join(links)
    return text, links

def get_mentions_legales_url(root_url, links):
    out = list()
    for link in links:
        if dom_name(link) == dom_name(root_url) and 'mention' in link and 'legal' in link:
            out.append(link)
    return out

def get_socials(links):
    socials = {
         'linkedin': list(),
         'twitter': list(),
         'facebook': list(),
         'youtube': list(),
         'instagram': list()}
         
    for link in links:
        if dom_name(link) in ['linkedin', 'twitter','facebook', 'youtube','instagram']:
            socials[dom_name(link)] += [link]
    return socials
    
def clean_socials(raison_sociale, socials):
    for site in socials:
        socials[site] = list(set(socials[site]))
        if site == 'linkedin':
            socials[site] = linkedin_utils.clean_linkedin(
                raison_sociale, 
                ' '.join(socials[site]))
            
        if site == 'twitter':
            socials[site] = twitter_utils.clean_twitter(
                ' '.join(socials[site]))
            
        if site == 'facebook':
            socials[site] = facebook_utils.clean_facebook(
                 raison_sociale, 
                ' '.join(socials[site]))
            
        if site == 'youtube':
            socials[site] = youtube_utils.clean_youtube(
                ' '.join(socials[site]))
            
        if site == 'instagram':
            socials[site] = instagram_utils.clean_instagram(
                ' '.join(socials[site]))
    return socials

         
def get_phones(text):
    phones = tel_classifier.phone_check(text)
    fixes = [u for u in phones if u[0:2] in ["01","02","03","04","05","09"]]
    mobiles = [u for u in phones if u[0:2] in ["06","07"]]
    speciaux = [u for u in phones if u[0:2] in ["09"]]
    return fixes, mobiles, speciaux
    
def clean_emails(emails, api_key):
    ste = {
        'siren': "",
        'raison_sociale': [""],
        'domain': [""],
        'emails': [ ';'.join(emails)]
        }
    
    if len(emails) > 0:
        clean_email_output = email_classifier_mod_light.clean_emails(ste)
        #black_email = clean_email_output[1]
        #wrong_organization = clean_email_output[2]
        email_company = clean_email_output[3]

        email_company = [u for u in email_company if validate_email(
            u,
            api_key) >= 0 ]
            

        email_perso = clean_email_output[4]
        email_perso = [u for u in email_perso if validate_email(
            u,
            api_key) >= 0 ]

    else:
        email_perso = list()
        email_company = list()
    return email_perso, email_company

def get_email_validation_secret():
    client = boto3.client('secretsmanager')
    subscription_key = client.get_secret_value(
            SecretId=settings.EMAIL_VALIDATION_SECRET_ARN
            )
    api_key = subscription_key['SecretString']
    return api_key
    
    
def lambda_handler(event, context):
    if not type(event) == dict:event = json.loads(event)
    url = event['url']
    raison_sociale = event['nom_raison_sociale']
    
    api_key = get_email_validation_secret()
  
    text_with_links, links = extract_text_and_links_from_url(url)
    
    fixes, mobiles, speciaux = get_phones(text_with_links)
    
    socials = get_socials(links)
    socials = clean_socials(raison_sociale, socials)
    
    emails = getemail(text_with_links) 
    email_perso, email_company = clean_emails(emails, api_key)
    
    out = {
        'telephone_fixe': list(set(fixes)),
        'telephone_mobile': list(set(mobiles)),
        'numero_special' : list(set(speciaux)),
        #'email_individuel': list(set(email_perso)),
        'email_entreprise': list(set(email_company))
        }
    out_merged = {**out, **socials}
    return out_merged
