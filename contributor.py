import json
import matplotlib.pyplot as plt
import sys

from util import make_request


class Contributor:
    def __init__(self, type, contributions=0):
        """
        Parameters:
        type: type of contributor (User, Anonymous)
        contributions: number of contributions (commits) in the repo
        """
        self.type = type
        self.contributions = contributions
        self.commits = None


class UserContributor(Contributor):
    def __init__(self, login, id, url, repos_url, 
        site_admin, contributions=0):
        """
        Parameters:
        login: login of the contributor
        id: id of the contributor
        url: github url of the contributor
        repos_url: github url of contributor's repositories
        site_admin: true if the contributor is an admin
        contributions: number of contributions (commits) in the repo
        """

        super().__init__("User", contributions)
        self.login = login
        self.id = id 
        self.url = url
        self.repos_url = repos_url
        self.site_admin = site_admin 


class AnonymousContributor(Contributor):
    def __init__(self, email, name, contributions=0):
        """
        Parameters:
        email: email of the contributor
        name: name of the contributor
        contributions: number of contributions (commits) in the repo
        """
        super().__init__("Anonymous", contributions)
        self.email = email
        self.name = name 


def get_contributor_from_dict(contributor):
    """
    Paramaters:
    contributor: dictionary 

    Returns:
    object UserContributor or AnonymousContributor or nothing 
    if contributor is null 
    """

    if contributor:
        if contributor["type"] == "User" or contributor["type"] == "Bot":
            login = contributor["login"]
            id = contributor["id"] 
            url = contributor["url"]
            repos_url = contributor["repos_url"]
            site_admin = contributor["site_admin"]
            return UserContributor(login, id, url, repos_url, 
                site_admin)
        elif contributor["type"] == "Anonymous":
            email = contributor["email"]
            name = contributor["name"]
            return AnonymousContributor(email, name)
        else: 
            print("OTHER TYPE")
    else: 
        pass


def get_contributors(token):
    """
    Parameters:
    token: authorization token

    Returns:
    list of Contributor objects
    """

    i = 1
    contributors_list = []

    while True:
        params = {
            "per_page": "100",
            "page": str(i),
            "anon": "1"
        }
        url = "https://api.github.com/repos/facebook/react/contributors"
        contributors = make_request(url, token, params=params)
        
        print("REQUEST FOR " + str(i) + " PAGE OK")

        if not contributors:
            break

        i += 1

        for contributor in contributors:
            print(contributor)
            if contributor["type"] == "User" or contributor["type"] == "Bot":
                login = contributor["login"]
                id = contributor["id"]
                url = contributor["url"]
                repos_url = contributor["repos_url"]
                site_admin = contributor["site_admin"]
                contributions = contributor["contributions"]
                contributor_obj = UserContributor(
                    login, id, url, repos_url, site_admin, contributions
                )
            elif contributor["type"] == "Anonymous":
                email = contributor["email"]
                name = contributor["name"]
                contributions = contributor["contributions"]
                contributor_obj = AnonymousContributor(
                    email, name, contributions
                )
                
            
                contributors_list.append(contributor_obj)

    return contributors_list


def read_json_contributors():
    """
    Returns:
    json object with the contributors
    """
    with open("contributors.json") as f:
        contributors = json.load(f)

    return contributors


def visualize_contributions():
    """
    This function plots a circular diagram with contributions of
    contributors. 
    """
    contributors = read_json_contributors()
    anonymous = 0
    bots = 0
    others = 0
    labels = []
    values = []
    for contributor in contributors:
        if contributor["type"] == "Anonymous":
            anonymous += 1
            contributors.remove(contributor)
        elif contributor["type"] == "Bot":
            bots += 1
            contributors.remove(contributor)
        elif contributor["contributions"] < 300:
            others += 1
            contributors.remove(contributor)
        else:
            labels.append(contributor["login"])
            values.append(contributor["contributions"])

    labels += ["anonymous", "bots", "others"]
    values += [anonymous, bots, others]

    plt.pie(values, labels=labels, autopct='%1.1f%%')
    plt.title("Contributions des contributeurs au repo facebook/react")
    plt.savefig("contributions.png")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Please give an authentification token from github api")
        exit(1)
    
    token = sys.argv[1]

    #contributors = get_contributors(token)
    #write_to_json("contributors.json", contributors)

    #visualize_contributions()