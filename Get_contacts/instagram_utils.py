
def clean_instagram(insta_links):
    insta_links = insta_links.split()
    insta_links = [filtre(link) for link in insta_links]
    insta_links = list(set(insta_links))
    out = ' '.join(insta_links)
    return out


def filtre(url):
    url = url.lower()
    black_words = ['business.instagram.com']
    out = str()
    p_cond = list()
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

