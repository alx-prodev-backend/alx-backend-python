#!/usr/bin/env python3
"""Test for GithubOrgClient"""

import unittest
from unittest.mock import patch, PropertyMock
from client import GithubOrgClient  # ✅ بعد التعديل الصحيح

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
