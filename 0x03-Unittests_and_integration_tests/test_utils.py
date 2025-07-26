#!/usr/bin/env python3
"""Unit test for memoization"""

import unittest
from unittest.mock import patch
from utils import memoize


class TestMemoize(unittest.TestCase):
    def test_memoize(self):
        """Test that memoize caches the result after first call"""

        class TestClass:
            def a_method(self):
                return 42

            @memoize
            def a_property(self):
                return self.a_method()

        with patch.object(TestClass, 'a_method', return_value=42) as mock_method:
            obj = TestClass()

            # First call (calls a_method)
            result1 = obj.a_property()
            # Second call (uses cached result)
            result2 = obj.a_property()

            # Both should return 42
            self.assertEqual(result1, 42)
            self.assertEqual(result2, 42)

            # a_method should be called only once
            mock_method.assert_called_once()
