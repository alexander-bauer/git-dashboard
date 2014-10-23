#!/usr/bin/python

import graph
import gitutils


br = gitutils.BrowsedRepo("../foodd-hophacks")

with open("test_graph_data.json", "w") as f:
    br.build_tree().to_graph().to_sigma_json(f)
