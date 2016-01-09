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
import pprint
import re
import codecs
import json

###############################################################################################################

OSMFILE = "data/zagreb_croatia.osm"

expected_street_types = ["ulica", "prolaz", "trg", "cesta", "avenija", "park", "put",
                         "stube", "prilaz", "aleja", "perivoj", "zavoj", "ugao", "odvojak"]

abbreviation_mapping = {"Ul.": "Ulica",
                        "Av.": "Avenija"}


###############################################################################################################

def street_types_from_file(osmfile):
    osm_file = open(osmfile, "r")

    street_types_count = {"ulica": 0, "prolaz": 0, "trg": 0, "cesta": 0,
                          "avenija": 0, "park": 0, "put": 0, "stube": 0,
                          "prilaz": 0, "aleja": 0, "perivoj": 0, "zavoj": 0,
                          "ugao": 0, "odvojak": 0, "error": 0}

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
            # when street type is not mentioned we default to type "ulica" by Croatia's convention
            # "ulica" is equivalent to "Street"
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
# CREATING LIST OF DICTIONARIES FROM XML DATA
###############################################################################################################

lower = re.compile(r'^([a-z]|_)*$')
lower_colon = re.compile(r'^([a-z]|_)*:([a-z]|_)*$')
problemchars = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')


###############################################################################################################

def create_list_of_dictionaries_from_xml_file(file_in, pretty = False):
    # You do not need to change this file
    file_out = "{0}.json".format(file_in)
    data = []
    with codecs.open(file_out, "w") as fo:
        for _, element in ET.iterparse(file_in):
            el = shape_element(element)
            if el:
                data.append(el)
                if pretty:
                    fo.write(json.dumps(el, indent=2)+"\n")
                else:
                    fo.write(json.dumps(el) + "\n")
    return data


###############################################################################################################

def shape_element(element):
    node = {}
    if element.tag == "node" or element.tag == "way":
        # YOUR CODE HERE
        keys = element.attrib.keys()
        node['id'] = element.attrib['id']
        node['type'] = element.tag
        if 'visible' in keys:
            node['visible'] = element.attrib['visible']
        if 'lon' in keys and 'lat' in keys:
            node['pos'] = [float(element.attrib['lat']),float(element.attrib['lon'])]

        node['created'] = {}
        node['created']['version'] = element.attrib['version']
        node['created']['changeset'] = element.attrib['changeset']
        node['created']['timestamp'] = element.attrib['timestamp']
        node['created']['user'] = element.attrib['user']
        node['created']['uid'] = element.attrib['uid']


        for tag in element.iter('tag'):
            k = tag.attrib['k']
            if k == 'cuisine':
                node['cuisine'] = tag.attrib['v']
            if k == 'amenity':
                node['amenity'] = tag.attrib['v']
            if k == 'name':
                node['name'] = tag.attrib['v']
            if k == 'phone':
                node['phone'] = tag.attrib['v']
            if lower_colon.match(k) and k.startswith('addr:'):
                if 'address' not in node:
                    node['address'] = {}
                node['address'][k[5:]] = tag.attrib['v']

        for tag in element.iter('nd'):
            if 'node_refs' not in node:
                node['node_refs'] = []
            node['node_refs'].append(tag.attrib['ref'])

        return node
    else:
        return None


###############################################################################################################
# CREATING MONGODB
###############################################################################################################

from pymongo import MongoClient

JSON_GENERATED_FROM_XML = 'data/zagreb_croatia.osm.json'


###############################################################################################################

def get_current_mongo_db_instance():
    client = MongoClient('mongodb://localhost:27017')
    db = client.new_db
    return db


###############################################################################################################

def initialize_mongo_db():
    db = get_current_mongo_db_instance()

    data = []
    with open(JSON_GENERATED_FROM_XML, 'r') as f:
        for line in f:
            data.append(json.loads(line))

    db.locations.insert_many(data)

    print 'Database initialized ...'


###############################################################################################################

def mongo_db_make_aggregation_query(query):
    db = get_current_mongo_db_instance()
    entries = db.locations.aggregate(query)

    i = 0
    for en in entries:
        if i < 3:
            i += 1
            pprint.pprint(en)
    print '\n'


###############################################################################################################

def mongo_db_drop_collection():
    db = get_current_mongo_db_instance()
    db.locations.drop()


###############################################################################################################




def save_data_to_file(data):
    with open('list_of_dictionaries_zagreb', 'w') as f:
        for item in data:
            f.write("%s\n" % item)




if __name__ == '__main__':
    # test()
    # process_map(OSMFILE)
    #pprint.pprint(street_types_from_file(OSMFILE))
    #count_unique_users(OSMFILE)
    #data = create_list_of_dictionaries_from_xml_file(OSMFILE)

    #mongo_db_drop_collection()
    #initialize_mongo_db()
    # mongo_db_make_aggregation_query([{'$match': {"amenity": "kindergarten",
    #                                              "created.user": "Matija Nalis"}},
    #                                  {'$limit': 10}])
    #
    # mongo_db_make_aggregation_query([{'$match': {"amenity": "kindergarten"}},
    #                                  {'$group': {'_id': '$amenity',
    #                                              'count': {'$sum': 1}}}])
    #
    # mongo_db_make_aggregation_query([{'$match': {"amenity": "school"}},
    #                                  {'$group': {'_id': '$amenity',
    #                                              'count': {'$sum': 1}}}])
    #
    # mongo_db_make_aggregation_query([{'$match': {"amenity": "pub"}},
    #                                  {'$group': {'_id': '$amenity',
    #                                              'count': {'$sum': 1}}}])
    #
    # mongo_db_make_aggregation_query([{'$match': {"amenity": "cafe"}},
    #                                  {'$group': {'_id': '$amenity',
    #                                              'count': {'$sum': 1}}}])

    db = get_current_mongo_db_instance()
    # print '\nNumber of documents: ' + str(db.locations.find().count())
    # print 'Number of nodes: ' + str(db.locations.find({"type": "node"}).count())
    # print 'Number of ways: ' + str(db.locations.find({"type": "way"}).count()) + '\n'
    #
    # mongo_db_make_aggregation_query([{'$match': {"created.user": {'$exists': 1}}},
    #                                  {'$group': {'_id':'$created.user',
    #                                             'count':{'$sum': 1}}},
    #                                  {'$group': {'_id': 'Number of unique users',
    #                                             'count': {'$sum': 1}}}])
    print 'Top 3 contributing users:'
    mongo_db_make_aggregation_query([{'$group': {'_id':'$created.user',
                                                 'count':{'$sum': 1}}},
                                     {'$sort': {'count': -1}},
                                     {'$limit': 3}])

    print 'Minimum number of posts per user:'
    mongo_db_make_aggregation_query([{'$group': {'_id': '$created.user',
                                                 'count': {'$sum': 1}}},
                                     {'$sort': {'count': 1}},
                                     {'$limit': 1}])

    mongo_db_make_aggregation_query([{'$group': {'_id': '$created.user',
                                                 'count': {'$sum': 1}}},
                                     {'$match': {'count': {'$eq': 3}}},
                                     {'$group': {'_id':'Users having three posts',
                                                 'count':{'$sum': 1}}}])

    print 'Top 10 users contribution sum:'
    mongo_db_make_aggregation_query([{'$group': {'_id': '$created.user',
                                                 'count': {'$sum': 1}}},
                                     {'$sort': {'count': -1}},
                                     {'$limit': 10},
                                     {'$group': {'_id': 'Sum of top 10 users contributions',
                                                 'sum_all': {'$sum': '$count'}}}])

    print 'Top 3 amenities:'
    mongo_db_make_aggregation_query([{'$match':{'amenity':{'$exists': 1}}},
                                     {'$group': {'_id':'$amenity',
                                                 'count':{'$sum': 1}}},
                                     {'$sort': {'count': -1}},
                                     {'$limit': 3}])

    print 'Most popular cafe chain:'
    mongo_db_make_aggregation_query([{'$match':{'amenity': {'$exists': 1},
                                                'amenity': 'cafe'}},
                                     {'$group': {'_id': '$name',
                                                 'count': {'$sum': 1}}},
                                     {'$sort': {'count': -1}},
                                     {'$limit': 3}])





    # pprint.pprint(data[2384])
    # print '----------------------'
    # pprint.pprint(data[2813])
    # print '----------------------'
    # pprint.pprint(data[2926])
    # print '----------------------'