from util.create_map import create_map
import networkx as nx
import numpy as np


class Graph(nx.Graph):

    def __init__(self, graph):
        super(Graph, self).__init__(graph)
        self.graph = graph

    def display(self):

        color_dict = {"start": "green", "empty": "skyblue", "target": "red"}
        colors = [color_dict[node[1]["node_type"]] for node in self.graph.nodes(data=True)]
        
        pos = nx.spring_layout(self.graph, k=1.5)
        nx.draw(self.graph, pos, with_labels=True, node_color=colors)


class Map2Graph: 
    
    def __init__(self):
        self.last_mapp = None
        
    def to_graph(self, mapp):
        self.last_mapp = mapp
        return self.convert()

    def convert(self):
        
        map_arr = self.last_mapp.mapp
        start = self.last_mapp.start
        target = self.last_mapp.target

        graph = nx.Graph()

        # keep the indices of empty spaces, starting point and target (0,1,2)
        # -1 and -2 means wall and obstacle
        indices = np.argwhere((map_arr == 0) | (map_arr == 1) | (map_arr == 2))
        indices = [tuple(ind) for ind in indices]

        # add nodes to graph after determining type (start, target and empty)
        for node in indices:
            if tuple(node) == start:
                graph.add_node(tuple(node), node_type="start")
            elif tuple(node) == target:
                graph.add_node(tuple(node), node_type="target")
            else:        
                graph.add_node(tuple(node), node_type="empty")


        for node in indices:
            possible_neighbors = [
                (node[0]-1, node[1]),
                (node[0]+1, node[1]),
                (node[0], node[1]-1),
                (node[0], node[1]+1)
            ]

            for neighbor in possible_neighbors:
                if neighbor in indices:
                    graph.add_edge(tuple(node), neighbor)

        self.graph = Graph(graph)
        return self.graph