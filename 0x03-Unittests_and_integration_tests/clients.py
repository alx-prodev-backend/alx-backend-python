# clients.py

from utils import get_json


class GithubOrgClient:
    """GitHub Organization Client"""

    ORG_URL = "https://api.github.com/orgs/{}"

    def __init__(self, org_name):
        self.org_name = org_name

    @property
    def org(self):
        """Fetch organization data"""
        return get_json(self.ORG_URL.format(self.org_name))

    @property
    def _public_repos_url(self):
        """Get repos_url from org data"""
        return self.org.get("repos_url", "")

    def public_repos(self, license=None):
        """Return list of public repo names, optionally filtered by license"""
        repos_data = get_json(self._public_repos_url)
        names = []
        for repo in repos_data:
            repo_license = repo.get("license", {})
            if license is None or (repo_license and repo_license.get("key") == license):
                names.append(repo["name"])
        return names
