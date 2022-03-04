import pickle, os
import pandas as pd
from nlp_tools_email_classifier import Nlp_tools
import regex as re


def dom_available_in_emails(row):
    if row['domain'] in row['emails']:
        out = 1
    else:
        out = 0
    return out

def remove_last_dot(text):
    if len(text) > 0:
        if text[-1] == ".":
            out = text[0: len(text)-1]
        else:
            out = text
    else:
        out = str()
    return out

def nb_points_post_arobase(email):
    email = [u for u in email]
    arobase_index = email.index('@')
    post_arobase = email[arobase_index:len(email)]
    n = 0
    for u in post_arobase:
        if u == '.':n+=1
    return n

def key_words(row):
        separators = ['-', '_', '.']
        prefixe = row['prefixe']
        #global separator
        for sep in separators:
           prefixe = prefixe.replace(sep, ' ')
        prefixe = prefixe.split()
        prefixe = [re.sub("[^a-z]", '', u) for u in prefixe]
        #prefixe = [u for v in prefixe for u in Nlp_tools.split_text(v)[1]]
        prefixe = [u for u in prefixe if len(u) > 2]
        prefixe = list(set(prefixe))
        out = ';'.join(prefixe)
        return out


def inv_log_freq_prefixe_vocab_prod(row, par):
    clean_prefixe = row['prefixe_keywords'].split(';')
    clean_prefixe = [re.sub("[^a-z]", '', u) for u in clean_prefixe]
    out = [Nlp_tools.split_text(u, par)[0] for u in clean_prefixe]
    out = min(out)
    return out


def inv_log_freq_prefixe_noms_prod(row, par):
    clean_prefixe = row['prefixe_keywords'].split(';')
    clean_prefixe = [re.sub("[^a-z]", '', u) for u in clean_prefixe]
    out = [Nlp_tools.split_name(u, par)[0] for u in clean_prefixe]
    out = min(out)
    return out

def inv_log_freq_prefixe_prenoms_prod(row, par):
    clean_prefixe = row['prefixe_keywords'].split(';')
    clean_prefixe = [re.sub("[^a-z]", '', u) for u in clean_prefixe]
    out = [Nlp_tools.split_first_name(u, par)[0] for u in clean_prefixe]
    out = min(out)
    return out

def inv_log_freq_prefixe_perso(row):
    score_prenom = row['inv_log_freq_prefixe_prenoms']
    score_nom = row['inv_log_freq_prefixe_noms']
    out = min(score_prenom, score_nom)
    return out



def replace_inf(x):
    if x == 'inf':
        out = 100
    else:
        out = x
    return out

def cat(row):
    if not row['extension'] in ['at','au','be','biz','br','bzh','ch','co','com','coop','cz','de','edu','es','eu','fi','fr','frou','ft','gouv','gov','gp','gr','group','hk','hr','hu','immo','in','info','io','it','jp','kr','lu','media','mg','mq','nc','net','nl','no','nz','online','org','paris','pl','pro','pt','re','ro','ru','se','si','studio','tech','tr','travel','tv','uk','us','yt','za','zm']:
        out = 'not_email'
    elif ('cnil' in row['prefixe']) or ('rgpd' in row['prefixe']) or ('dpo' in row['prefixe']) or ('dpd' in row['prefixe']) :
        out = 'black_email'
    elif row['dom_available_in_emails'] == 1 and not row['domain'] in row['emails']:
        out = 'wrong_organization'
    elif row['inv_log_freq_prefixe_vocab'] < replace_inf(row['inv_log_freq_prefixe_perso']):
        out = 'email_company'
    else:
        out = 'email_perso'
    return out


def email_parse(email):
    email = [l for l in email]
    arobase_index = email.index('@')
    if '.' in email:
        dot_indexe = len(email) - email[::-1].index('.') - 1
    else:
        dot_indexe = len(email)
    size = len(email)
    prefixe = ''.join(email[0:arobase_index])
    suffixe = ''.join(email[arobase_index+1:dot_indexe])
    extension = ''.join(email[dot_indexe+1:size])
    return prefixe, suffixe, extension



def pickle_it(file_name, obj):
    file = file_name
    try:
        with open(file, mode='rb') as f:
            out = pickle.load(f)
    except FileNotFoundError:
        out = obj
        with open(file, mode='wb') as f:
            pickle.dump(obj, f)
    return out

def is_in_aws():
    return os.getenv('AWS_EXECUTION_ENV') is not None

def add_freq_to_param():
    param = dict()
    if is_in_aws():
        param['word_freq_fr'] = pickle_it("/opt/python/word_freq_fr", "-> already pickeled")
        param['noms_freq_fr'] = pickle_it("/opt/python/noms_freq_fr_500000", "-> already pickeled")
        param['prenoms_freq_fr'] = pickle_it("/opt/python/prenoms_freq_fr", "-> already pickeled")
    else:
        param['word_freq_fr'] = pickle_it("/Users/mehdibennouna/Dropbox/Perso/Machine learning/Power_data/NLP_enrich/Lambda/url_to_data/scrap/url_to_data_api/utils/word_freq_fr", "-> already pickeled")
        param['noms_freq_fr'] = pickle_it("/Users/mehdibennouna/Dropbox/Perso/Machine learning/Power_data/NLP_enrich/Lambda/url_to_data/scrap/url_to_data_api/utils/noms_freq_fr_500000", "-> already pickeled")
        param['prenoms_freq_fr'] = pickle_it("/Users/mehdibennouna/Dropbox/Perso/Machine learning/Power_data/NLP_enrich/Lambda/url_to_data/scrap/url_to_data_api/utils/prenoms_freq_fr", "-> already pickeled")
    return param



def clean_emails(company_dict):
    paramètres = add_freq_to_param()
    data = pd.DataFrame.from_dict(company_dict)
    data['dom_available_in_emails'] = data.apply(
        dom_available_in_emails,
        axis=1
        )
    data['emails'] = data['emails'].apply(lambda x: x.split(';'))
    dataset = data.explode('emails')
    dataset['emails'] = dataset['emails'].apply(lambda x : remove_last_dot(x))
    dataset['emails'] = dataset['emails'].apply(lambda x : Nlp_tools.strip_accents(x))
    dataset = dataset.drop_duplicates(subset=['siren', 'emails'], keep='first',ignore_index=True)
    
    dataset = dataset[~dataset['emails'].isin([''])]
    dataset['prefixe'] = dataset['emails'].apply(lambda x: email_parse(x)[0])
    dataset['suffixe'] = dataset['emails'].apply(lambda x: email_parse(x)[1])
    dataset['extension'] = dataset['emails'].apply(lambda x: email_parse(x)[2])
    dataset['dom_email'] = dataset['emails'].apply(
        lambda x: email_parse(x)[1] + '.' + email_parse(x)[2] )
    dataset['nb_points_post@'] = dataset['emails'].apply(
        lambda x:nb_points_post_arobase(x))
    #dataset['check_email_domain_with_website'] = dataset.apply(
    #    check_dom,
    #    axis=1
    #    )
    #dataset['nb_chiffres_prefixe'] = dataset.apply(
    #    nb_chiffres_pref,
    #    axis=1
    #    )
    dataset['prefixe_keywords'] = dataset.apply(
        key_words,
        axis=1
        )
    dataset['inv_log_freq_prefixe_vocab'] = dataset.apply(
        inv_log_freq_prefixe_vocab_prod,
        par=paramètres,
        axis=1
        )
    dataset['inv_log_freq_prefixe_noms'] = dataset.apply(
        inv_log_freq_prefixe_noms_prod,
        par=paramètres,
        axis=1
        )
    dataset['inv_log_freq_prefixe_prenoms'] = dataset.apply(
        inv_log_freq_prefixe_prenoms_prod,
        par=paramètres,
        axis=1
        )
    dataset['inv_log_freq_prefixe_perso'] = dataset.apply(
        inv_log_freq_prefixe_perso,
        axis=1
        )

    dataset['cat'] = dataset.apply(
        cat,
        axis=1
        )
    
    not_email = dataset[dataset['cat'].isin(['not_email'])]
    black_email = dataset[dataset['cat'].isin(['black_email'])]
    wrong_organization = dataset[dataset['cat'].isin(['wrong_organization'])]
    email_company = dataset[dataset['cat'].isin(['email_company'])]
    email_perso = dataset[dataset['cat'].isin(['email_perso'])]

    not_email = not_email['emails'].to_list()
    black_email = black_email['emails'].to_list()
    wrong_organization = wrong_organization['emails'].to_list()
    email_company = email_company['emails'].to_list()
    email_perso = email_perso['emails'].to_list()
    
    return not_email, black_email, wrong_organization, email_company, email_perso
        

