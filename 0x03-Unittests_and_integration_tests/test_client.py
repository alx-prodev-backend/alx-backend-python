from unittest import TestCase
from parameterized import parameterized_class
import fixtures
from client import GithubOrgClient
from unittest.mock import patch, Mock


@parameterized_class(
    ("org_payload", "repos_payload", "expected_repos", "apache2_repos"),
    fixtures.TEST_PAYLOAD
)
class TestIntegrationGithubOrgClient(TestCase):
    """Integration test for GithubOrgClient.public_repos"""

    @classmethod
    def setUpClass(cls):
        """Patch requests.get and set side_effects based on URL"""
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
        """Stop the patcher"""
        cls.get_patcher.stop()

    def test_public_repos(self):
        """Test public_repos returns expected repos list"""
        client = GithubOrgClient("my_org")
        self.assertEqual(client.public_repos(), self.expected_repos)

    def test_public_repos_with_license(self):
        """Test public_repos returns repos with apache-2.0 license"""
        client = GithubOrgClient("my_org")
        self.assertEqual(client.public_repos("apache-2.0"), self.apache2_repos)
