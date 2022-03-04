import utils
import math
import re
import time

def snippet_score(bing_result_dict):
    t = time.time()
    score = utils.sentence_similarity(
        bing_result_dict['snippet'],
        bing_result_dict['libelle_activite_principale_entreprise'])
    tt = time.time()
    print("snippet_score time : ", tt-t)
    return score


def dom_lev_score(bing_result_dict):
    t = time.time()
    score = 0
    print("aa")
    score = utils.lev_score_url_with_txt(
        bing_result_dict['url'],
        bing_result_dict['nom_raison_sociale'])
    tt = time.time()
    print("dom_lev_score time : ", tt-t)
    return score

def max_rs_n_gram_matching_dom(bing_result_dict):
    t = time.time()
    n = 0
    rs = bing_result_dict['nom_raison_sociale'].lower()
    n_rs = len(rs.split())
    url = bing_result_dict['url']
    n_grams = utils.get_all_n_grams(rs)
    dom = bing_result_dict['domain'].lower()
    dom = re.sub("[^0-9a-z]", "", dom)
    max_n = 0
    for n_gram in n_grams:
        n = len(n_gram)
        if ' '.join(n_gram) in dom:
           max_n = max(n, max_n)
    score = (math.exp(max_n) - 1)*(1- math.exp(-n_rs))
    tt = time.time()
    print("max_rs_n_gram_matching_dom time : ", tt-t)
    return score

def max_len_string_match(bing_result_dict):
    t = time.time()
    rs = bing_result_dict['nom_raison_sociale'].lower()
    url = bing_result_dict['url'].lower()
    n = 0
    dom = bing_result_dict['domain'].lower()
    n = len(utils.longestSubstringFinder(dom, rs))
    if min(len(dom), len(rs)) > 0:
        score = n / min(len(dom), len(rs))
    else:
        score = 0
    tt = time.time()
    print("max_len_string_match time : ", tt-t)
    return score

def dom_ville_score(bing_result_dict):
    t = time.time()
    url = bing_result_dict['url'].lower()
    dom = bing_result_dict['domain'].lower()
    score = 0
    if bing_result_dict['libelle_commune'].lower() in dom:
        score = 1
    tt = time.time()
    print("dom_ville_score time : ", tt-t)
    return score
        
def dom_dep_score(bing_result_dict):
    t = time.time()
    url = bing_result_dict['url'].lower()
    dom = bing_result_dict['domain'].lower()
    score = 0
    if bing_result_dict['code_postal'][0:2] in dom:
        score = 1
    tt = time.time()
    print("dom_dep_score time : ", tt-t)
    return score
    
def lang(bing_result_dict):
    l = 1
    if not bing_result_dict['language'] == 'fr':
        l = 0
    return l