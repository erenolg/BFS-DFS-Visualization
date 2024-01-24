import numpy as np
import matplotlib.pyplot as plt


class Search:
    
    def __init__(self):
        self.last_mapp = None # keep the map to plot search progress
        self.found = False
    
    def bfs(self, mapp):
        self.last_mapp = mapp
        start, target = mapp.start, mapp.target
        queue = [start]
        visited = [start]

        while queue:
            current = queue.pop(0)
            childs = self.extend(mapp, current)
            for child in childs:
                if child not in visited:
                    if child == mapp.target:
                        print(f"Found at {child} || {len(visited)} steps")
                        self.found = True
                        return visited
                    visited.append(child)  
                    queue.append(child)
        print("Not found!")
        self.found = False
        return visited
    
    def dfs(self, mapp):
        self.last_mapp = mapp
        start, target = mapp.start, mapp.target
        stack = [start]
        visited = [start]
        
        while stack:
            current = stack.pop(-1)
            childs = self.extend(mapp, current)
            for child in childs:
                if child not in visited:
                    if child == mapp.target:
                        print(f"Found at {child} || {len(visited)} steps")
                        self.found = True
                        return visited
                    visited.append(child)
                    stack.append(child)
        print("Not found!")
        self.found = False
        return visited
    
    def extend(self, mapp, current):
        possible = [(current[0]+1, current[1]),
                    (current[0]-1, current[1]),
                    (current[0], current[1]+1),
                    (current[0], current[1]-1)]
        answer = []
        for pnt in possible:
            if mapp.mapp[pnt] == 2 or mapp.mapp[pnt] == 0:
                answer.append(pnt)
        return answer
    
    def plot_progress(self, path):
        temp_map = self.last_mapp.mapp.copy()
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