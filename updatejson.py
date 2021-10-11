import json

def update_json(dictionary, location):
    temp = open(location, 'w')
    json.dump(dictionary, temp, indent = 4)
    temp.close()
    
def refresh_json(location):
    with open(location) as read_file:
            accounts = json.load(read_file)
            return accounts

def new_element(parameters):
    output = {}
    for x in parameters:
        output[str(x)] = ""
    return output

def remove_element(dictparam, element):
    try:
        return dictparam.pop(element)
    except:
        return dictparam
