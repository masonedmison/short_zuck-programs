import pandas as pd
import requests

"""
This script checks URL's for records in the Zuckerberg Transcripts Archive for validity
"""

# load in batch revise xls as Pandas df
df = pd.read_excel('sheets/zuck.xls')
urls = df['source_url']
bad_urls = pd.DataFrame(columns=df.columns)

print(bad_urls.shape)


# iterate through list and if request response IS NOT 200 then append associated record with url to new dictionary
for i, url in enumerate(urls):
    try:
        response = requests.get(url, timeout=20, allow_redirects=False)
        if response.status_code != 200:
            bad_urls = bad_urls.append(df.iloc[i])
    except Exception as e:
        # if exception then URL is probably bad, so append to bad_urls
        bad_urls = bad_urls.append(df.iloc[i])
        print('exception: {}'.format(df.iloc[i]['title']))

# to excel
bad_urls.to_excel('sheets/bad_urls.xls')

