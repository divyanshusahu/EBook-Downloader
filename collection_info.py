import requests
import csv
import json

"""
collection can be any book url, need to improve by addind a specific url to fetch info
"""
# todo: replace by book collection info

collections = """59ccf6031555400fd895966c
59ccfc71b02e5c4fb6570892
59ccf411b02e5c4fb657088f
59ccf5015603670fbfdfbc9c
59ccff0f1782ad0fb5dc75f9
59ba31fbf7c3490f93054c81
59b2977a78d8c80fe23c0190
59ccf805b02e5c4fb6570890
59ccfb99b02e5c4fb6570891
59a7fdafd3abe11911ddbde0
59a7fbc3d18f3ac8107f411f
59cd002bfbbcf80f7ac69247
59b126e0d3abe11911ddbdec"""

collections = collections.strip().split('\n')

result = {}
for collection in collections:
    x = requests.get('HOST'.format(collection))
    x = json.loads(x.content)
    result[collection] = x['data']['collection']['query']['book']['book_id']

with open('file.csv', 'wb') as f:
    w = csv.DictWriter(f, result.keys())
    w.writeheader()
    w.writerow(result)
