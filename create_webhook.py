#!/usr/bin/env python

import configvar
import sys
import requests
import json
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
    """POST /repos/:owner/:repo/hooks"""
    api_uri = "https://api.github.com/repos/{}/{}/hooks".format(gh_orgname, repo_name)
    print("API endpoint: {}".format(api_uri))
    print("Username: {}".format(gh_username))
    print("API Key: {}".format(gh_api_key))
    session = requests.Session()
    session.auth = (gh_username, gh_api_key)


    try:
        hooks = Request('POST', api_uri, data=data)
        prepped = hooks.prepare()
        # Request body for the POST to create a webhook
        payload = {
               "name": "web",
               "active": true,
               "events": ["release"],
               "config": {
                          "url": "https://devnet-int-svcs.cisco.com/api/githubs/githubWebhook/release",
                          "content_type": "json",
                          "secret": gh_secret,
                          "insecure_ssl": "0"
                          }
               }
        prepped.body = json.dumps(payload)
        resp = session.send(prepped)
        print(payload)
        print(hooks.status_code)
        print(hooks.text)
        print(json.dumps(hooks.json(), indent=4))
    except:
        print(hooks.status_code)
        print("Response text: {}".format(hooks.text))
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
            #response = get_webhook(configvar.gh_orgname, repo_name, configvar.gh_username, configvar.gh_api_key, configvar.gh_secret)
            response = post_create_webhook(configvar.gh_orgname, repo_name, configvar.gh_username, configvar.gh_api_key, configvar.gh_secret)
if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
