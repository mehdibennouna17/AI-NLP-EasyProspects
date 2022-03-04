import json
import settings
import boto3
import time
import requests
from utils import extract_data_from_search_results


def lambda_handler(event, context):
    client = boto3.client('secretsmanager')
    subscription_key = client.get_secret_value(SecretId=settings.BING_SECRET_ID)
    search_url = settings.SEARCH_URL
    search_term = event['nom_raison_sociale'] + " " + event['libelle_commune']
    print("Search term : ", search_term)
    headers = {"Ocp-Apim-Subscription-Key": subscription_key['SecretString'],
               "Accept-Language": "fr"
               }
    if ('latitude' in event) and ('longitude' in event):
        la = event['latitude']
        lo = event['longitude']
        headers.update({
            "X-Search-Location": "lat:{};long:{};re:22".format(la, lo)
            })

    params = {"q": search_term}
    params.update(settings.BING_PARAMS)
    try:
        ti = time.time()
        response = requests.get(search_url,
                                headers=headers,
                                params=params
                                )
        tii = time.time()
        print("Bing time : ", (1/10)*int(10*(tii-ti)), "Seconds")
        search_results = response.json()
        output_results = extract_data_from_search_results(search_results)
        output_results = [{**result, **event} for result in output_results]
    except Exception as Ex:
        print("Error", Ex)
    return output_results

        