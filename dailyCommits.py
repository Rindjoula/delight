import calendar
import datetime
import json
import os 
import sys

from commit import Commit
from contributor import get_contributor_from_dict
from contributor import read_json_contributors
from util import make_request
from util import read_from_json
from util import write_to_json


def get_commits_per_contributor(token, contributor):
    """
    Parameters: 
    token: authorization token
    contributor: contributor for which we want their commits

    Returns:
    contributor name + list of commits
    """
    if contributor.type == "User":
            c = contributor.login
            c_name = c
    else:
        c = contributor.email
        c_name = contributor.name.replace(' ', '')

    r = "https://api.github.com/repos/facebook/react/commits?author={}"\
            .format(c)
    
    commits = make_request(r, token)
    commits_list = []

    for commit in commits:
        sha = commit["sha"]
        date = commit["commit"]["author"]["date"]
        commit_obj = Commit(sha, date, contributor)
        commits_list.append(commit_obj)

    return c_name, commits_list


def get_write_commits(token):
    """
    token: authorization token
    """
    with open("contributors.json") as f:
        contributors = json.load(f)

    for contributor in contributors:
        contributor_obj = get_contributor_from_dict(contributor)
        c_name, commits = get_commits_per_contributor(token, contributor_obj)
        file_output = "commits/{}.json".format(c_name)
        write_to_json(file_output, commits)



def get_critical_days():
    """
    Returns:
    dictionary of days when there had less than 2 commits
    """

    nb_commits_per_day = {}
    commits_per_day = {}

    for f in os.listdir("commits"):
        commits = read_from_json("commits/{}".format(f))
        for commit in commits:
            date = datetime.datetime.strptime(commit["date"], 
                    "%Y-%m-%dT%H:%M:%S%z")
            day = "{}-{}-{}".format(date.year, date.month, date.day)
            if day not in commits_per_day:
                nb_commits_per_day[day] = 1
                commits_per_day[day] = [commit]
            else:
                nb_commits_per_day[day] += 1
                commits_per_day[day].append(commit)
    
    critical_days = []

    for k, v in nb_commits_per_day.items():
        if v < 2:
            critical_days.append((k, v))

    return critical_days


def analyze_commits():

    critical_days = get_critical_days()
    write_to_json("critical_days.json", critical_days)

    contributors = read_json_contributors()
    
    nb_contributors = {}

    for c in contributors:
        if c["type"] == "User":
            c_name = c["login"]
        else: 
            c_name = c["name"].replace(' ', '')
        nb_contributors[c_name] = c["contributions"]

    print(nb_contributors)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Please give an authentification token from github api")
        exit(1)

    token = sys.argv[1]
    get_write_commits(token)

    analyze_commits()