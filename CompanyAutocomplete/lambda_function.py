import requests
import json
import settings
import time
from utils import clean_data


def url(mode_lambda):
    if mode_lambda == 'recherche':
        url = settings.URL_BASE_FULL_TEXT + settings.SUFIXE
    if mode_lambda == 'siren':
        url = settings.URL_BASE_SIREN + settings.SUFIXE
    return url
        
def mode(event):
    out = 'erreur'
    if 'siren' in event:
        if len(event['siren']) == 9:
            out = 'siren'
    if 'recherche' in event and out == 'erreur':
        if len(event['recherche']) > 0:
            out = 'recherche'
    return out

def lambda_handler(event, context):
    mode_lambda = mode(event)
    assert 'recherche' in event or 'siren' in event, "Veuillez vérifier vos variables d'entrée"
    key = event[mode_lambda]
    t = time.time()
    response = requests.get(url(mode_lambda).format(key), verify=False)
    response.encoding = 'utf-8'
    tt = time.time()
    response_text = response.text
    response = json.loads(response.text)

    
    
    if not "no results found" in response_text:
        if mode_lambda == 'recherche':
            etablissements = [{u: clean_data(u, etab[u]) for u in settings.OUTPUT_COLS} 
                              for etab in response['etablissement']]
            response['etablissement'] = etablissements
        else:
            etablissements = [{u: clean_data(u, etab[u]) for u in settings.OUTPUT_COLS} 
                              for etab in [response['siege_social']]]
            response = {'etablissement': etablissements}
            
    else:
        response = {'etablissement': []}
    print("Durée request siren api : ", int((tt-t)*1000) , 'ms')
    return response