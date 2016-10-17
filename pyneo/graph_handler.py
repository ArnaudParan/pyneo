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
        self.authheader = "Basic {}".format(base64string)
        self.query_url = "http://{0}/db/data/cypher".format(host_port)
        self.graph_query_url = "http://{0}/db/data/transaction/commit"\
            .format(host_port)

    def send_query(self, query):
        """
        The important function, it sends a cypher query to the neo4j database
        and returns the formatted result
        """
        query_params = {}
        query_params["query"] = query
        req = urllib2.Request(self.query_url,
                              data=json.dumps(query_params))
        req.add_header('Content-Type', 'application/json')
        req.add_header("Authorization", self.authheader)
        handle = urllib2.urlopen(req)
        response_dict = json.loads(handle.read())
        formatted_response = GraphHandler.format_query_response(response_dict)
        return formatted_response

    def ask_graph(self, query):
        """
        The important function, it sends a graph cypher query to the neo4j
        database and returns the formatted result
        """
        query_params = {}
        query_params["statement"] = query
        query_params["resultDataContents"] = ["graph"]
        query_params = {"statements": [query_params]}
        req = urllib2.Request(self.graph_query_url,
                              data=json.dumps(query_params))
        req.add_header('Content-Type', 'application/json')
        req.add_header("Authorization", self.authheader)
        handle = urllib2.urlopen(req)
        response_dict = json.loads(handle.read())
        return response_dict

    @staticmethod
    def format_query_response(response_dict):
        """Formats the response recieved by the server"""
        col_names = response_dict["columns"]
        formatted_response = []
        for line in response_dict["data"]:
            formatted_line = {}
            for col_name, cell in zip(col_names, line):
                formatted_line[col_name] = cell
            formatted_response.append(formatted_line)
        return formatted_response

    @staticmethod
    def protect(string):
        """replaces the \' in strings by \\\', one kind of security"""
        return string.replace("'", "\\\'")
