import json, ast
import boto3
import time
import pandas as pd
import utils
import predict 
import settings
import lambdas



def mode_recherche(siren_company_autocomplete):
    CompanyAutocomplete_nb_output = len(siren_company_autocomplete['etablissement'])
    output_mode_recherche = {
        'statusCode': 200,
        'message': 'mode recherche OK',
        'response': siren_company_autocomplete
                }
    return  utils.filter_output(output_mode_recherche)

def mode_siren_empty_autocomplete():
    output_mode_siren_no_entreprise_at_siren = {
            'statusCode': 204,
            'message' : "pas d'entreprise identifiée au registre SIREN avec cet identifiant",
            'response': dict()
                        }        
    return output_mode_siren_no_entreprise_at_siren


def mode_siren_full_autocomplete(client, siren_company_autocomplete):
    client = boto3.client('lambda')
    data=siren_company_autocomplete['etablissement'][0]
    FunctionName=settings.POSSIBLE_URLS_NAME
    possible_urls = lambdas.get_possible_urls(client, FunctionName, data)
    if len(possible_urls) == 0:
        out = data
        message = "pas de site internet référencé"
    else:
        data = possible_urls
        FunctionName=settings.ADD_CLASSIFIER_FEATURES_NAME
        possible_urls_with_features = lambdas.add_features(client, FunctionName, data)
        full_data = predict.predict_website(
            possible_urls_with_features, settings.CLASSIFIER_SEUIL
            )
        if not full_data:
            message = 'url non trouvé'
            out = utils.transform_offline_output(
                {'data': possible_urls_with_features})
        else:
            message = 'url identifié'
            data={"url": full_data['url'], "nom_raison_sociale": full_data['nom_raison_sociale']}
            FunctionName=settings.GET_CONTACT_NAME
            contacts = lambdas.add_contacts(client, FunctionName, data)
            out = {**full_data, **contacts}
            

    resp = {
        'statusCode': 200,
        'message' : message,
        'response': out
        }
    return utils.filter_output(resp)


def lambda_handler(event, context):
    client = boto3.client('lambda')
    if not type(event) == dict:event = json.loads(event)
    mode_lambda = utils.mode(event)
    FunctionName = settings.COMPANY_AUTOCOMPLET_NAME
    siren_company_autocomplete = lambdas.get_siren_autocomplete(
        client,
        FunctionName, 
        event)
    print(mode_lambda)    
    if mode_lambda == 'recherche':
        return mode_recherche(siren_company_autocomplete)
    else:
        CompanyAutocomplete_nb_output = len(siren_company_autocomplete['etablissement'])
        if CompanyAutocomplete_nb_output == 0:
            return mode_siren_empty_autocomplete()
        else:
            return mode_siren_full_autocomplete(
                                                client,
                                                siren_company_autocomplete)
