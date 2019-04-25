import requests
import pandas as pd
from googlesearch import search
import re
from fuzzywuzzy import fuzz
import time

"""
script to create google search based off record
if google results yield url with source of same name
append possible url to record
"""

USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36'

df = pd.read_excel('sheets/bad_urls.xls')
poss_url = []
prom_urls = []
# LENGTH = len(df['source_url'])


def get_possible_urls():
    # must send index value from query looper
    index = 1

    for row_index in range(index, len(df['source_url'])):
        row = df.iloc[row_index]
        # remove http:// if any from url
        full_url = str(row['source_url']).replace('http://', '').strip()
        url_domain = full_url.split('/')[0]
        query = "{} site: {}".format(str(row['title']), url_domain)
        try:
            url_results = [url for url in search(query, stop=10, user_agent=USER_AGENT, pause=5.0)]
            refined_urls = source_check(url_results, url_domain)
            check_for_prom_urls(refined_urls, row['title'], url_domain)
            poss_url.append(refined_urls)
            index += 1
        except Exception as e:
            print(index)
            print(e.args)
            return index


def source_check(url_results, source_url):
    refined_urls = set()
    for url in url_results:
        try:
            if source_url == "":
                return
            r = re.search(source_url, url)
            if r:
                refined_urls.add(url)
        except Exception as e:
            print("problem with url: {}".format(source_url))
    return refined_urls


def check_for_prom_urls(refined_urls, title, url_domain):
    promising_urls = set()

    for url in refined_urls:
        # clean urls of domain and http
        for r in (("http://", ""), ("https://", ""), (url_domain, "")):
            url_l_half = url.replace(*r)
        ratio = fuzz.ratio(url_l_half, title)
        if ratio > 55:
            promising_urls.add(url)
    prom_urls.append(promising_urls)


def combine_df_to_dicts(index):
    global df
    # df = df.iloc[:, ]
    # df['promising_urls'] = prom_urls
    # df['possible_urls'] = poss_url
    # modify copy not global df
    #
    dfCopy = df.iloc[:index, ]
    dfCopy['promising_urls'] = prom_urls
    dfCopy['possible_urls'] = poss_url
    # hack copied part off global df
    df = df.iloc[index:,]
    return dfCopy


def query_looper(doc_count):
    doc_count += 1
    index = 1
    # df is constantly being modified in place by combine_df_to_dicts so length will eventually be <
    length = len(df['source_url'])
    while index < length:
        index = get_possible_urls() # modifies df inplace
        dfCopy = combine_df_to_dicts(index)
        dfCopy.to_excel('sheets/poss_urls{}.xls'.format(doc_count))
        time.sleep(15)
        query_looper(doc_count)


if __name__ == '__main__':
    query_looper(0)
