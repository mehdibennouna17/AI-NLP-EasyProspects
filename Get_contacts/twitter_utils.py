

def clean_twitter(tw_links):
    tw_links = tw_links.split()
    tw_links = [link for link in tw_links if not link == str()]
    tw_links = [filtre(link) for link in tw_links]
    tw_links = [link for link in tw_links if not link == str()]
    tw_links = [link[0:index_of_nth_slash(link, 4)] for link in tw_links]
    tw_links = [link for link in tw_links if not link == str()]
    tw_links = list(set(tw_links))
    out = ' '.join(tw_links)
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
    black_words = [
        '/intent/tweet?',
        '/share?url=',
        'share?text=']
    out = str()
    p_cond = list()
    p_cond.append(
        url[0:19] == 'https://twitter.com' or url[0:18] == 'http://twitter.com' 
        )
    for word in black_words:
        p_cond.append(not word in url)
    p_cond.append(len(url) >= 24)
    
    p_val = True
    for val in p_cond:
        p_val *= val
    
    if p_val:
        if not url[-1] == '/':url+='/'
        out = url
    else:
        out = str()   
    return out


