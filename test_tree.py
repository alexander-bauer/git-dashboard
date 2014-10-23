#!/usr/bin/python
import gitutils

br = gitutils.BrowsedRepo("../foodd-hophacks")
print(br.build_tree().roots)
