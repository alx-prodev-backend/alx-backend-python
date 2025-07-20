#!/usr/bin/env python3
"""Unit test for GithubOrgClient._public_repos_url"""

import unittest
from unittest.mock import patch
from client import GithubOrgClient


class TestGithubOrgClient(unittest.TestCase):
    """Tests for GithubOrgClient"""

    def test_public_repos_url(self):
        """Test that _public_repos_url returns expected value from mocked org"""
        test_payload = {"repos_url": "https://api.github.com/orgs/testorg/repos"}

        with patch('client.GithubOrgClient.org', new_callable=property) as mock_org:
            mock_org.return_value = test_payload

            client = GithubOrgClient("testorg")
            result = client._public_repos_url

            self.assertEqual(result, test_payload["repos_url"])
