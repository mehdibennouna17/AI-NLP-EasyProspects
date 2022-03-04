import re
from urllib.parse import urlparse
from textdistance import levenshtein
from wordfreq import word_frequency
import protos.service_pb2 as spb2
import protos.service_pb2_grpc as spb2_grpc
import grpc
import numpy as np
import time
from numpy import dot
from numpy.linalg import norm
import settings
        
def dom_name(url):
    o = urlparse(url)
    dom_name = o.hostname
    return dom_name        

def LD(s, t): 
    res = levenshtein.distance(s, t)
    return res

def lev_score_url_with_txt(url, txt):
    url = url.lower()
    txt = txt.lower()
    dom = dom_name(url)
    dom = re.sub("[^0-9a-z]", '', dom)
    txt = re.sub("[^0-9a-z]", '', txt)
    score = 0
    lev_dist = int()
    m = min(len(dom), len(txt)) 
    lev_dist = LD(txt, dom)
    if m > 0:
        score = 1 - lev_dist/m
    return score
    

def get_all_n_grams(text_sentence):  
    sentence = text_sentence.split()
    grams = list()
    for N in range(1, len(sentence)+1):
        grams += [sentence[i:i+N] for i in range(len(sentence)-N+1)]
    return grams
    
    
def longestSubstringFinder(string1, string2):
    answer = ""
    len1, len2 = len(string1), len(string2)
    for i in range(len1):
        match = ""
        for j in range(len2):
            if (i + j < len1 and string1[i + j] == string2[j]):
                match += string2[j]
            else:
                if (len(match) > len(answer)): answer = match
                match = ""
    return answer
    
def sentence_embedding(sent, tf=True):
    sent = sent.lower()
    batch = sent.split()
    batch = [re.sub("[^a-zäåçéñöüáàâãèêëíìîïóòôõú'ùûæƒœÿ]", "", u)
             for u in batch]
    batch = [u for u in batch if word_frequency(u, 'fr') > 0 and len(u) > 2]
    freq = [word_frequency(u, 'fr') for u in batch]
    if len(batch) > 0:
        channel = grpc.insecure_channel(settings.FASTTEXT_URL)
        stub = spb2_grpc.FastTextStub(channel)
        request = spb2.VectorsRequest(
            model_name="cc.fr.300", batch=batch
        )
        response = stub.GetWordsVectors(request)
        embeddings = list()
        for i in range(len(batch)):
            a = str(response.vectors[i])
            a = a.replace('element: ', '')
            a = a.splitlines()
            if tf:
                a = [float(u)/freq[i] for u in a]
            else:
                a = [float(u) for u in a]
            embeddings.append(a)
        embeddings = np.array(embeddings)
        sent_embed = np.mean(embeddings, axis=0)
    else:
        sent_embed = np.zeros(300)   
    return sent_embed


def sentence_similarity(sent1, sent2):
    for _ in range(settings.EMBEDDINGS_MAX_TRIALS):
        try:
            vec1 = sentence_embedding(sent1)
            vec2 = sentence_embedding(sent2)
            sim = dot(vec1, vec2)/(norm(vec1)*norm(vec2))
            break
        except Exception as ex:
            print("sentence similarity error {}".format(ex))
            time.sleep(settings.EMBEDDINGS_TRIAL_SLEEP)
            sim = 'error'
    return sim