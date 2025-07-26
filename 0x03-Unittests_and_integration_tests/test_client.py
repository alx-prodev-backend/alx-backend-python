#!/usr/bin/env python3
"""
Module to test GithubOrgClient class from clients.py using unit and integration tests.
"""

import unittest
from unittest.mock import patch
from parameterized import parameterized_class

from clients import GithubOrgClient
from fixtures import TEST_PAYLOAD


@parameterized_class([
    {"org_payload": TEST_PAYLOAD[0],
     "repos_payload": TEST_PAYLOAD[1],
     "expected_repos": ["repo1", "repo2"],
     "apache2_repos": ["repo2"]}
])
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """Integration test class for GithubOrgClient.public_repos"""

    @classmethod
    def setUpClass(cls):
        """Patch get_json and set side effects before any test runs"""
        cls.get_patcher = patch("utils.get_json")
        cls.mock_get = cls.get_patcher.start()
        cls.mock_get.side_effect = [cls.org_payload, cls.repos_payload]

        cls.client = GithubOrgClient("testorg")

    @classmethod
    def tearDownClass(cls):
        """Stop patching get_json after all tests"""
        cls.get_patcher.stop()

    def test_public_repos(self):
        """Test that public_repos returns expected repo names"""
        self.assertEqual(self.client.public_repos(), self.expected_repos)

    def test_public_repos_with_license(self):
        """Test that public_repos returns repos filtered by license"""
        repos = self.client.public_repos(license="apache-2.0")
        self.assertEqual(repos, self.apache2_repos)
