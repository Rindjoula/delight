import json 
import requests
import sys

class Contributor:
    def __init__(self, type, contributions):
        """
        Parameters:
        type: type of contributor (User, Anonymous)
        """
        self.type = type
        self.contributions = contributions

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

def get_contributors(contributors):
    """
    Parameters:
    contributors: json objects

    Returns:
    list of Contributor objects
    """

    contributors_list = []
    
    for contributor in contributors:
        if contributor["type"] == "User":
            login = contributor["login"]
            id = contributor["id"]
            url = contributor["url"]
            repos_url = contributor["repos_url"]
            type = contributor["type"]
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

if __name__ == "__main__":
    r = "https://api.github.com/repos/facebook/react/contributors?anon=true"
    x = requests.get(r)
    contributors = json.loads(x.text)
    #print(contributors)
    
    contributors_list = get_contributors(contributors)