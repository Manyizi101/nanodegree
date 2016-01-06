"""
Your task in this exercise has two steps:

- audit the OSMFILE and change the variable 'mapping' to reflect the changes needed to fix
    the unexpected street types to the appropriate ones in the expected list.
    You have to add mappings only for the actual problems you find in this OSMFILE,
    not a generalized solution, since that may and will depend on the particular area you are auditing.
- write the update_name function, to actually fix the street name.
    The function takes a string with street name as an argument and should return the fixed name
    We have provided a simple test so that you see what exactly is expected
"""
import xml.etree.cElementTree as ET
from collections import defaultdict
import re
import pprint

OSMFILE = "data/zagreb_croatia.osm"
street_type_re = re.compile(r'\b\S+\.?$', re.IGNORECASE)


#expected = ["Street", "Avenue", "Boulevard", "Drive", "Court", "Place", "Square", "Lane", "Road",
#            "Trail", "Parkway", "Commons"]

expected = ["ulica", "prolaz", "trg", "cesta", "avenija", "park", "put", "stube", "prilaz", "aleja", "perivoj", "zavoj", "ugao", "odvojak"]

# UPDATE THIS VARIABLE
mapping = { "Ul.": "Ulica",
            "Ul":"Ulica",
            "Av.":"Avenija"
            }


def audit_street_type(street_types, street_name):
    found = False
    for name in expected:
        idx = street_name.lower().find(name)
        if idx >= 0:
            found = True
    if street_name.lower().strip().find(' ') < 0:
        found = True
    if found == False and (street_name not in street_types):
        street_types.add(street_name)
        print street_name




def is_street_name(elem):
    return (elem.attrib['k'] == "addr:street")


def audit(osmfile):
    osm_file = open(osmfile, "r")
    street_types = set()
    for event, elem in ET.iterparse(osm_file, events=("start",)):

        if elem.tag == "node" or elem.tag == "way":
            for tag in elem.iter("tag"):
                if is_street_name(tag):
                    audit_street_type(street_types, tag.attrib['v'])

    return street_types


def update_name(name, mapping):

    # YOUR CODE HERE

    for key in mapping:
        indexes = [match.start() for match in re.finditer(re.escape(key), name)]
        if len(indexes) > 0:
            name = name[:indexes[0]]
            name = name + mapping[key]

    return name


def test():
    st_types = audit(OSMFILE)
    #assert len(st_types) == 3
    #pprint.pprint(dict(st_types))

    for st_type, ways in st_types.iteritems():
        for name in ways:
            better_name = update_name(name, mapping)
            #print name, "=>", better_name
            # if name == "West Lexington St.":
            #     assert better_name == "West Lexington Street"
            # if name == "Baldwin Rd.":
            #     assert better_name == "Baldwin Road"


if __name__ == '__main__':
    test()