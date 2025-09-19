#!/usr/bin/env python3
import unittest
from parameterized import parameterized
from unittest.mock import patch
from client import GithubOrgClient


class TestGithubOrgClient(unittest.TestCase):
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
        # Arrange: tell the mock what to return
        expected_payload = {"login": org_name}
        mock_get.return_value = expected_payload

        # Act: create client and call org()
        client = GithubOrgClient(org_name)
        result = client.org

        # Assert: get_json was called correctly and result is the mocked payload
        mock_get.assert_called_once_with(f"https://api.github.com/orgs/{org_name}")
        self.assertEqual(result, expected_payload)


    def test_public_repos_url(self):
        # payload we want .org to return
        test_payload = {"repos_url": "http://fakeurl.com/repos"}

        with patch("client.GithubOrgClient.org", new_callable=PropertyMock) as mock_org:
            # make .org return our fake payload
            mock_org.return_value = test_payload

            client = GithubOrgClient("test-org")

            result = client._public_repos_url

            # check if the result is taken from repos_url of the fake payload
            self.assertEqual(result, "http://fakeurl.com/repos")
            mock_org.assert_called_once()

