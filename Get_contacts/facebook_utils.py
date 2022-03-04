import regex as re
import utils



words_to_clean = {'/pages/' : '/'}
    
    
def clean_facebook(rs, fb_links):
    words_to_clean = {'/pages/' : '/'}
    fb_links = fb_links.split()
    fb_links = [filtre(link) for link in fb_links]
    fb_links = [clean(link, words_to_clean) for link in fb_links]
    fb_links = [link[0:index_of_nth_slash(link, 4)] for link in fb_links]
    fb_links = list(set(fb_links))
    fb_links = [link for link in fb_links if not link == str() ]
    
    fb_linkss = [[u[33:],u] for u in fb_links]
    fb_linkss = [[utils.format_web_str(l[0]),l[1]] for l in fb_linkss]
    fb_linkss = [l for l in fb_linkss if len(l[0])>= 3]
    rs = utils.format_web_str(rs)
    best_dist = 100
    out = str()
    for l in fb_linkss:
        dist = utils.LD(l[0], rs)
        if dist < best_dist:
            out = l[1]
            best_dist = dist
    return out


def tag(url, tag):
    out = 0
    if tag in url:
        out = 1
    else:
        out = 0
    return out

def clean(url, clean_dict):
    for u in clean_dict:
        url = re.sub(u, clean_dict[u], url)
    return url

def index_of_nth_slash(url, n):
    if '/' in url:
        url_list = [u for u in url]
        slash_indexes = list()
        for i, letter in enumerate(url_list):
            if letter == '/':slash_indexes.append(i)
        out = slash_indexes[n-1] 
    else:
        out = 0
    return out

def filtre(url):
    url = url.lower()
    black_words = [
    "share.php?",
    "sharer.php?",
    "login.php?",
    'hashtag',
    'facebook.com/dialog',
    'l.facebook.com'
    ]
    out = str()
    p_cond = list()
    p_cond.append(url[0:8] == "https://")
    for word in black_words:
        p_cond.append(not word in url)
    p_cond.append(len(url) >= 26)
    
    p_val = True
    for val in p_cond:
        p_val *= val
    
    if p_val:
        if not url[-1] == '/':url+='/'
        out = url
    else:
        out = str()   
    return out


