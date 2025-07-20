#!/usr/bin/env python3
"""Test for GithubOrgClient"""
from unittest.mock import patch, PropertyMock
from client import GithubOrgClient

class TestGithubOrgClient(unittest.TestCase):
    """Unit tests for GithubOrgClient"""

    @patch('client.get_json')
    def test_public_repos(self, mock_get_json):
        """Test public_repos returns list of repo names"""

        # Mocked response from get_json
        mock_get_json.return_value = [
            {"name": "repo1"},
            {"name": "repo2"},
        ]

        # Mock _public_repos_url to return a fake URL
        with patch.object(GithubOrgClient, "_public_repos_url", new_callable=PropertyMock) as mock_url:
            mock_url.return_value = "http://fake-url.com"

            client = GithubOrgClient("myorg")
            result = client.public_repos()

            self.assertEqual(result, ["repo1", "repo2"])

            # Assert calls
            mock_get_json.assert_called_once_with("http://fake-url.com")
            mock_url.assert_called_once()
