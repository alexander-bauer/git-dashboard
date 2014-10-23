#!/usr/bin/python

import graph
import gitutils


br = gitutils.BrowsedRepo("../foodd-hophacks")
br.build_tree()
br.balance_tree_on(None)

with open("test_graph_data.json", "w") as f:
    br.tree.to_graph().to_sigma_json(f)
