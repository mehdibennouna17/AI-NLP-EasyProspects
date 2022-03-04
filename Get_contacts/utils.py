from textdistance import levenshtein
import unicodedata
import regex as re

def strip_accents(text):
    try:
        text = unicode(text, 'utf-8')
    except NameError: # unicode is a default on python 3 
        pass

    text = unicodedata.normalize('NFD', text)\
           .encode('ascii', 'ignore')\
           .decode("utf-8")
    return str(text)


def format_web_str(string):
    string = string.lower()
    string = strip_accents(string)
    string = re.sub("[0-9]", "", string)
    string = re.sub("[^a-z]", " ", string)
    return string
    
    
def LD(s, t): 
    res = levenshtein.distance(s, t)
    return res