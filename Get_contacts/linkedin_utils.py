
import utils




def strip_accents(text):
    try:
        text = unicode(text, 'utf-8')
    except NameError: # unicode is a default on python 3 
        pass
    text = unicodedata.normalize('NFD', text)\
           .encode('ascii', 'ignore')\
           .decode("utf-8")

    return str(text)


def clean_linkedin(rs, ld_links,):
    ld_links = ld_links.split()
    ld_links = [filtre(link) for link in ld_links]
    ld_links = [link for link in ld_links if not link == str()]
    ld_links = [link[0:index_of_nth_slash(link, 5)] for link in ld_links]
    ld_links = [link for link in ld_links if not link == str()]
    ld_links = list(set(ld_links))
    ld_links_old = ld_links
    ld_linkss = [[u[33:],u] for u in ld_links]
    ld_linkss = [[utils.format_web_str(l[0]),l[1]] for l in ld_linkss]
    ld_linkss = [l for l in ld_linkss if len(l[0])>= 3]
    rs = utils.format_web_str(rs)
    best_dist = 100
    out = str()
    for l in ld_linkss:
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


def index_of_nth_slash(url, n):
    url_list = [u for u in url]
    slash_indexes = list()
    for i, letter in enumerate(url_list):
        if letter == '/':slash_indexes.append(i)
    
    if len(slash_indexes) > 4:
        out = slash_indexes[n-1]
    else:
       out = 0
    return out

def filtre(url):
    url = url.lower()
    black_words = []
    out = str()
    p_cond = list()
    p_cond.append('linkedin.com/company' in url )
    for word in black_words:
        p_cond.append(not word in url)
    p_cond.append(len(url) >= 24)
    
    p_val = True
    for val in p_cond:
        p_val *= val
    
    if p_val:
        if not url[-1] == '/':url+='/'
        if url[0:12] == 'linkedin.com': url = 'https://www.' + url
        if url[0:3] == 'www': url = 'https://' + url
        out = url
    else:
        out = str()   
    return out


