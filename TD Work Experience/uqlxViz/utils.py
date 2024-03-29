import random


# these are valid currencies for large JSON must be changed!!!!!
_validCurrencies = ["USD", "JPY", "EUR", "CAD" ]

# check is a currency
def is_currency(x):
    if len(x) != 3:
        return  False
    else:
        return x in _validCurrencies

# check if a currency pair
def is_ccypair(x):
    if len(x) != 6:
        return  False
    else:
        return is_currency(x[0:3]) and is_currency(x[3:6])



# generalised dictionary extract , find-all-occurrences-of-a-key-in-nested-python-dictionaries-and-lists
# dcs = list(utils.gen_dict_extract(_dc_key, model_d))
def gen_dict_extract(key, var):

    if hasattr(var,'items'):
        for k, v in var.items():
            if k == key:
                yield v
            if isinstance(v, dict):
                for result in gen_dict_extract(key, v):
                    yield result
            elif isinstance(v, list):
                for d in v:
                    for result in gen_dict_extract(key, d):
                        yield result
    
                        

# random hex colour gen
def random_colour():
    possible_chars = ["0",'1','2','3','4','5','6','7','8','9','a','b','c','d','e','f']
    full_str = "#"
    for counter in range(6):
        rand = random.randint(0,15)
        full_str += possible_chars[rand]
    return full_str
    



# checks in list - few place to replace with this
def check_in_list(item, dataList):
    if item in dataList:
        return True
    else:
        return False

# takes longer filename and recudes it so it can be used as a curvename in explorer
def extract_file_name(filename):
    filename = str(filename)
    for index in range(0, len(filename)-1 ,1):
        if filename[index] =="/":
            fname = filename[index+1:]
    return(fname)
