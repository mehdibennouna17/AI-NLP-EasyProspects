import settings

def transform_offline_output(offline_output):
    reset_items = ['url', 'snippet', 'domain', 'url_rank', 'language']
    out = dict()
    if len(offline_output['data']) > 0:
        out = offline_output['data'][0]
        for u in reset_items:
            if u in out :
                out[u] = str()
    else:
        out = {'transform_offline_output': "no data"}
    return out
    
    
    
def filter_output(output_dict):
    response_items = [
        'nom_raison_sociale',
        'nom_domaine',
        'description_entreprise',
        'siren',
        "numero_voie",
        "type_voie",
        "libelle_voie",
        "code_postal",
        "libelle_commune",
        "departement",
        "geo_adresse",
        "activite_principale",
        "libelle_activite_principale_entreprise",
        "tranche_effectif_salarie",
        "categorie_entreprise",
        "latitude",
        "longitude",
        'telephone_fixe' ,
        'telephone_mobile',
        'numero_special',
        'email_entreprise',
        'email_individuel',
        'url',
        'reseaux_sociaux',
        'etablissement',
        'linkedin',
        'twitter',
        'youtube',
        'instagram',
        'facebook'
        ]
    response = output_dict['response']
    if 'domain' in response : response['nom_domaine'] = response['domain']
    if 'snippet' in response : response['description_entreprise'] = response['snippet']
    response = {u : response[u] for u in response if u in response_items}
    if settings.FILTER_OUTPUT:
        return {
            'statusCode': output_dict['statusCode'],
            'response': response,
            'message': output_dict['message']
        }
    else:
        return output_dict

def mode(event):
    out = 'erreur'
    if 'recherche' in event :
        if len(event['recherche']) > 0:
            out = 'recherche'
    if 'siren' in event:
        if len(event['siren']) == 9:
            out = 'siren'
    return out