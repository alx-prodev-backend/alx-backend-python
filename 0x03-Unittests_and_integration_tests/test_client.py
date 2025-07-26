#!/usr/bin/env python3
"""Unit tests for GithubOrgClient"""

import unittest
from unittest.mock import patch, PropertyMock
from client import GithubOrgClient


class TestGithubOrgClient(unittest.TestCase):
    """
    Test the _public_repos_url property in GithubOrgClient.
    """

    def test_public_repos_url(self):
        """Test that _public_repos_url returns correct repos_url"""

        with patch('client.GithubOrgClient.org', new_callable=PropertyMock) as mock_org:
            mock_org.return_value = {
                "repos_url": "https://api.github.com/orgs/testorg/repos"
            }

            client = GithubOrgClient("testorg")
            result = client._public_repos_url

            self.assertEqual(result, "https://api.github.com/orgs/testorg/repos")


if __name__ == '__main__':
    unittest.main()
