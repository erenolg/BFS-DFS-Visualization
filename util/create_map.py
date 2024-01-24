import numpy as np
import matplotlib.pyplot as plt

class Map:
    def __init__(self, mapp, target, start=(0,0)):
        self.mapp = mapp # 2d map in np array format
        self.start = start[0]+1, start[1]+1 # coordinates of starting point
        self.target = target # coordinates of target point
        
    def __copy__(self):
        return Map(self.mapp, self.target, self.start)

    def plot(self):
        # method to plot 2d map
        plt.imshow(self.mapp, cmap="inferno")
        plt.show()


def create_map(h, w=None, start=(0,0), d=0.1, close=False):
    """
    n: height of map
    m: width of map
    d: obstacle density
    close: if True, target point won't be too far away from start
    """
    
    if not w:
        w=h
    if not close:
        target = np.random.randint(h)+1, np.random.randint(w)+1
    else:
        # choose 3 random target points and use the closest one to starting point
        best_dist, target = float("inf"), None
        for i in range(3):
            target_candidate = np.random.randint(h)+1, np.random.randint(w)+1
            dist = (start[0]-target_candidate[0])**2 + (start[1]-target_candidate[1])**2
            if dist < best_dist:
                best_dist, target = dist, target_candidate
    """
    wall: -2
    start: 1
    target: 2
    obstacle: -1
    """
    mapp = np.zeros((h+2, w+2))
    mapp[:,0] = -2
    mapp[:,-1] = -2
    mapp[0,:] = -2
    mapp[-1,:] = -2
    mapp[start[0]+1, start[1]+1] = 1
    mapp[target[0], target[1]] = 2
    
    # according to d (obstacle density), create random obstacles
    rand_obstacles = np.random.randint(0, h*w, int(h*w*d))
    rows, cols = (rand_obstacles // h)+1, (rand_obstacles % w)+1
    obstacles = list(zip(rows, cols))
    for obs in obstacles:
        if mapp[obs] == 0:
            mapp[obs] = -1

    # create Map object
    mapp = Map(mapp, start=start,target=(target[0], target[1]), )
    return mapp