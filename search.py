import numpy as np
import matplotlib.pyplot as plt
from collections import deque
from queue import PriorityQueue
import math


class Search:
    
    def __init__(self):
        self.last_map = None
        self.last_progress = None

    def bfs(self, map):
        self.last_map = map
        start, target = map.start, map.target
        graph = map.graph
        
        queue = deque([start])
        visited = list()
        
        while queue:
            current = queue.popleft()
            if current == target:
                visited.append(current)
                print(f"Found in {current} || {len(visited)} steps")
                self.last_progress = visited
                return
            elif current not in visited:
                visited.append(current)
                childs = graph.neighbors(current)
                for child in childs:
                    queue.append(child)
        print(f"Not found in {len(visited)} steps")
        self.last_progress = visited
        return
    
    def dfs(self, map):
        self.last_map = map
        start, target = map.start, map.target
        graph = map.graph
        
        stack = deque([start])
        visited = list()
        
        while stack:
            current = stack.pop()
            if current == target:
                visited.append(current)
                print(f"Found in {current} || {len(visited)} steps")
                self.last_progress = visited
                return
            if current not in visited:
                visited.append(current)
                childs = graph.neighbors(current)
                for child in childs:
                    stack.append(child)
        print(f"Not found in {len(visited)} steps")
        self.last_progress = visited
        return
    
    def astar(self, map, h="manhattan"):
        
        if h == "manhattan": h = manhattan
        elif h == "euclidian": h = euclidian
        else:
            print("Heuristic function not found, default will be used!")
            h = manhattan


        self.last_map = map
        start, target = map.start, map.target
        graph = map.graph

        queue = PriorityQueue()
        visited = []

        g_score = {cell: float('inf') if cell!=start else 0 for cell in graph.nodes}
        f_score = {cell: float('inf') if cell!=start else h(start,target) for cell in graph.nodes}

        queue.put((f_score[start], h(start, target), start))

        while queue:
            current = queue.get()[2]
            visited.append(current)
            if current == target:
                print(f"Found at {current} || {len(visited)} steps")
                self.last_progress = visited
                return
            neighbors = list(graph.neighbors(current))
            for neighbor in neighbors:
                temp_g = g_score[current]+1
                temp_f = temp_g + h(neighbor, target)
                
                if temp_f < f_score[neighbor]:
                    g_score[neighbor] = temp_g
                    f_score[neighbor] = temp_f
                    queue.put((f_score[neighbor], h(neighbor, target), neighbor))
        print(f"Not found in {len(visited)} steps")
        self.last_progress = visited
        return

    
    def plot_progress(self):
        if not self.last_progress:
            print("Progress not found!") 
            return
        path = self.last_progress
        temp_map = self.last_map.mapp.copy()
        progress = []    
        while path:
            curr = path.pop(0)
            temp_map[curr] = 1
            progress.append(temp_map.copy())

        n = len(progress)
        rows = int(np.ceil(n / 6))
        cols = min(n, 6)

        fig, axes = plt.subplots(rows, cols, figsize=(cols*6, rows*6))

        for i in range(rows):
            for j in range(cols):
                index = i * cols + j
                if index < n:
                    axes[i, j].imshow(progress[index], cmap='inferno')  # Assuming grayscale images
                    axes[i, j].axis('off')
                    axes[i, j].text(0.5, -0.1, str(index + 1), fontsize=15, color='black', ha='center', va='center', transform=axes[i, j].transAxes)
                else:
                    axes[i, j].axis('off')  # Turn off empty subplots if any

        plt.show()


def manhattan(current, target):
    currx, curry = current
    tarx, tary = target
    return abs(currx - tarx) + abs(curry - tary)

def euclidian(current, target):
    currx, curry = current
    tarx, tary = target
    return math.sqrt(abs(currx - tarx)**2 + abs(curry - tary)**2)