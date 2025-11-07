from bs4 import BeautifulSoup

import xml.etree.ElementTree as ET

try:
    from lxml import etree
    print('running with lxml.etree')
except ImportError:
    print('you\'re not running with lxml active')


import re
from pathlib import Path

ns = {
    'mods' : 'http://www.loc.gov/mods/v3',
    'ead3'  : 'http://ead3.archivists.org/schema/',
}



MODS_file = Path('/','Users','sarahdababneh','Desktop','si676-2025-data-main-2','data','xml','2018_lcwa_MODS_25.xml')

record_count = 0

with open(MODS_file, 'r') as xml_records:
    metadata = BeautifulSoup(xml_records, features='xml')
    for mods in metadata.find_all('mods'):
        print(mods.name, mods.title, mods.form)
        record_count += 1

print(record_count)


with open(MODS_file, 'r') as xml_records:
    metadata = BeautifulSoup(xml_records, features='xml')
    for mods in metadata.find_all('mods'):
        for identifier in mods.find_all('identifier'):
            print(identifier.name, identifier.text)

with open(MODS_file, 'r') as xml_records:
    metadata = BeautifulSoup(xml_records, features='xml')
    for mods in metadata.find_all('mods'):
        for identifier in mods.find_all('identifier'):
            print(identifier.name, identifier.text, identifier.attrs)


with open(MODS_file, 'r') as xml_records:
    metadata = BeautifulSoup(xml_records, features='xml')
    for mods in metadata.find_all('mods'):
        for identifier in mods.find_all('identifier'):
            tag = identifier.name
            content = identifier.text
            try:
                type_ = identifier.attrs['type']
            except:
                type_ = "Blank type"
            print(tag, content, type_)


with open(MODS_file, 'r') as xml_records:
    metadata = BeautifulSoup(xml_records, features='xml')
    for mods in metadata.find_all('mods'):
        for identifier in mods.find_all('identifier', type="uri"):
            print(identifier.attrs['type'], identifier.text)

xml_records = etree.parse(MODS_file)

for identifier in xml_records.findall('.//mods:identifier', namespaces=ns):
    element = identifier
    print(element.tag, element.text, element.attrib)


xml_records = etree.parse(MODS_file)

for identifier in xml_records.findall('.//mods:identifier[@type="uri"]', namespaces=ns): 
    element = identifier
    attribs = element.attrib
    type = attribs.get('type')
    print(element.tag, type, element.text)


with open(MODS_file, 'r') as xml_records:
    metadata = BeautifulSoup(xml_records, features='xml')
    for mods in metadata.find_all('mods'):
        for title in mods.find_all('title'):
            print(title.name, title.find_parent())



xml_records = etree.parse(MODS_file)
metadata = xml_records.getroot()

for mods in metadata.findall('.//mods:mods', namespaces=ns):
    for title in mods.findall('.//mods:title', namespaces=ns):
        parent = title.getparent()
        print(title.tag, parent.tag)


xml_records = etree.parse(MODS_file)

for titleInfo in xml_records.findall('.//mods:title', namespaces=ns):
    element = titleInfo
    print(element.text)



for title in xml_records.findall('.//mods:title', namespaces=ns):
    print(title.text)


with open(MODS_file, 'r') as xml_records:
    metadata = BeautifulSoup(xml_records, features='xml')
    for mods in metadata.find_all('mods'):
        title = mods.find('title')
        print(title.name, title.text)

xml_records = etree.parse(MODS_file)
metadata = xml_records.getroot()

for title in metadata.findall('.//mods:mods/mods:titleInfo/mods:title', namespaces=ns):
    print(title.text, title.tag)



large_MODS_collec = Path('/','Users','sarahdababneh','Desktop','si676-2025-data-main-2','data','xml','2018_lcwa_MODS_25.xml')



xml_records = etree.parse(large_MODS_collec)
metadata = xml_records.getroot()

for subject in metadata.findall('.//mods:subject[@authority="lcsh"]', namespaces=ns):
    print(subject.tag, subject.attrib)
    print(etree.tostring(subject, encoding='utf-8').decode('utf-8'))



xml_records = etree.parse(large_MODS_collec)
metadata = xml_records.getroot()

for subject in metadata.findall('.//mods:subject[@authority="lcsh"]', namespaces=ns):
    print(subject.tag, subject.attrib)
    for item in subject:
        print(item.tag, item.text)
    print('\n')


metadata = BeautifulSoup(open(large_MODS_collec), features='xml')

for mods in metadata.find_all('mods'):
    for subject in mods.find_all('subject', authority="lcsh"):
        print(subject, subject.attrs, '\n')


metadata = BeautifulSoup(open(large_MODS_collec), features='xml')

for mods in metadata.find_all('mods'):
    for subject in mods.find_all('subject', authority="lcsh"):
        print(subject.topic)



xml_records = etree.parse(large_MODS_collec)

for subject in xml_records.findall('.//mods:subject', namespaces=ns):
    print(subject.tag, subject.attrib)


xml_records = etree.parse(large_MODS_collec)

for subject in xml_records.findall('.//mods:subject[@authority="lcsh"]', namespaces=ns):
    print(subject.tag, len(subject), subject.attrib)



xml_records = etree.parse(large_MODS_collec)
count = 0

for subject in xml_records.findall('.//mods:subject[@authority="lcsh"]', namespaces=ns):
    count += 1
    print(subject.tag, count, 'children:')
    print(f'  type: {subject.attrib["authority"]}')
    for subelement in subject:
        print(f'  {subelement.tag.split("}")[1]} - {subelement.text}')
    print('\n')
    if count > 4:
        break


with open(large_MODS_collec, 'r') as xml_records:
    metadata = BeautifulSoup(xml_records, features='xml')

    for mods in metadata.find_all('mods'):
        for identifier in mods.find_all('identifier'):
            print(identifier.name, identifier.text, identifier.attrs)



call_num_pattern = re.compile(r'^blcwaN\d{7}')

with open(large_MODS_collec, 'r') as xml_records:
    metadata = BeautifulSoup(xml_records, features='xml')

    for mods in metadata.find_all('mods'):
        for identifier in mods.find_all('identifier'):
            if re.match(call_num_pattern, identifier.text):

                identifier['type'] = 'local_call_number'
                identifier['invalid'] = 'no'
                identifier['displaylabel'] = 'Local Call Number'
                print(identifier.prettify())
                print('  ',identifier.attrib)

newfile = Path('/','Users','sarahdababneh','Desktop','si676-2025-data-main-2','data','xml','NEW_2018_lcwa_MODS_25.xml')

call_num_pattern = re.compile(r'[a-z]{4}N\d{7}')

with open(large_MODS_collec, 'r') as xml_records:
    metadata = BeautifulSoup(xml_records, features='xml')

    for mods in metadata.find_all('mods'):
        for identifier in mods.find_all('identifier'):
            if re.match(call_num_pattern, identifier.text):
                identifier['type'] = 'local_call_number'
                identifier['invalid'] = 'no'
                identifier['displaylabel'] = 'Local Call Number'


    with open(newfile, 'w') as updated_records:
        updated_records.write(metadata.prettify(formatter="minimal"))
        print("Wrote a new file, you're welcome!")
