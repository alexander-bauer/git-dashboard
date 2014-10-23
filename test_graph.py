#!/usr/bin/python

import graph

g = graph.Graph()
c_root = graph.Node("c0", "root node", "c1", y=1)
c1 = graph.Node("c1", "child", y=0)
g.add(c_root, c1)

with open("test_graph_data.json", "w") as f:
    g.to_sigma_json(f)
