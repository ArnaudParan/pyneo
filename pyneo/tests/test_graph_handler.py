#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Tests the abstract_graph_handler module"""

import urllib2
import unittest
import StringIO
import json
import base64
import mock

from pyneo import GraphHandler


class TestGraphHandler(unittest.TestCase):
    """tests the GraphHandler class"""

    def assert_eq(self, first, second, message=''):
        """Redefiniton of assertEqual with enchanced error message.
        in order to be more readable, it shows the two values"""
        self.assertEqual(
            first,
            second,
            'expects {} to be {}.\n'.format(first, second) + message)

    def setUp(self):
        self.graph_handler = GraphHandler('localhost:7474', 'neo4j', 'neo4j')
        self.default_response = {
            'columns': ['a', 'b'],
            'data': [
                [None, 1],
                [None, 2]
            ]
        }

    def test_send_query(self):
        """tests the fact that queries are correctly sent, with the
        correct headers"""
        response_stream = StringIO.StringIO(json.dumps(self.default_response))
        urllib2.urlopen = mock.Mock(return_value=response_stream)
        query = 'MATCH (n) RETURN n LIMIT 25'
        self.graph_handler.send_query(query, test='test')

        args, _ = urllib2.urlopen.call_args
        request = args[0]

        expected_url = 'http://localhost:7474/db/data/cypher'
        actual_url = request.get_full_url()
        self.assert_eq(expected_url, actual_url)

        encoded_auth = 'Basic {}'.\
            format(base64.encodestring('neo4j:neo4j')[:-1])
        self.assertIn('Accept', request.headers)
        self.assert_eq(request.headers['Accept'], 'application/json')
        self.assertIn('Content-type', request.headers)
        self.assert_eq(request.headers['Content-type'], 'application/json')
        self.assertIn('Authorization', request.headers)
        self.assert_eq(request.headers['Authorization'], encoded_auth)

        query_dict = {
            'query': query,
            'params': {'test': 'test'}
            }
        self.assert_eq(json.dumps(query_dict), request.data)

    def test_ask_graph(self):
        """tests the fact that queries are correctly sent, with the
        correct headers"""
        response_stream = StringIO.StringIO(json.dumps(self.default_response))
        urllib2.urlopen = mock.Mock(return_value=response_stream)
        query = 'MATCH (n) RETURN n LIMIT 25'
        self.graph_handler.ask_graph(query, test='test')

        args, _ = urllib2.urlopen.call_args
        request = args[0]

        expected_url = 'http://localhost:7474/db/data/transaction/commit'
        actual_url = request.get_full_url()
        self.assert_eq(expected_url, actual_url)

        encoded_auth = 'Basic {}'.\
            format(base64.encodestring('neo4j:neo4j')[:-1])
        self.assertIn('Accept', request.headers)
        self.assert_eq(request.headers['Accept'], 'application/json')
        self.assertIn('Content-type', request.headers)
        self.assert_eq(request.headers['Content-type'], 'application/json')
        self.assertIn('Authorization', request.headers)
        self.assert_eq(request.headers['Authorization'], encoded_auth)

        query_dict = {
            'statements': [{
                'statement': query,
                'parameters': {'test': 'test'},
                'resultDataContents': ['graph']
                }]
            }
        self.assert_eq(json.dumps(query_dict), request.data)

    def test_format_query_response(self):
        """Tests that the responses are correctly formatted"""
        formatted_response =\
            self.graph_handler.format_query_response(self.default_response)
        self.assert_eq(formatted_response[0]['b'], 1)
