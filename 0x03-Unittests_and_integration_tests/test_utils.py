#!/usr/bin/env python3
"""
Unit tests for utils module functions:
- access_nested_map
- get_json
- memoize
"""

import unittest
from unittest.mock import patch, Mock
from parameterized import parameterized
from utils import access_nested_map, get_json, memoize


class TestAccessNestedMap(unittest.TestCase):
    """Test access_nested_map function with various nested paths"""

    @parameterized.expand([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a",), {"b": 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2),
    ])
    def test_access_nested_map(self, nested_map, path, expected):
        """Test that access_nested_map returns expected results"""
        self.assertEqual(access_nested_map(nested_map, path), expected)


class TestGetJson(unittest.TestCase):
    """Test get_json function with mocked HTTP requests"""

    @parameterized.expand([
        ("http://example.com", {"payload": True}),
        ("http://holberton.io", {"payload": False}),
    ])
    def test_get_json(self, test_url, test_payload):
        """
        Test that get_json returns expected payload
        and requests.get is called once with the URL
        """
        with patch('utils.requests.get') as mock_get:
            mock_response = Mock()
            mock_response.json.return_value = test_payload
            mock_get.return_value = mock_response

            result = get_json(test_url)

            mock_get.assert_called_once_with(test_url)
            self.assertEqual(result, test_payload)


class TestMemoize(unittest.TestCase):
    """Test memoize decorator functionality"""

    def test_memoize(self):
        """
        Test that memoize caches the result after the first method call.
        a_method should only be called once even if a_property is accessed twice.
        """
        class TestClass:
            """Sample class with memoized method"""

            def a_method(self):
                """Simulate an expensive operation"""
                return 42

            @memoize
            def a_property(self):
                """Memoized property method"""
                return self.a_method()

        with patch.object(TestClass, 'a_method', return_value=42) as mock_method:
            obj = TestClass()
            self.assertEqual(obj.a_property(), 42)
            self.assertEqual(obj.a_property(), 42)
            mock_method.assert_called_once()
