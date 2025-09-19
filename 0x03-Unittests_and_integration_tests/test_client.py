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
