#!/usr/bin/env python

import configvar
import json
from requests import Request, Session
import sys
"""
Creates webhooks in a repo upon release using
GitHub API v3 POST /repos/:owner/:repo/hooks
Requires a file with repo names, one per line,
and a user token with access to each repo.
"""

def get_webhook(gh_orgname, repo_name, gh_username, gh_api_key, gh_secret):
    api_uri = "https://api.github.com/repos/{}/{}/hooks".format(gh_orgname, repo_name)
    print(api_uri)
    session = requests.Session()
    session.auth = (gh_username, gh_api_key)
    try:
        gethooks = session.get(api_uri)
        print(json.dumps(gethooks.json(), indent=4))
    except:
        print(gethooks.status_code)
        print("Response text: {}".format(gethooks.text))

def post_create_webhook(gh_orgname, repo_name, gh_username, gh_api_key, gh_secret):
    api_uri = "https://api.github.com/repos/{}/{}/hooks".format(gh_orgname, repo_name)
    print("API endpoint: {}".format(api_uri))
    print("Username: {}".format(gh_username))
    print("API Key: {}".format(gh_api_key))
    print("Secret for payload: {}".format(gh_secret))

    try:
        print("In the try block")

        headers = {'User-Agent': 'annegentle',
                   'content-type': 'application/json',
                   'Authorization': 'token {}'.format(gh_api_key)
        }
        print(headers)
        payload = {
               'name': 'web',
               'active': True,
               'events': ['release'],
               'config': {
                           'url': 'https://devnet-int-svcs.cisco.com/api/githubs/githubWebhook/release',
                           'content_type': 'json',
                           'secret': gh_secret,
                           'insecure_ssl': '0'
                           }
               }
        session = Session()
        makehooks = Request('POST', api_uri, data=payload, headers=headers).prepare()
        resp = session.send(makehooks)
        print(json.dumps(payload, indent=4))
        print(resp.status_code)
        print(resp.text)
        print(json.dumps(resp.json(), indent=4))
        #print(makehooks.status_code)
        #print(makehooks.text)
        #print(json.dumps(makehooks.json(), indent=4))
    except:
        print(makehooks.status_code)
        print("Response text: {}".format(makehooks.text))
        sys.exit()

def main(args):
    if not len(args) == 1:
        print("Enter the filename for the file that contains the list of repos, one per line")
        return
    filename = args[0]
    # Read data in from a text list of all LL repo names
    repolist = []
    with open(filename) as f:
        repolist = f.readlines()
        for repo in repolist:
            repo_name = repo.rstrip('\n')
            print("Working on this repo: " + repo_name)
            #getresponse = get_webhook(configvar.gh_orgname, repo_name, configvar.gh_username, configvar.gh_api_key, configvar.gh_secret)
            postresponse = post_create_webhook(configvar.gh_orgname, repo_name, configvar.gh_username, configvar.gh_api_key, configvar.gh_secret)
if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
