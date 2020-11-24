import json
import sys

from util import make_request
from util import write_to_json


class Branch:
    def __init__(self, name, last_commit_sha):
        """
        Parameters:
        name: name of the branch
        last_commit_sha: sha of the last commit on the branch
        """

        self.name = name
        self.last_commit = last_commit_sha

def get_all_branches(token):
    i = 0
    branches_list = []

    while True:
        params = {
            "per_page": "100",
            "page": str(i), 
        }
        url = "https://api.github.com/repos/facebook/react/branches"
        branches = make_request(url, token, params=params)

        #print(branches)

        if not branches:
            break

        i += 1

        for branch in branches: 
            name = branch["name"]
            sha_last_commit = branch["commit"]["sha"]
            branch_obj = Branch(name, sha_last_commit)
            branches_list.append(branch_obj)

    return branches_list

def get_all_branches_from_json():
    with open("branches.json") as f:
        branches = json.load(f)

    return branches


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Please give an authentification token from github api")
        exit(1)

    token = sys.argv[1]

    branches = get_all_branches(token)
    #print(branches)
    
    write_to_json("branches.json", branches)