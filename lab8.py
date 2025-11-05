from bs4 import BeautifulSoup

import xml.etree.ElementTree as ET

ns = {
    'mods' : 'http://www.loc.gov/mods/v3',
    'ead3'  : 'http://ead3.archivists.org/schema/',
}

try:
    from lxml import etree
    print('running with lxml.etree')
except ImportError:
    print('you\'re not running with lxml active')

import re
from pathlib import Path

MODS_collection = Path('/Users/sarahdababneh/Desktop/si676-2025-data-main-2','data','xml','2018_lcwa_MODS_25.xml')

mods_collec = etree.parse(MODS_collection)
metadata = mods_collec.getroot()

for item in metadata:
    print(item.tag)
    len(item.tag)

el_count = 0

for element in metadata.iter():
    el_count += 1
    print(element.tag)

print(el_count)

### 1. There are 1358 individual MODS records in the XML file.


xml_records = etree.parse(MODS_collection)
metadata = xml_records.getroot()

for subject in metadata.findall('.//mods:subject[@authority="lcsh"]', namespaces=ns):
    print(etree.tostring(subject, encoding='utf-8').decode('utf-8'))

xml_records = etree.parse(MODS_collection)
metadata = xml_records.getroot()

for subject in metadata.findall('.//mods:subject[@authority="lcsh"]', namespaces=ns):
    print(subject.tag, subject.attrib)
    for item in subject:
        print(item.tag, item.text)
    print('\n')


xml_records = etree.parse(MODS_collection)
metadata = xml_records.getroot()

for subject in xml_records.findall('.//mods:subject', namespaces=ns):
    print(subject.tag, subject.attrib)
    for item in subject:
        print(item.tag, item.text)
    print('\n')

metadata = BeautifulSoup(open(MODS_collection), features='xml')

for mods in metadata.find_all('mods'):
    for subject in mods.find_all('subject', authority="lcsh"):
        print(subject, subject.attrs, '\n')

metadata = BeautifulSoup(open(MODS_collection), features='xml')

for mods in metadata.find_all('mods'):
    for subject in mods.find_all('subject', authority="lcsh"):
        print(subject.topic)

for subject in xml_records.findall('.//mods:subject', namespaces=ns):
    print(subject.tag, subject.attrib)

xml_records = etree.parse(MODS_collection)

for subject in xml_records.findall('.//mods:subject[@authority="lcsh"]', namespaces=ns):
    print(subject.tag, len(subject), subject.attrib)

count = 0

for subject in xml_records.findall('.//mods:mods/mods:subject', namespaces=ns):
    if subject.attrib['authority'] == 'lcsh':
        count += 1
        print(subject.tag, count, 'children:')
        for subelement in subject:
            print('  ',subelement.tag)
        print('\n')
        if count > 4:
            break

for subject in xml_records.findall('.//mods:mods/mods:subject', namespaces=ns):
    if subject.attrib['authority'] == 'lcsh':
        count += 1
        print(subject.tag, count, 'children:')
        for subelement in subject:
            print(f'  {subelement.tag.split("}")[1]} - {subelement.text}')
        print('\n')
        if count > 4:
            break


with open(MODS_collection, 'r') as xml_records:
    metadata = BeautifulSoup(xml_records, features='xml')

    for mods in metadata.find_all('mods'):
        for identifier in mods.find_all('identifier'):
            print(identifier.name, identifier.text, identifier.attrs)


call_num_pattern = re.compile(r'^lcwa[A-Z]\d{7}')

with open(MODS_collection, 'r') as xml_records:
    metadata = BeautifulSoup(xml_records, features='xml')

    for mods in metadata.find_all('mods'):
        for identifier in mods.find_all('identifier'):
            if re.match(call_num_pattern, identifier.text):
                print(identifier.name, identifier.text, identifier.attrs)


    for mods in metadata.find_all('mods'):
        for identifier in mods.find_all('identifier'):
            if re.match(call_num_pattern, identifier.text):

                identifier['type'] = 'local_call_number'
                identifier['invalid'] = 'no'
                identifier['displaylabel'] = 'Local Call Number'
                identifier['updated'] = 'true'

                print(identifier.name, identifier.text, identifier.attrs)

    for mods in metadata.find_all('mods'):
        for identifier in mods.find_all('identifier'):
            if re.match(call_num_pattern, identifier.text):

                identifier['type'] = 'local_call_number'
                identifier['invalid'] = 'no'
                identifier['displaylabel'] = 'Local Call Number'
                print(identifier.prettify())


xml_records = etree.parse(MODS_collection)
for identifier in xml_records.findall('.//mods:mods/mods:identifier', namespaces=ns):
        if re.match(call_num_pattern, identifier.text):
            print(identifier.text)
        else:
            print(f'invalid LCCN: { identifier.text }')

for identifier in xml_records.findall('.//mods:mods/mods:identifier', namespaces=ns):
    if re.match(call_num_pattern, identifier.text):
        print(identifier.text)
        identifier.attrib['displaylabel'] = 'Local Call Number'
        identifier.attrib['invalid'] = 'no'
        identifier.attrib['type'] = 'local_call_number'
        print('  ',identifier.attrib)

for identifier in xml_records.findall('.//mods:mods/mods:identifier', namespaces=ns):
    print(identifier.text)
    if re.match(call_num_pattern, identifier.text):
        print(identifier.tag, identifier.text, identifier.attrib)



newfile = Path('/Users/sarahdababneh/Desktop/si676-2025-data-main-2','data','xml','2018_lcwa_MODS_25_updatedlxml.xml')


call_num_pattern = re.compile(r'[a-z]{4}N\d{7}')


ET.register_namespace('mods','http://www.loc.gov/mods/v3')
ET.register_namespace('ead3', 'http://ead3.archivists.org/schema/')

metadata = etree.parse(MODS_collection)
xml_records = metadata.getroot()

for mods in xml_records.findall('mods:mods', namespaces=ns):
    for identifier in mods.find('.//mods:identifier', namespaces=ns):
        if re.match(call_num_pattern, identifier.text):

            identifier.set('type', 'local_call_number')
            identifier.set('invalid', 'no')
            identifier.set('displaylabel', 'Local Call Number')
            identifier.set('updated', 'true')


metadata.write(newfile, xml_declaration=True, encoding='utf-8', method='xml')
print("Wrote a new file!")