import numpy as np
import matplotlib.pyplot as plt
import networkx as nx

class Map:
    def __init__(self, mapp, target, start=(0,0)):
        self.mapp = mapp # 2d map in np array format
        self.start = start[0]+1, start[1]+1 # coordinates of starting point
        self.target = target # coordinates of target point

        self.graph = None
        
    def __copy__(self):
        return Map(self.mapp, self.target, self.start)
    
    def add_graph(self, graph):
        self.graph = graph

    def plot_map(self):
        h,w = self.mapp.shape
        # method to plot 2d map
        fig = plt.figure(figsize=(8*(w//10),6*(h//10)))
        plt.imshow(self.mapp, cmap="inferno")
        plt.show()
    
    def plot_graph(self):
        self.graph.display()


class Graph(nx.Graph):

    def __init__(self, graph, start, target):
        super(Graph, self).__init__(graph)
        self.graph = graph
        self.start = start
        self.target = target

    def display(self):

        color_dict = {"start": "green", "empty": "skyblue", "target": "red"}
        colors = [color_dict[node[1]["node_type"]] for node in self.graph.nodes(data=True)]
        
        pos = nx.spring_layout(self.graph, k=1.5)
        nx.draw(self.graph, pos, with_labels=True, node_color=colors)


class Map2Graph: 
            
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

        return Graph(graph, start, target)
def create_map(w, h=None, start=(0,0), d=0.1):
    """
    n: height of map
    m: width of map
    d: obstacle density
    close: if True, target point won't be too far away from start
    """
    
    if not h:
        h=w

    target = np.random.randint(1,w+1), np.random.randint(1,h+1)

    """
    wall: -2
    start: 1
    target: 2
    obstacle: -1
    """
    mapp = np.zeros((w+2, h+2))
    mapp[:,0] = -2
    mapp[:,-1] = -2
    mapp[0,:] = -2
    mapp[-1,:] = -2
    mapp[start[0]+1, start[1]+1] = 1
    mapp[target[0], target[1]] = 2
    
    # according to d (obstacle density), create random obstacles
    rand_obstacles = np.random.randint(1, h*w+1, int(h*w*d))
    rows, cols = (rand_obstacles // h)+1, (rand_obstacles % h)
    obstacles = list(zip(rows, cols))
    for obs in obstacles:
        if mapp[obs] == 0:
            mapp[obs] = -1

    # create Map object
    mapp = Map(mapp, start=start,target=(target[0], target[1]), )

    m2g = Map2Graph()
    graph = m2g.to_graph(mapp)
    mapp.add_graph(graph)

    return mapp