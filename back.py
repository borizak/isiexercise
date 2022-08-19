import requests
from logging import Logger
import time
import json

logger = Logger('back logger')

# CONSTS
update_rate_minutes = 5
source_url = "https://run.mocky.io/v3/367bedbd-5bf6-4d55-a659-2eb6e4f733a2"

# GLOBALS
source_data = None 
last_update = None
next_update = time.time()
indexes = {}

 # GET and FILTERING
def GET_ALL():  
    response = requests.get(source_url)  
    ok = response.status_code == 200

    data_raw = response.content if ok else None
    if not ok:
        logger.error(f"Recieved Response from {response.url}:\n {response.status_code}.{response.text}") 
    
    # desensitizing the service to char case
    data_raw = json.loads(data_raw).get('records',[])

    # flattening entries
    #       from: {ship:{a:1,...}, position:{}}
    #       to:   {a:1,...,position:{}}
    data = []
    for entry in data_raw:
        flat_entry = entry['ship']
        flat_entry['position']= entry['position']
        data.append(flat_entry)

    return data

def GET_by_key(key_name : str, key_value: str):
    
    # fetching all data every <update_rate_minutes> minutes
    __fetch()

    
    if key_name not in indexes:
        # creating index for specific key
        __reindex(key_name)
    
    # collecting entries by the index
    res = []
    relevant_indexes = indexes[key_name].get(key_value, []) 
    for i in relevant_indexes: 
        res.append(source_data[i])
    
    return res

def GET_by_custom_qualifier(qualifier:object):
    # fetching all data every <update_rate_minutes> minutes
    __fetch()
    
    return [item for item in source_data if qualifier(item)]
    
# SERVICE
def __fetch():
    global source_data, last_update, next_update

    if next_update <= time.time(): 
        # re-fetching all data
        source_data = GET_ALL()
        if not source_data:
            raise Exception(f"Could not load data for the app.")        
        
        # droppin indexes until next GET_by_Key request
        indexes = {}
        
        # setting next time globals will be reset    
        last_update = time.time()
        next_update = last_update + 60 * update_rate_minutes   

def __reindex(key):
    global indexes

    # dropping current index for the key
    indexes[key] = {}
    
    # collecting indexes per key values
    for i in range(0, len(source_data)):
        key_val = str(source_data[i][key])
        if key_val not in indexes[key]:
            indexes[key][key_val] =[]
        indexes[key][key_val].append(i)
    
def __not_implemented_ERROR():
    raise Exception(f"Not Implemented")

# ON LOAD
__fetch()
