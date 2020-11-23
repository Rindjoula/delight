import json
from util import write_to_json 
import requests


class Contributor:
    def __init__(self, type, contributions):
        """
        Parameters:
        type: type of contributor (User, Anonymous)
        """
        self.type = type
        self.contributions = contributions
        self.commits = None


class UserContributor(Contributor):
    def __init__(self, login, id, url, repos_url, 
        site_admin, contributions):
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
    def __init__(self, email, name, contributions):
        super().__init__("Anonymous", contributions)
        self.email = email
        self.name = name 


def get_contributor_from_dict(contributor):
    """
    Paramaters:
    contributor: dictionary 

    Returns: object UserContributor or AnonymousContributor
    """

    contributions = contributor["contributions"]

    if contributor["type"] == "User":
        login = contributor["login"]
        id = contributor["id"] 
        url = contributor["url"]
        repos_url = contributor["repos_url"]
        site_admin = contributor["site_admin"]
        return UserContributor(login, id, url, repos_url, 
            site_admin, contributions)
    else:
        email = contributor["email"]
        name = contributor["name"]
        return AnonymousContributor(email, name, contributions)


def get_contributors():
    """
    Returns:
    list of Contributor objects
    """

    headers = {"Authorization": "token 3c6a26089c47f66da4de8f59b2ae7e5b759e9d2b"}
    r = "https://api.github.com/repos/facebook/react/contributors?anon=true"
    x = requests.get(r, headers=headers)
    contributors = json.loads(x.text)

    contributors_list = []

    for contributor in contributors:
        if contributor["type"] == "User":
            login = contributor["login"]
            id = contributor["id"]
            url = contributor["url"]
            repos_url = contributor["repos_url"]
            site_admin = contributor["site_admin"]
            contributions = contributor["contributions"]
            contributor_obj = UserContributor(
                login, id, url, repos_url, site_admin, contributions
            )
        else: 
            email = contributor["email"]
            name = contributor["name"]
            contributions = contributor["contributions"]
            contributor_obj = AnonymousContributor(
                email, name, contributions
            )
        
        contributors_list.append(contributor_obj)

    return contributors_list


def read_json_contributors():
    with open("contributors.json") as f:
        contributors = json.load(f)

    return contributors


if __name__ == "__main__":
    contributors = get_contributors()
    write_to_json("contributors.json", contributors)