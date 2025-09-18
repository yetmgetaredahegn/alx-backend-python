#!/usr/bin/env python3
import unittest
from unittest import result
from unittest.mock import Mock, patch
from parameterized import parameterized

from utils import access_nested_map, get_json, memoize


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


#!/usr/bin/env python3
import unittest
from unittest.mock import patch
from utils import memoize


class TestMemoize(unittest.TestCase):
    def test_memoize(self):
        class TestClass:
            def a_method(self):
                return 42

            @memoize
            def a_property(self):
                return self.a_method()

        # Patch a_method so we can count calls
        with patch.object(TestClass, "a_method", return_value=42) as mock_method:
            obj = TestClass()

            # First access calls a_method
            self.assertEqual(obj.a_property, 42)
            mock_method.assert_called_once()

            # Second access should not call a_method again (cached)
            self.assertEqual(obj.a_property, 42)
            mock_method.assert_called_once()  # still only one call
