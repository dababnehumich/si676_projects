import csv
import json
import requests
import os
from os.path import join
import glob


main_dir = os.path.join('/','Users','sarahdababneh','Desktop','si676-2025-data-main-2')
project_dir = 'collection-site-materials'
files_dir = 'item-files'
metadata_dir = 'item-metadata'

files_loc = os.path.join(main_dir,project_dir,files_dir)
print('Checking for',files_loc)

if os.path.isdir(files_loc):
    print('Files directory exists')
else:
    os.mkdir(files_loc)
    print('Created file directory:',files_loc)



search_for_metadata_here = os.path.join(project_dir,metadata_dir)

print(search_for_metadata_here)

metadata_file_list = glob.glob(search_for_metadata_here + '/*.json')

print(metadata_file_list)


item_image_urls = list()
count = 0

for item in metadata_file_list:
    with open(item, 'r', encoding='utf-8') as f:
        metadata = json.load(f)
        image_url_no = len(metadata['image_url'])
        image_url = metadata['image_url'][-1]
        item_image_urls.append(image_url)
        count += 1

print(f'Identified { str(count) } image URLs')


item_image_urls


collection_set_list_with_images = list()

for item in metadata_file_list:
    with open(item, 'r', encoding='utf-8') as item_info:
        item_metadata = json.load(item_info)

        item_metadata_dict = dict()
        item_metadata_dict['item_URI'] = item_metadata['id']
        try:
            item_metadata_dict['lccn'] = item_metadata['library_of_congress_control_number']
        except:
            item_metadata_dict['lccn'] = None
        item_metadata_dict['title'] = item_metadata['title']
        item_metadata_dict['image_URL_large'] = item_metadata['image_url'][-1]


        collection_set_list_with_images.append(item_metadata_dict)

print(collection_set_list_with_images[0])


item_count = 0
error_count = 0
file_count = 0

img_file_prefix = 'img_'

for item in collection_set_list_with_images:
        image_URL = item['image_URL_large']
        short_ID = item['item_URI'].split('/')[-2]
        print('... requesting',image_URL)
        item_count += 1

        r = requests.get(image_URL)
        if r.status_code == 200:
            img_out = os.path.join(project_dir,files_dir,str(img_file_prefix + short_ID + '.jpg'))
            with open(img_out, 'wb') as file:
                file.write(r.content)
                print('Saved',img_out)
                file_count += 1


print('--- mini LOG ---')
print('files requested:',item_count)
print('errors:',error_count)
print('files written:',file_count)






