#!/usr/bin/env python3
"""Test for GithubOrgClient"""

import unittest
from unittest.mock import patch, PropertyMock
from client import GithubOrgClient


class TestGithubOrgClient(unittest.TestCase):
    """Unit test for GithubOrgClient"""

    def test_public_repos_url(self):
        """Test _public_repos_url returns expected value from org"""
        test_payload = {
            "repos_url": "https://api.github.com/orgs/myorg/repos"
        }

        with patch.object(GithubOrgClient, 'org', new_callable=PropertyMock) as mock_org:
            mock_org.return_value = test_payload

            client = GithubOrgClient("myorg")
            result = client._public_repos_url

            self.assertEqual(result, test_payload["repos_url"])

    @patch("client.get_json")
    def test_public_repos(self, mock_get_json):
        """Test public_repos returns list of repo names"""
        mock_get_json.return_value = [
            {"name": "repo1"},
            {"name": "repo2"},
        ]

        with patch.object(GithubOrgClient, "_public_repos_url", new_callable=PropertyMock) as mock_url:
            mock_url.return_value = "http://fake-url.com"

            client = GithubOrgClient("myorg")
            result = client.public_repos()

            expected = ["repo1", "repo2"]
            self.assertEqual(result, expected)

            mock_get_json.assert_called_once_with("http://fake-url.com")
            mock_url.assert_called_once()
