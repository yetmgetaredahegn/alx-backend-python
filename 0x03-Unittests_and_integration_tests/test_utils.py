#!/usr/bin/env python3
import unittest
from unittest import result
from unittest.mock import Mock, patch
from parameterized import parameterized

from utils import access_nested_map, get_json


class TestAccessNestedMap(unittest.TestCase):
    @parameterized.expand([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a",), {"b": 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2),
    ])
    def test_access_nested_map(self,nested_map,path,expected):
        self.assertEqual(access_nested_map(nested_map, path),expected)

    @parameterized.expand([
        ({}, ("a",), "'a'"),
        ({"a": 1}, ("a", "b"), "'b'"),
    ])
    def test_access_nested_map_exception(self,nested_map,path,expected):
        with self.assertRaises(KeyError) as ex:
            access_nested_map(nested_map,path)
        self.assertEqual(str(ex.exception), expected)

class TestGetJson(unittest.TestCase):
    @parameterized.expand([
        ("http://example.com", {"payload": True}),
        ("http://holberton.io", {"payload": False})
    ])
    @patch("utils.requests.get")
    def test_get_json(self, test_url, test_payload, mock_get):
        mock_response = Mock()
        mock_response.json.return_value = test_payload
        mock_get.return_value = mock_response

        result = get_json(test_url)

        self.assertEqual(result,test_payload)
        mock_get.assert_called_once_with(test_url)