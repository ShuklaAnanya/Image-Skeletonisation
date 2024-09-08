'''
Image Skeletonization using Breadth First Search Traversal Algorithm

Logic Flow:
Initialize the Image into a Graph Representation (in form of an Adjacency List) and Enqueue the Initial Boundary Pixels of the Object in the Image (White Pixels with Black Neighbors)

While there are Boundary Pixels to Process, Keep Traversing the Pixels using BFS and Apply Zhang-Suen Conditions to Check if the Pixel can be Removed or Not
If the Conditions are Satisfied, Mark the Pixel for Removal (1 -> 0 or White -> Black Pixel)
Enqueue the Neighbors of the Pixel as Potential New Boundary Pixels and Repeat until there are no Boundary Pixels to Process, i.e., Goal State is Reached

Zhang-Suen Conditions:
1. 2 <= N(P1) <= 6 (Number of Foreground Pixels in the 8-Neighbors is between 2 and 6)
2. S(P1) == 1 (Number of 0 -> 1 Transitions in the 8-Neighbors is 1)
3. P2 * P4 * P6 == 0 (P2, P4, P6 are Foreground Pixels)
4. P4 * P6 * P8 == 0 (P4, P6, P8 are Foreground Pixels)

Input:
- Image (2D Matrix) with Foreground (White) and Background (Black) Pixels

Output:
- Image Skeletonized (Thin Image) with Foreground (White) and Background (Black) Pixels

Space and Time Complexity:
- O(N * M) where N is the Number of Rows and M is the Number of Columns in the Image
'''

# Importing Libraries
import time
import numpy as np
from queue import Queue
import numpy as np
import cv2
import matplotlib.pyplot as plt

# Image to Graph Representation 
# Converts the image into a graph structure where each pixel is a node
def initialize_graph(image):
    graph = {}
    rows, cols = image.shape
    
    for x in range(rows):
        for y in range(cols):
            if image[x][y] == 1:  # Only process foreground (white) pixels
                pixel = (x, y)
                graph[pixel] = get_8_neighbors(image, x, y)  # Store its 8-neighbors
    return graph