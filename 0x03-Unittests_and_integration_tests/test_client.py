#!/usr/bin/env python3
"""Integration tests for GithubOrgClient"""

import unittest
from unittest.mock import patch
from parameterized import parameterized_class
from client import GithubOrgClient
from fixtures import TEST_PAYLOAD


@parameterized_class([
    {
        "org_payload": TEST_PAYLOAD[0]["org_payload"],
        "repos_payload": TEST_PAYLOAD[0]["repos_payload"],
        "expected_repos": TEST_PAYLOAD[0]["expected_repos"],
        "apache2_repos": TEST_PAYLOAD[0]["apache2_repos"],
    }
])
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """Integration test class for GithubOrgClient"""

    @classmethod
    def setUpClass(cls):
        """Start patching requests.get and set side effects"""
        cls.get_patcher = patch("requests.get")
        cls.mock_get = cls.get_patcher.start()

        # Mocked responses in the correct order
        cls.mock_get.side_effect = [
            MockResponse(cls.org_payload),
            MockResponse(cls.repos_payload)
        ]

    @classmethod
    def tearDownClass(cls):
        """Stop patching"""
        cls.get_patcher.stop()

    def test_public_repos(self):
        """Test that public_repos returns all repository names"""
        client = GithubOrgClient("google")
        self.assertEqual(client.public_repos(), self.expected_repos)

    def test_public_repos_with_license(self):
        """Test filtering repos by license"""
        client = GithubOrgClient("google")
        result = client.public_repos(license="apache-2.0")
        self.assertEqual(result, self.apache2_repos)


class MockResponse:
    """MockResponse mimics `requests.Response.json()`"""
    def __init__(self, json_data):
        self._json = json_data

    def json(self):
        return self._json
