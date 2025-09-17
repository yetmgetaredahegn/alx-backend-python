#!/usr/bin/env python3
import unittest
from parameterized import parameterized

from utils import access_nested_map


class TestAccessNestedMap(unittest.TestCase):
    @parameterized.expand([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a",), {"b": 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2),
    ])
    def test_access_nested_map(self,nested_map,path,expected):
        self.assertEqual(access_nested_map(nested_map, path),expected)

    # @parameterized.expand([
    #     ({}, ("a",), "'a'"),
    #     ({"a": 1}, ("a", "b"), "'b'"),
    # ])
    # def test_access_nested_map_exception(self,nested_map,path,expected):
    #     with self.assertRaises(KeyError) as ex:
    #         access_nested_map(nested_map,path)
    #     self.assertEqual(str(ex.exception), expected)