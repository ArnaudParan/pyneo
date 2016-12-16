#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    Pyneo
    =====

    This module lets one make cypher requests to a neo4j server on a google app
    engine application. In order to be appengine compatible, the code uses only
    urllib for the requests

    :Example:
    If you want to send cypher requests to a remote server, you need to tell
    pyneo your username and password first for neo4j authentication.

    >>> from pyneo import GraphHandler
    >>> graph_handler = GraphHandler(host_port='localhost:7474',
    >>>                              username='neo4j',
    >>>                              password='neo4j')

    Then, you can send cypher requests to your neo4j server

    >>> graph_handler.send_query('MATCH (n) RETURN ID(n) AS id LIMIT 25')
    [{'id': 0}, {'id': 1}, {'id': 2}, {'id': 3}, ..., {'id': 23}, {'id': 24}]

    And with parameters

    >>> graph_handler.\
    >>>     send_query('MATCH (n {name: {p}}) RETURN ID(n)', p="test")
    [{'id': 20}]

    Be careful with your requests because we don't handle returning nodes,
    relations or paths yet. However, you can return ID(n), LABELS(n) or
    n.name or other parameters.

    One day, you might want to get a full graph to display it in d3js as
    explained at:
    https://neo4j.com/developer/guide-data-visualization/#_neo4j_query_result_format

    If you want to do so, from now on you need to send a graph query

    >>> graph_handler.ask_graph('MATCH path = (n)-[r]->(m) RETURN path')
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

    If you want to perform your request over https, when initiating the
    graph, you can provide the parameter secure=True

    and hopefully, soon you will be able to download our graph polymer
    component which directly displays that data

    .. warnings:: don't use requests which return nodes, relationships or
    graphs with send_query. That functionnality is not implemented yet

    .. todo:: handle returning nodes, relations and paths
              unify graphs with normal queries
"""

from pyneo.graph_handler import GraphHandler  # noqa # pylint: disable=unused-import

__all__ = ['graph_handler']
