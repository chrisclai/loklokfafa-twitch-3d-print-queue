import json

# Function updates the current json file with the new data from dictionary
def update_json(dictionary, location):
    temp = open(location, 'w')
    json.dump(dictionary, temp, indent = 4)
    temp.close()
    
# Function turns the data inside of the print queue into a returned dictionary
def refresh_json(location):
    with open(location) as read_file:
            accounts = json.load(read_file)
            return accounts

# Function adds a new element to the dictionary
def new_element(parameters):
    output = {}
    for x in parameters:
        output[str(x)] = ""
    return output

# Function will remove the first element from the dictionary and shift all elements upwards by 1
def remove_element(queuedict):
    for x in range(len(queuedict)):
        if x != 0 and x < len(queuedict) - 2:
            queuedict[str(x)]['username'] = queuedict[str(x + 1)]['username']
            queuedict[str(x)]['printlink'] = queuedict[str(x + 1)]['printlink']
            queuedict[str(x)]['printname'] = queuedict[str(x + 1)]['printname']
            queuedict[str(x)]['daterequest'] = queuedict[str(x + 1)]['daterequest']
    if len(queuedict) > 1:
        i = len(queuedict) - 1
        queuedict[str(i - 1)]['username'] = queuedict[str(i)]['username']
        queuedict[str(i - 1)]['printlink'] = queuedict[str(i)]['printlink']
        queuedict[str(i - 1)]['printaname'] = queuedict[str(i)]['printname']
        queuedict[str(i - 1)]['daterequest'] = queuedict[str(i)]['daterequest']
        queuedict.pop(str(i))
    return queuedict
