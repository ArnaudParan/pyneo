#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    GraphHandler
    ============

    Submodule containing the class which sends the cypher requests to the
    server.
"""

import urllib2
import json
import base64


class GraphHandler(object):
    """
        GraphHandler
        ============

        This class stores what is necessary for authentication with the
        neo4j server, and sends requests to that server with the
        :func:`send_query` function. That class also allows you to get
        graphs for d3js displaying with the :func:`ask_graph` function.

        .. warnings:: don't use requests which return nodes, relationships or
        graphs with send_query. That functionnality is not implemented yet
    """

    def __init__(self, host_port, username, password):
        """initializes the authentification parameters

            - parameters using ``:param <name>: <description>``
            - type of the parameters ``:type <name>: <description>``
            - returns using ``:returns: <description>``
            - examples (doctest)
            - seealso using ``.. seealso:: text``
            - notes using ``.. note:: text``
            - warning using ``.. warning:: text``
            - todo ``.. todo:: text``

            :param host_port: the 'host:port' of the server
            :param username: the username you use to authenticate with neo4j
            :param password: the password you use to authenticate with neo4j
            :type host_port: string
            :type username: string
            :type password: string

            :Example:

                >>> graph_handler = GraphHandler(host_port='localhost:7474',
                >>>                              username='neo4j',
                >>>                              password='neo4j')
        """
        base64string = base64.encodestring('{}:{}'.format(username,
                                                          password))[:-1]
        self.authheader = 'Basic {}'.format(base64string)
        self.query_url = 'http://{0}/db/data/cypher'.format(host_port)
        self.graph_query_url = 'http://{0}/db/data/transaction/commit'\
            .format(host_port)

    def send_query(self, query, **params):
        """the function that sends normal cypher queries to the server

            - parameters using ``:param <name>: <description>``
            - type of the parameters ``:type <name>: <description>``
            - returns using ``:returns: <description>``
            - examples (doctest)
            - seealso using ``.. seealso:: text``
            - notes using ``.. note:: text``
            - warning using ``.. warning:: text``
            - todo ``.. todo:: text``

            :param query: a cyhper query to execute on the server
            :param params: the parameters passed to the cypher request
            :type query: string
            :type params: dict

            .. warning:: we would strongly advise you to use parameters
            if you want to avoid having to face cypher injection security
            issues

            :Example:

                >>> graph_handler.\
                >>>     send_query('MATCH (n) RETURN ID(n) AS id LIMIT 25')
                [{'id': 0}, {'id': 1}, ..., {'id': 23}, {'id': 24}]

                And with parameters

                >>> graph_handler.\
                >>>     send_query('MATCH (n {name: {p}}) RETURN ID(n)',
                >>>                p="test")
                [{'id': 20}]
        """
        query_params = {}
        query_params['query'] = query
        query_params['params'] = params

        req = urllib2.Request(self.query_url,
                              data=json.dumps(query_params))
        req.add_header('Content-Type', 'application/json')
        req.add_header('Accept', 'application/json')
        req.add_header('Authorization', self.authheader)

        handle = urllib2.urlopen(req)

        response_dict = json.loads(handle.read())
        formatted_response = GraphHandler.format_query_response(response_dict)

        return formatted_response

    def ask_graph(self, query, **params):
        """the function that sends cypher queries that should retrive neo4j graphs
        in order to display it in a d3js force element

            - parameters using ``:param <name>: <description>``
            - type of the parameters ``:type <name>: <description>``
            - returns using ``:returns: <description>``
            - examples (doctest)
            - seealso using ``.. seealso:: text``
            - notes using ``.. note:: text``
            - warning using ``.. warning:: text``
            - todo ``.. todo:: text``

            :param query: a cyhper query to execute on the server to
            select the graph to retrive
            :param params: a dict of parameters to pass with the request
            :type query: string
            :type params: dict

            :Example:

                >>> graph_handler.\
                >>>     ask_graph('MATCH path = (n)-[r]->(m) RETURN path')
                {
                'results': [
                    {
                        'columns': ['path'],
                        'data': [
                            {
                                'graph': {
                                    'nodes': [{...}, {...}],
                                    'relationships': [{...}]
                            },
                            {
                                'graph': ...
                            },
                            ...
                        ]
                    }
                ],
                'errors': []
                }
        """
        query_params = {}
        query_params['statement'] = query
        query_params['resultDataContents'] = ['graph']
        query_params['parameters'] = params
        query_params = {'statements': [query_params]}

        req = urllib2.Request(self.graph_query_url,
                              data=json.dumps(query_params))
        req.add_header('Content-Type', 'application/json')
        req.add_header('Accept', 'application/json')
        req.add_header('Authorization', self.authheader)

        handle = urllib2.urlopen(req)

        response_dict = json.loads(handle.read())

        return response_dict

    @staticmethod
    def format_query_response(response_dict):
        """Formats the response recieved by the server
        it essentially seperates the data in order to return
        a single array of dicts, each dict representing one row
        of the data

            - parameters using ``:param <name>: <description>``
            - type of the parameters ``:type <name>: <description>``
            - returns using ``:returns: <description>``
            - examples (doctest)
            - seealso using ``.. seealso:: text``
            - notes using ``.. note:: text``
            - warning using ``.. warning:: text``
            - todo ``.. todo:: text``

            :param response_dict: the dict returned by the server
            :type response_dict: dict
        """
        col_names = response_dict['columns']
        formatted_response = []
        for line in response_dict['data']:
            formatted_line = {}
            for col_name, cell in zip(col_names, line):
                formatted_line[col_name] = cell
            formatted_response.append(formatted_line)
        return formatted_response
