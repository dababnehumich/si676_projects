import csv
import json
import requests
import os
from os.path import join

endpoint = 'https://www.loc.gov/free-to-use'
parameters = {
    'fo' : 'json'
}
collection = 'libraries'
collection_list_response = requests.get(endpoint + '/' + collection, params=parameters)
collection_list_response.url



collection_json = collection_list_response.json()

collection_json.keys()

for k in collection_json['content']['set']['items']:
    print(k)

len(collection_json['content']['set']['items'])


collection_json['content']['set']['items'][0].keys()

collection_set_list = '/Users/sarahdababneh/Desktop/si676-2025-data-main-2/collection_set_list.csv'
headers = ['image','link','title']


with open(collection_set_list, 'w', encoding='utf-8', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=headers)
    writer.writeheader()
    for item in collection_json['content']['set']['items']:


        item['title'] = item['title'].rstrip()
        writer.writerow(item)
    print('wrote',collection_set_list)


collection_csv = os.path.join('/','Users','sarahdababneh','Desktop','si676-2025-data-main-2','collection-site-materials','collection_set_list.csv')


def regenerate_collection_list(collection_csv):
    """
    Reads a CSV file and returns the data as a dictionary.

    Parameters:
    collection_csv (str): The path to the CSV file

    Returns:
    dict: A dictionary where each key is a column header and each value is a list of column values.
    """

    coll_items = list()

    with open(collection_csv, 'r', newline='', encoding='utf-8') as f:
        data = csv.DictReader(f)

        for row in data:
            row_dict = dict()
            for field in data.fieldnames:
                row_dict[field] = row[field]
            coll_items.append(row_dict)

        return coll_items

collection_set_list = regenerate_collection_list(collection_csv)
collection_set_list[0]


baseURL = 'https://www.loc.gov'
parameters = {
    'fo' : 'json'
}


item_metadata_directory = os.path.join('/','Users','sarahdababneh','Desktop','si676-2025-data-main-2','collection-site-materials','item-metadata')

if os.path.isdir(item_metadata_directory):
    print(item_metadata_directory,'exists')
else:
    os.mkdir(item_metadata_directory)
    print('created',item_metadata_directory)


item_count = 0
error_count = 0
file_count = 0

data_directory = 'collection-site-materials'
item_metadata_directory = 'item-metadata'
item_metadata_file_prefix = 'item_metadata'
json_suffix = '.json'

for item in collection_set_list:
    if item['link'] == 'link':
        continue

    if '?' in item['link']:
        resource_ID = item['link']
        short_ID = item['link'].split('/')[2]
        item_metadata = requests.get(baseURL + resource_ID, params={'fo':'json'})
        print('requested',item_metadata.url,item_metadata.status_code)
        if item_metadata.status_code != 200:
            print('requested',item_metadata.url,item_metadata.status_code)
            error_count += 1
            continue
        try:
            item_metadata.json()
        except:
            error_count += 1
            print('no json found')
            continue
        fout = os.path.join(data_directory, item_metadata_directory, str(item_metadata_file_prefix + '-' + short_ID + json_suffix))
        with open(fout, 'w', encoding='utf-8') as json_file:
            json_file.write(json.dumps(item_metadata.json()['item']))
            file_count += 1
            print('wrote', fout)
        item_count += 1
    else:
        resource_ID = item['link']
        short_ID = item['link'].split('/')[2]
        item_metadata = requests.get(baseURL + resource_ID, params={'fo':'json'})
        print('requested',item_metadata.url,item_metadata.status_code)
        if item_metadata.status_code != 200:
            print('requested',item_metadata.url,item_metadata.status_code)
            error_count += 1
            continue
        try:
            item_metadata.json()
        except:
            error_count += 1
            print('no json found')
            continue
        fout = os.path.join(data_directory, item_metadata_directory, str(item_metadata_file_prefix + '-' + short_ID + json_suffix))
        with open(fout, 'w', encoding='utf-8') as json_file:
            json_file.write(json.dumps(item_metadata.json()['item']))
            file_count += 1
            print('wrote', fout)
        item_count += 1

print('--- mini LOG ---')
print('items requested:',item_count)
print('errors:',error_count)
print('files written:',file_count)

