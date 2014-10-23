import json

class Graph:
    def __init__(self):
        self.nodes = {} # id to node mapping

    def add(self, *nodes):
        for node in nodes:
            self.nodes[node.id] = node

    def points_to(self, node_from_id, node_to_id):
        self.nodes[node_to_id].add_from(node_from_id)

    def to_sigma_json(self, file):
        data = {"nodes": [], "edges": []}

        for index, node in enumerate(self.nodes):
            node_data = self.nodes[node].node_for_sigma()
            data["nodes"].append(node_data)

            for edge in self.nodes[node].edges_for_sigma():
                data["edges"].append(edge)

        json.dump(data, file)

class Node:
    def __init__(self, id, label, *from_ids, x=0, y=0, size=1):
        self.id = id
        self.label = label
        self.x = x
        self.y = y
        self.size = size
        self.edges_from = []

        for from_id in from_ids:
            self.add_from(from_id)

    def add_from(self, from_id):
        if type(from_id) == Node:
            from_id = from_id.id

        if from_id not in self.edges_from:
            self.edges_from.append(from_id)

    def node_for_sigma(self):
        return {"id": self.id, "label": self.label,
                "x": self.x, "y": self.y, "size": self.size}

    def edges_for_sigma(self):
        for edge_from in self.edges_from:
            yield { "id": "%s..%s" % (edge_from, self.id),
                    "source": edge_from,
                    "target": self.id,
                    "size": 8,
                    "type": "arrow"}
