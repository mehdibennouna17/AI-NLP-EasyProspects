


def clean_youtube(yt_links):
    yt_links = yt_links.split()
    yt_links = [link for link in yt_links if not link == str()]
    yt_links = [filtre(link) for link in yt_links]
    yt_links = [link for link in yt_links if not link == str()]
    yt_links = list(set(yt_links))
    out = ' '.join(yt_links)
    return out


def filtre(url):
    url = url.lower()
    black_words = []
    out = str()
    p_cond = list()
    for word in black_words:
        p_cond.append(not word in url)
    p_cond.append(len(url) >= 28)
    
    p_val = True
    for val in p_cond:
        p_val *= val
    
    if p_val:
        if not url[-1] == '/':url+='/'
        out = url
    else:
        out = str()   
    return out


