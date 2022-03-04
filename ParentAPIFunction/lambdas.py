import json
import boto3
import time

def get_siren_autocomplete(client, FunctionName, event):
    t = time.time()
    print(FunctionName)
    siren_company_autocomplete = client.invoke(
            FunctionName=FunctionName,    
            InvocationType='RequestResponse',
            Payload=json.dumps(event)
                )
    siren_company_autocomplete = siren_company_autocomplete['Payload'].read()
    siren_company_autocomplete = json.loads(siren_company_autocomplete)
    tt = time.time()
    print(siren_company_autocomplete)
    print("Time : ", tt-t)
    return siren_company_autocomplete
    
    
def get_possible_urls(client, FunctionName, data):
    t = time.time()
    print(FunctionName)
    possible_urls = client.invoke(
        FunctionName=FunctionName,   
        InvocationType='RequestResponse',
        Payload=json.dumps(data)
            )
    possible_urls = possible_urls['Payload'].read()
    possible_urls = json.loads(possible_urls)
    tt = time.time()
    print("Time : ", tt-t)
    print(possible_urls)
    return possible_urls
    
    
def add_features(client, FunctionName, data):
    t = time.time()
    print(FunctionName)
    possible_urls_with_features = client.invoke(
        FunctionName=FunctionName,   
        InvocationType='RequestResponse',
        Payload=json.dumps(data)
            )
    possible_urls_with_features = possible_urls_with_features['Payload'].read()
    possible_urls_with_features = json.loads(possible_urls_with_features)
    tt = time.time()
    print("Time : ", tt-t)
    print(possible_urls_with_features)
    return possible_urls_with_features
    
    
def add_contacts(client, FunctionName, data):
    t = time.time()
    print(FunctionName)
    contacts = client.invoke(
        FunctionName=FunctionName,   
        InvocationType='RequestResponse',
        Payload=json.dumps(data)
            )
    contacts = contacts['Payload'].read()
    contacts = json.loads(contacts)
    tt = time.time()
    print("Time : ", tt-t)
    print(contacts)
    return contacts
