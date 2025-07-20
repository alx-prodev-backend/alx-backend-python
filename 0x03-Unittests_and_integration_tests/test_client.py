#!/usr/bin/env python3
import unittest
from parameterized import parameterized_class
from unittest.mock import patch, Mock
from client import GithubOrgClient
import fixtures


@parameterized_class(
    ("org_payload", "repos_payload", "expected_repos", "apache2_repos"),
    fixtures.TEST_PAYLOAD
)
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """Integration tests"""

    @classmethod
    def setUpClass(cls):
        """Set up by patching requests.get"""
        cls.get_patcher = patch("requests.get")
        mock_get = cls.get_patcher.start()

        def side_effect(url):
            mock_response = Mock()
            if url.endswith("/orgs/my_org"):
                mock_response.json.return_value = cls.org_payload
            elif url.endswith("/orgs/my_org/repos"):
                mock_response.json.return_value = cls.repos_payload
            return mock_response

        mock_get.side_effect = side_effect

    @classmethod
    def tearDownClass(cls):
        """Tear down by stopping patcher"""
        cls.get_patcher.stop()

    def test_public_repos(self):
        client = GithubOrgClient("my_org")
        self.assertEqual(client.public_repos(), self.expected_repos)

    def test_public_repos_with_license(self):
        client = GithubOrgClient("my_org")
        self.assertEqual(
            client.public_repos(license="apache-2.0"),
            self.apache2_repos
        )
