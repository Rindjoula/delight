from branch import get_all_branches_from_json
import calendar
import datetime
import json
import os 
import sys


import matplotlib.pyplot as plt

from commit import Commit
from contributor import get_contributor_from_dict
from contributor import read_json_contributors
from util import make_request
from util import read_from_json
from util import write_to_json


def write_to_json_commits_per_day(token, day):
    """
    Parameters:
    token: authorization token
    day: day of commits we want to retrieve
    """

    begin = day.replace(hour=0, minute=0, second=0)
    begin = begin.strftime("%Y-%m-%dT%H:%M:%SZ")
    end = day.replace(hour=23, minute=59, second=59)
    end = end.strftime("%Y-%m-%dT%H:%M:%SZ")

    file_output = day.strftime("%Y%m%d")

    commits_list = []

    i = 1
    while True: 
        params = {
            "per_page": "100",
            "page": str(i), 
            "since": begin,
            "until": end
        }
        url = "https://api.github.com/repos/facebook/react/commits"
        commits = make_request(url, token, params=params)
        print(commits)
        if not commits: 
            break
        
        i += 1
        nb_commits = 0
        for commit in commits:
            sha = commit["sha"]
            date = commit["commit"]["author"]["date"]
            contributor = get_contributor_from_dict(commit["author"])
            commit_obj = Commit(sha, date, contributor)
            commits_list.append(commit_obj)
            nb_commits += 1

        if nb_commits < 100: 
            break

    write_to_json("commits/" + file_output + ".json", commits_list)
    

def write_commits_per_year(token, year):
    """
    Parameters:
    token: authorization token
    """

    day_delta = datetime.timedelta(days=1)
    start_date = datetime.datetime(year, 1, 1)
    #end_date = datetime.datetime(year, 12, 31)
    end_date = datetime.datetime.now()
    end_date = end_date.replace(hour=0, minute=0, second=0, microsecond=0)

    for i in range((end_date - start_date).days + 1):
        write_to_json_commits_per_day(token, start_date + i*day_delta)


def get_critical_days():
    """
    Returns:
    dictionary of days when there had less than 2 commits
    """

    critical_days = []

    for f in os.listdir("commits"):
        commits = read_from_json("commits/{}".format(f))
        if len(commits) < 2:
            date = datetime.datetime(int(f[0:4]), int(f[4:6]), int(f[6:8]))
            date_str = datetime.datetime.strftime(date, "%Y-%m-%d")
            critical_day = {date_str: len(commits)}
            critical_days.append(critical_day)

    return critical_days
            

def get_critical_days():

    critical_days = get_critical_days()
    print(critical_days)
    print(len(critical_days))
    write_to_json("critical_days.json", critical_days)


def visualize_commits():
    for f in os.listdir("commits"):
        contributors = {}
        commits = read_from_json("commits/{}".format(f))
        date = datetime.datetime(int(f[0:4]), int(f[4:6]), int(f[6:8]))
        nb_commits = len(commits)
        for commit in commits:
            contributor = commit["contributor"]
            if contributor:
                if contributor["type"] == "User" or contributor["type"] == "Bot":
                    c = contributor["login"]
                else:
                    c = contributor["email"]
            else:
                c = "unknown"
            
            if c not in contributors:
                contributors[c] = 1
            else:
                contributors[c] += 1

    # TODO: add graphics with contribution of each contributor (contributors) per day


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Please give an authentification token from github api")
        exit(1)

    token = sys.argv[1]

    #write_commits_per_year(token, 2020)

    # get_critical_days()

    visualize_commits()