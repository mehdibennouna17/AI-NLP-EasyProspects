import re
import tldextract
import black_domains


def remove_html_tags(text):
    """Remove html tags from a string"""
    import re
    clean = re.compile('<.*?>')
    return re.sub(clean, '', text)

def root_url(url):
    root_url = 'https://www.{}/'.format(domain(url))
    return root_url
    
def domain(url):
    ext = tldextract.extract(url)
    domain_ = ext.registered_domain
    return domain_
    
def extract_data_from_search_results(search_results):
    data = list()
    domains = list()
    results = search_results['webPages']['value']
    for i, result in enumerate(results):
        new_result = dict()
        new_result['url_rank'] = result['id'].split('.')[-1]
        new_result['url'] = root_url(result['url'])
        new_result['full_url'] = result['url']
        new_result['snippet'] = remove_html_tags(result['snippet'])
        new_result['language'] = result['language']
        new_result['domain'] = domain(result['url'])
        new_result['name'] = result['name']
        new_result['isFamilyFriendly'] = result['isFamilyFriendly']
        new_result['isNavigational'] = result['isNavigational']
        if not new_result['domain'] in black_domains.black_domains:
            data.append(new_result)
            domains += [new_result['domain']]
    return data
