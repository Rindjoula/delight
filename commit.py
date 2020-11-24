
class Commit:
    def __init__(self, sha, date, contributor):
        """
        Parameters:
        sha: sha of the commit
        date: date of the commit 
        contributor: Contributor object
        """

        self.sha = sha
        self.date = date 
        self.contributor = contributor