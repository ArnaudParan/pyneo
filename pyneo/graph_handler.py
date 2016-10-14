#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""The module which sends cypher queries to the neo4j database and formats the results
It's a kind of replacement of py2neo while it does not work with gae, but it is compatible
with py2neo for replacement when the library will be compatible"""

import urllib
import urllib2
import json
import base64

class GraphHandler(object):
    """Handles sending cypher requests to a remote neo4j server with the rest api"""
    def __init__(self, host_port, username, password):
        """creates the variables necessary for the future requests"""
        self.username = username
        self.password = password
        self.query_url = "http://{0}/db/data/cypher".format(host_port)
        self.graph_query_url = "http://{0}/db/data/transaction/commit".format(host_port)
        password_mgr = urllib2.HTTPPasswordMgrWithDefaultRealm()
        password_mgr.add_password(None, self.query_url, username, password)
        handler = urllib2.HTTPBasicAuthHandler(password_mgr)
        self.opener = urllib2.build_opener(handler)

    def send_query(self, query, **kwargs):
        """The important function, it sends a cypher query to the neo4j database and returns the
        formatted result"""
        query_params = kwargs
        query_params["query"] = query
        response_dict =\
                json.load(self.opener.open(self.query_url, urllib.urlencode(query_params)))
        formatted_response = GraphHandler.format_query_response(response_dict)
        return formatted_response

    def ask_graph(self, query, **kwargs):
        """The important function, it sends a graph cypher query to the neo4j database and returns the
        formatted result"""
        query_params = kwargs
        query_params["statement"] = query
        query_params["resultDataContents"] = ["graph"]
        req = urllib2.Request(self.graph_query_url, data=json.dumps({"statements": [query_params]}))
        req.add_header('Content-Type', 'application/json')
        base64string = base64.encodestring('%s:%s' % (self.username, self.password))[:-1]
        authheader =  "Basic %s" % base64string
        req.add_header("Authorization", authheader)
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
