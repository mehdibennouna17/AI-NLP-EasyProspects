import regex as re
from langdetect import detect
import numpy as np
import unicodedata

class Nlp_tools:
    def algo_split_text(text, word_frequencies, cache):
        if text in cache:
            return cache[text]
        if not text:
            return 1, []
        best_freq, best_split = 0, []
        for i in range(1, len(text) + 1):
            word, remainder = text[:i], text[i:]
            
            freq = word_frequencies.get(word, None)
            if freq:
                remainder_freq, remainder = Nlp_tools.algo_split_text(
                        remainder, word_frequencies, cache)
                freq *= remainder_freq
                if freq > best_freq:
                    best_freq = freq
                    best_split = [word] + remainder
        
        cache[text] = (best_freq, best_split)
        return cache[text]

    def split_text(text, param):
        WORD_FREQUENCIES = param['word_freq_fr']
        
        split = Nlp_tools.algo_split_text(text, WORD_FREQUENCIES, dict())
        try:
            log_freq = -np.log10(split[0])
        except:
            log_freq = 100
        return log_freq, split[1]
    
    def split_name(text, param):
        WORD_FREQUENCIES = param['noms_freq_fr']
        split = Nlp_tools.algo_split_text(text, WORD_FREQUENCIES, dict())
        try:
            log_freq = -np.log10(split[0])
        except:
            log_freq = 100
        return log_freq, split[1]

    def split_first_name(text, param):
        WORD_FREQUENCIES = param['prenoms_freq_fr']
        split = Nlp_tools.algo_split_text(text, WORD_FREQUENCIES, dict())
        try:
            log_freq = -np.log10(split[0])
        except:
            log_freq = 100
        return log_freq, split[1]
    
    
    
    def check_long_numeric_key_in_text(key, text, error_max):
        if key == '':
            response, result = False, 0
        else:
            text = re.sub("[^0-9]", "", text)
            pattern = key + '{e<=' + str(error_max) + '}'
            r_check = re.compile(pattern)
            result = len(re.findall(r_check, text))
            if result > 0:
                response = True
            else:
                response = False
        return response, result

    def check_approx_mix_key_in_text(key, text, error_max=0):
        if key == '':
            response, result = False, 0
        else:
            text = str(text)
            key = str(key)
            text = text.lower()
            key = key.lower()
            text = re.sub("[^0-9a-zäåçéñöüáàâãèêëíìîïóòôõúùûæƒœÿ]", "", text)
            key = re.sub("[^0-9a-zäåçéñöüáàâãèêëíìîïóòôõúùûæƒœÿ]", "", key)
            pattern = '('+key+')' + '{e<=' + str(error_max) + '}'
            r_check = re.compile(pattern)
            result = len(re.findall(r_check, text))
            if result > 0:
                response = True
            else:
                response = False 
        return response, result

    def check_approx_text_key_in_text(key, text, error_max):
        if key == '':
            response, result = False, 0
        else:
            text = str(text)
            key = str(key)
            text = text.lower()
            key = key.lower()
            pattern = '('+key+')' + '{e<=' + str(error_max) + '}'
            r_check = re.compile(pattern)
            result = len(re.findall(r_check, text))
            if result > 0:
                response = True
            else:
                response = False
        return response, result

    def error_max(text):
        nb_letter = len(text)
        avrg_words = nb_letter / 4
        err = int(avrg_words)
        return err
    
    def check_adresse(text, adresse):
        cle = adresse
        a = cle.split()[0]
        cle = str(cle)
        
        if not a.isdigit():
            err = int((Nlp_tools.error_max(cle))/2)
        else:
            err = Nlp_tools.error_max(cle)
        
        out = Nlp_tools.check_approx_text_key_in_text(
            cle,
            text,
             err)
     
        if a.isdigit():
            if not a in text:out=(False, 0)
        return out
    
   

        
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
    
    def getemail(text):
        a = re.findall(r'[\w\.-]+@[\w\.-]+',text)
        return a
    
    def normalize_phone(phone):
        n = 2
        if len(phone) == 9:
            phone = '0' + phone
            
        elif len(phone) == 10:
            if not phone[0] == 0:
                phone = ""
        elif len(phone) == 11:
            if phone[0:2] == "33":
                phone = '0' + phone[2:]
            else:
                phone = ""
        elif len(phone) == 12:
             if phone[0:3] == "330":
                 phone = '0' + phone[3:]
             else:
                phone = ""
            
        phone = ' '.join([phone[i:i+n] for i in range(0, len(phone), n)])
        return phone    
   
    def getphone(text):
        a = re.findall(r'[\+\(]?[1-9][0-9 .\-\(\)]{8,}[0-9]',text)
        a = [re.sub("[^0-9]", "", u) for u in a if len(
            re.sub("[^0-9]", "", u)) in [9, 10, 11, 12]]
        a = [Nlp_tools.normalize_phone(str(u)) for u in a]
        a = list(set(a))
        return a
    
    def word_check(word, ratio):
        word = word.lower()
        word = word.replace(".", "")
        word = word.replace(",", "")
        word1 = word.replace("-", "")
        word1 = word1.replace("'", "")
        word1 = word1.replace(":", "")
        word1 = word1.replace("?", "")
        word1 = word1.replace("!", "")
        w = str()
        if len(word1) > 0:
            if len(re.sub("[^\-a-zäåçéñöüáàâãèêëíìîïóòôõúùûæƒœÿ']","",word1)) / len(
                                 word1) > ratio and len(word) > 1:
                w = word                
        return w
    
    def filter_text(text_list, ratio):
        text_list = [Nlp_tools.word_check(word, ratio) for word in text_list]
        text_list = [u for u in text_list if not u == str()]
        return text_list
    
    
    def lang(text):
        try:
            out = detect(text)
        except:
            out = "fr"
        return out
    
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
        string = Nlp_tools.strip_accents(string)
        string = re.sub("[0-9]", "", string)
        string = re.sub("[^a-z]", " ", string)
        return string
    
    def check_num_in(text):
        text = str(text)
        if '0' in text or '1' in text or '2' in text or '3' in text or '4' in text or '5' in text or '6' in text or '7' in text or '8' in text or '9' in text :
            out = True
        else:
            out = False
        return out 
        

