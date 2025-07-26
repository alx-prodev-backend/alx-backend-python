#!/usr/bin/env python3
"""Integration tests for GithubOrgClient"""

import unittest
from parameterized import parameterized_class
from unittest.mock import patch
from client import GithubOrgClient

import json


def read_fixture(filename):
    """Helper to load fixture from file"""
    with open(f"fixtures/{filename}") as f:
        return json.load(f)


@parameterized_class([
    {
        "org_payload": read_fixture("org_payload.json"),
        "repos_payload": read_fixture("repos_payload.json"),
        "expected_repos": ["repo1", "repo2", "repo3"],
        "apache2_repos": ["repo2"],
    }
])
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """Integration tests"""

    @classmethod
    def setUpClass(cls):
        """Patch get_json before tests"""
        cls.get_patcher = patch("client.get_json")
        cls.mock_get_json = cls.get_patcher.start()

        # Mock get_json return values in sequence
        cls.mock_get_json.side_effect = [
            cls.org_payload,
            cls.repos_payload,
        ]

    @classmethod
    def tearDownClass(cls):
        """Stop patching"""
        cls.get_patcher.stop()

    def test_public_repos(self):
        """Test public_repos without license"""
        client = GithubOrgClient("testorg")
        self.assertEqual(client.public_repos(), self.expected_repos)

    def test_public_repos_with_license(self):
        """Test public_repos with apache-2.0 license"""
        client = GithubOrgClient("testorg")
        self.assertEqual(client.public_repos(license="apache-2.0"), self.apache2_repos)
