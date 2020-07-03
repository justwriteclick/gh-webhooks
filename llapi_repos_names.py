#!/usr/bin/env python

import configvar
import json
import sys
"""
Gets a list of all repos using a JSON file generated from
the Learning Labs api/gits endpoint.
"""

def get_repos(filename):

    with open(filename,'r') as json_file:
        ourjson = json.load(json_file)

    json_file.close()
    for index, value in enumerate(ourjson):
        #print("Index is: " + str(index))
        orgname = str(value['user'])
        if orgname == "CiscoDevNet":
            #print("org name is: " + str(value['user']))
            print(str(value['repo']))
        else:
            pass
    #print(type(ourjson))
    #for key in ourjson:
    #    for value in key['repo']:
    #        print(value)

def main(args):
    if not len(args) == 1:
        print("Enter the filename for the JSON file")
        return
    filename = args[0]
    get_repos(filename)
if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
