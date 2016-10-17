#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Tests the abstract_graph_handler module"""

import unittest
from pyneo import GraphHandler


class TestGraphHandler(unittest.TestCase):
    """tests the GraphHandler class"""

    def assert_eq(self, first, second, message=""):
        """Redefiniton of assertEqual with enchanced error message.
        in order to be more readable, it shows the two values"""
        self.assertEqual(
            first,
            second,
            "expects {} to be {}.\n".format(first, second) + message)

    def setUp(self):
        self.graph_handler = GraphHandler("localhost:7474", "neo4j", "neo4j")

    def test_format_query_response(self):
        """Tests that the responses are correctly formatted"""
        response = {
            "columns": ["a", "b"],
            "data": [
                [None, 1],
                [None, 2]
            ]
        }
        formatted_response =\
            self.graph_handler.format_query_response(response)
        self.assert_eq(
            formatted_response[0]["b"],
            1,
            "{0} equal to {1}".format(formatted_response[0]["b"], 1))
