#!/usr/bin/env python3
"""
Unit tests for GithubOrgClient class in client.py
"""

import unittest
from parameterized import parameterized
from unittest.mock import Mock, PropertyMock, patch
from client import GithubOrgClient
from parameterized import parameterized_class
from fixtures import (org_payload, repos_payload, expected_repos,
                      apache2_repos)


class TestGithubOrgClient(unittest.TestCase):
    """
    Unit tests for the GithubOrgClient class.
    Verifies behavior of .org, _public_repos_url, and .public_repos.
    """

    @parameterized.expand([
        ("google",),
        ("abc",),
    ])
    @patch("client.get_json")
    def test_org(self, org_name, mock_get):
        """
        Ensure GithubOrgClient.org returns whatever client.get_json returns,
        and that get_json was called exactly once with the expected URL.
        """
        expected_payload = {"login": org_name}
        mock_get.return_value = expected_payload

        client = GithubOrgClient(org_name)
        result = client.org

        mock_get.assert_called_once_with(
            f"https://api.github.com/orgs/{org_name}"
        )
        self.assertEqual(result, expected_payload)

    def test_public_repos_url(self):
        """Test that _public_repos_url returns repos_url from org payload."""
        test_payload = {"repos_url": "http://fakeurl.com/repos"}

        with patch(
            "client.GithubOrgClient.org",
            new_callable=PropertyMock
        ) as mock_org:
            mock_org.return_value = test_payload
            client = GithubOrgClient("test-org")

            result = client._public_repos_url

            self.assertEqual(result, "http://fakeurl.com/repos")
            mock_org.assert_called_once()

    @patch("client.get_json")
    def test_public_repos(self, mock_get_json):
        """Test that public_repos returns list of repo names."""
        test_payload = [
            {"name": "repo1"},
            {"name": "repo2"},
        ]
        mock_get_json.return_value = test_payload

        with patch(
            "client.GithubOrgClient._public_repos_url",
            new_callable=PropertyMock
        ) as mock_repos_url:
            mock_repos_url.return_value = "http://fakeurl.com/repos"

            client = GithubOrgClient("test-org")
            result = client.public_repos()

            self.assertEqual(result, ["repo1", "repo2"])
            mock_repos_url.assert_called_once()
            mock_get_json.assert_called_once_with("http://fakeurl.com/repos")
    
    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False),
    ])
    def test_has_license(self, repo, license_key, expected):
        """
        Test GithubOrgClient.has_license returns True if repo's license
        matches the license_key, otherwise False.
        """
        self.assertEqual(
            GithubOrgClient.has_license(repo, license_key),
            expected
        )



"""
Integration tests for GithubOrgClient.public_repos using fixtures.
"""
@parameterized_class(
    ("org_payload", "repos_payload", "expected_repos", "apache2_repos"),
    [(org_payload, repos_payload, expected_repos, apache2_repos)]
)
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """Integration tests for GithubOrgClient.public_repos."""

    @classmethod
    def setUpClass(cls):
        """
        Patch requests.get used inside the client (via get_json) so that
        HTTP calls return the example payloads from fixtures.py.

        We start a patcher once for the whole class to avoid patching in
        each test method (faster). The mock uses a side_effect to return
        different payloads depending on the requested URL.
        """
        # Patch the requests.get used in client module indirectly from utils
        cls.get_patcher = patch("utils.requests.get")
        cls.mocked_get = cls.get_patcher.start()

        def get_side_effect(url, *args, **kwargs):
            """Return a Mock whose .json() returns different fixtures."""
            mock_resp = Mock()
            # URL used to fetch org (client.org)
            org_url = f"https://api.github.com/orgs/{cls.org_payload['login']}"
            # URL used to fetch repos (org_payload['repos_url'])
            repos_url = cls.org_payload.get("repos_url")

            if url == org_url:
                mock_resp.json.return_value = cls.org_payload
                return mock_resp
            if repos_url and url == repos_url:
                mock_resp.json.return_value = cls.repos_payload
                return mock_resp

            # default safe fallback
            mock_resp.json.return_value = {}
            return mock_resp

        cls.mocked_get.side_effect = get_side_effect

    @classmethod
    def tearDownClass(cls):
        """Stop the requests.get patcher started in setUpClass."""
        cls.get_patcher.stop()

    def test_public_repos(self):
        """public_repos should return the expected repository names."""
        client = GithubOrgClient(self.org_payload["login"])
        self.assertEqual(client.public_repos(), self.expected_repos)

    def test_public_repos_with_license(self):
        """public_repos should filter repos by license_key properly."""
        client = GithubOrgClient(self.org_payload["login"])
        self.assertEqual(
            client.public_repos(license_key="apache-2.0"),
            self.apache2_repos
        )

