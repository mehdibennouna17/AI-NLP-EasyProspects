import json
import features_builder
import black_domains


def check_if_none(text):
    if not text:
        out = str()
    else:
        out = str(text)
    return out
        
    
def score_possible_url(possible_url): 
    dom_lev_score = features_builder.dom_lev_score(possible_url)
    max_rs_n_gram_matching_dom = features_builder.max_rs_n_gram_matching_dom(possible_url)
    max_len_string_match = features_builder.max_len_string_match(possible_url)
    dom_ville_score = features_builder.dom_ville_score(possible_url)
    dom_dep_score = features_builder.dom_dep_score(possible_url)
    snippet_score = features_builder.snippet_score(possible_url)
    lang = features_builder.lang(possible_url)
    adresse = ' '.join([
            check_if_none(possible_url['numero_voie']),
            check_if_none(possible_url['type_voie']),
            check_if_none(possible_url['libelle_voie'])
            ]) 
    output = {
        'dom_lev_score' :  dom_lev_score,
        'max_rs_n_gram_matching_dom' : max_rs_n_gram_matching_dom,
        'max_len_string_match' : max_len_string_match,
        'dom_ville_score' : dom_ville_score,
        'dom_dep_score' :  dom_dep_score,
        'snippet_score': snippet_score,
        'lang': lang,
        'adresse': adresse
        }
    return output

def lambda_handler(event, context):
    
    output = [
        {**possible_url, **score_possible_url(possible_url)} for possible_url in event
        if not possible_url['domain'] in black_domains.black_domains]
    if len(output) == 0:
        choice = event[0]
        for u in ['url', 'domain', 'snippet', 'language']: choice[u] = str()
        output = [choice]
    return output
    