import numpy as np
import matplotlib.pyplot as plt
from collections import deque

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