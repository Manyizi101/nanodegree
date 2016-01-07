"""
Your task in this exercise has two steps:

- audit the OSMFILE and change the variable 'abbreviation_mapping' to reflect the changes needed to fix
    the unexpected street types to the appropriate ones in the expected list.
    You have to add mappings only for the actual problems you find in this OSMFILE,
    not a generalized solution, since that may and will depend on the particular area you are auditing.
- write the update_name function, to actually fix the street name.
    The function takes a string with street name as an argument and should return the fixed name
    We have provided a simple test so that you see what exactly is expected
"""
import xml.etree.cElementTree as ET
import re
import pprint

###############################################################################################################

OSMFILE = "data/zagreb_croatia.osm"

expected_street_types = ["ulica", "prolaz", "trg", "cesta", "avenija", "park", "put",
                         "stube", "prilaz", "aleja", "perivoj", "zavoj", "ugao", "odvojak"]

abbreviation_mapping = {"Ul.": "Ulica",
                        "Av.": "Avenija"}


###############################################################################################################

def street_types_from_file(osmfile):
    osm_file = open(osmfile, "r")

    street_types_count = {"ulica": 0, "prolaz": 0, "trg": 0, "cesta": 0, "avenija": 0, "park": 0, "put": 0, "stube": 0,
                          "prilaz": 0, "aleja": 0, "perivoj": 0, "zavoj": 0, "ugao": 0, "odvojak": 0, "error": 0}

    for event, elem in ET.iterparse(osm_file, events=("start",)):
        if elem.tag == "node" or elem.tag == "way":
            for tag in elem.iter("tag"):
                if is_street_name(tag):
                    sum_streets_by_type(street_types_count, tag.attrib['v'])

    print '\nStreet type count:'
    return street_types_count


###############################################################################################################

def is_street_name(elem):
    return (elem.attrib['k'] == "addr:street")


###############################################################################################################

def sum_streets_by_type(street_types_count, street_name):
    street_name = update_abbreviated_name_if_needed(street_name)

    for acceptable_name in expected_street_types:
        idx = street_name.strip().lower().find(acceptable_name)
        if idx >= 0:
            street_types_count[acceptable_name] += 1

    if street_name.lower().strip().find(' ') < 0:
        try:
            street_name_as_number = int(street_name)
            street_types_count["error"] += 1
            print 'Street type as a number error: ' + str(street_name_as_number)
        except:
            # when street type is not mentioned we default to type "ulica"
            # this is equivalent to "Street" by country's convention
            street_types_count["ulica"] += 1


###############################################################################################################

def update_abbreviated_name_if_needed(name):
    for key in abbreviation_mapping:
        index = name.find(key)
        if index >= 0:
            print name + ' => ' + name.replace(key, abbreviation_mapping[key])
            name = name.replace(key, abbreviation_mapping[key])

    return name


###############################################################################################################

def count_unique_users(filename):
    users = set()
    for _, element in ET.iterparse(filename):
        if element.tag == 'node' or element.tag == 'way' or element.tag == 'relation':
            uid = element.attrib['uid']
            # print uid
            if uid not in users:
                users.add(uid)
    print '\nNumber of unique users: ' + str(len(users))


###############################################################################################################

def process_map(filename):
    keys = set()
    for _, element in ET.iterparse(filename):
        if element.tag == "tag":
            # YOUR CODE HERE
            attribute = element.attrib['k']

            if attribute not in keys:
                keys.add(attribute)
                print attribute


###############################################################################################################

def create_json_from_xml_file(filename):
    pass


###############################################################################################################

if __name__ == '__main__':
    # test()
    # process_map(OSMFILE)
    pprint.pprint(street_types_from_file(OSMFILE))
    count_unique_users(OSMFILE)
    create_json_from_xml_file(OSMFILE)
    import os
    print os.getcwd()
