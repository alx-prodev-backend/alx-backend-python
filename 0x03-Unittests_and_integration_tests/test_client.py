#!/usr/bin/env python3
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
import unittest
from unittest.mock import patch
from parameterized import parameterized_class
from clients import GithubOrgClient
from fixtures import TEST_PAYLOAD


@parameterized_class(
    ("org_payload", "repos_payload"),
    TEST_PAYLOAD
)
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """Integration tests for GithubOrgClient"""

    @classmethod
    def setUpClass(cls):
        """Start patchers"""
        cls.get_patcher = patch("utils.get_json")
        cls.mock_get = cls.get_patcher.start()

        # Mock return values for two sequential calls to get_json
        mock_org = cls.org_payload
        mock_repos = cls.repos_payload
        cls.mock_get.side_effect = [mock_org, mock_repos]

        cls.client = GithubOrgClient("testorg")

    @classmethod
    def tearDownClass(cls):
        """Stop patchers"""
        cls.get_patcher.stop()

    def test_public_repos(self):
        """Test the public_repos method"""
        expected = [
            repo["name"] for repo in self.repos_payload
            if not repo.get("private", False)
        ]
        self.assertEqual(self.client.public_repos(), expected)

    def test_public_repos_with_license(self):
        """Test public_repos with license filter"""
        # Assuming BSD-3-Clause exists in the repos_payload license data
        filtered = [
            repo["name"] for repo in self.repos_payload
            if not repo.get("private", False)
            and repo.get("license", {}).get("key") == "bsd-3-clause"
        ]
        self.assertEqual(
            self.client.public_repos(license="bsd-3-clause"),
            filtered
        )


if __name__ == "__main__":
    unittest.main()
