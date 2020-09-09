#!/usr/bin/env python

import config
import json
import sys
"""
Creates a list of all repos using a JSON file generated from
the Learning Labs api/gits endpoint.
Usage:
python llapi_repos_names.py llgitsresponse.json > devnet_repos.txt
"""

def get_repos(filename):
    with open(filename,'r') as json_file:
        ourjson = json.load(json_file)
    json_file.close()
    for index, value in enumerate(ourjson):
        orgname = str(value['user'])
        if orgname == "CiscoDevNet":
            print(str(value['repo']))
        else:
            pass

def main(args):
    if not len(args) == 1:
        print("Enter the filename for the JSON file to read in")
        return
    filename = args[0]
    get_repos(filename)
if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
