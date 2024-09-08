'''
Image Skeletonization using Depth First Search Traversal Algorithm

Logic Flow:
Initialize the image into a graph representation (in the form of an adjacency list) and push the initial boundary pixels of the object in the image (white pixels with black neighbors) onto a stack.
While there are boundary pixels to process, keep traversing the pixels using DFS (depth-first search) by popping the pixels from the stack and processing them. Apply the Zhang-Suen conditions to check if the pixel can be removed or not
If the conditions are satisfied, mark the pixel for removal (1 -> 0 or white -> black pixel). Push the neighbors of the pixel onto the stack as potential new boundary pixels and repeat the process until there are no boundary pixels left to process, i.e., the goal state is reached

Zhang-Suen Conditions:
1. 2 <= N(P1) <= 6 (Number of foreground pixels in the 8-neighbors is between 2 and 6)
2. S(P1) == 1 (Number of 0 -> 1 transitions in the 8-neighbors is 1)
3. P2 * P4 * P6 == 0 (P2, P4, P6 are foreground pixels)
4. P4 * P6 * P8 == 0 (P4, P6, P8 are foreground pixels)

Input:
- Image (2D matrix) with foreground (white) and background (black) pixels

Output:
- Image skeletonized (thinned image) with foreground (white) and background (black) pixels

Space and Time Complexity:
- O(N * M) where N is the number of rows and M is the number of columns in the image
'''

# Importing Libraries
import time
import numpy as np
import cv2
import matplotlib.pyplot as plt

# Image to Graph Representation (Adjacency List) : Each Pixel is a Node and its 8-Neighbors are its Adjacent Nodes
def initialize_graph(image):
    graph = {}
    rows, cols = image.shape
    
    for x in range(rows):
        for y in range(cols):
            if image[x][y] == 1:  # Only process foreground (white) pixels
                pixel = (x, y)
                graph[pixel] = get_8_neighbors(image, x, y)  # Store its 8-neighbors
    return graph

# Enqueuing the Initial Boundary Pixels of the Object in the Image
def initialize_boundary_stack(image):
    boundary_stack = []
    rows, cols = image.shape
    
    for x in range(1, rows - 1):  # Ignore Boundary Pixels
        for y in range(1, cols - 1):
            if image[x][y] == 1 and has_background_neighbor(image, x, y):
                boundary_stack.append((x, y))
    return boundary_stack

# Check if the Pixel has any Background Neighbor (Black Pixel)
def has_background_neighbor(image, x, y):
    neighbors = get_8_neighbors(image, x, y)
    return any(image[nx][ny] == 0 for nx, ny in neighbors)

# Get the 8-Neighbors of a Pixel while Ensuring they are within the Image Bounds
def get_8_neighbors(image, x, y):
    rows, cols = image.shape
    neighbors = []
    
    neighbor_positions = [(-1,  0), (-1,  1), ( 0,  1), ( 1,  1),( 1,  0), ( 1, -1), ( 0, -1), (-1, -1)]
    
    for dx, dy in neighbor_positions:
        nx, ny = x + dx, y + dy
        if 0 <= nx < rows and 0 <= ny < cols:
            neighbors.append((nx, ny))
    
    return neighbors

# Count the Number of 0 -> 1 Transitions in the 8-Neighbors of a Pixel
def transitions(neighbors):
    n = neighbors + neighbors[0:1]
    return sum((n1, n2) == (0, 1) for n1, n2 in zip(n, n[1:]))

# Zhang-Suen Logic for DFS-based Skeletonization
def moveGen_dfs(image, stack):
    next_boundary_stack = []
    pixel_updates = 0
    condition_checks = 0

    while stack:
        x, y = stack.pop()

        neighbors_coords = get_8_neighbors(image, x, y)
        if len(neighbors_coords) < 8:
            continue

        P2, P3, P4, P5, P6, P7, P8, P9 = [image[nx][ny] for nx, ny in neighbors_coords]
        n = [P2, P3, P4, P5, P6, P7, P8, P9]
        
        # Apply Zhang-Suen Conditions
        condition_checks += 1
        if (image[x][y] == 1 and
            2 <= sum(n) <= 6 and
            transitions(n) == 1 and
            P2 * P4 * P6 == 0 and
            P4 * P6 * P8 == 0):

            image[x][y] = 0
            pixel_updates += 1

            for nx, ny in neighbors_coords:
                if image[nx][ny] == 1:
                    next_boundary_stack.append((nx, ny))
                    
    return image, next_boundary_stack, pixel_updates, condition_checks, len(next_boundary_stack)

# Goal Test: If the Stack is Empty
def goalTest(stack):
    return len(stack) == 0

# Depth First Search Traversal
def dfs_traversal(image):
    num_iterations = 0
    total_pixel_updates = 0
    total_condition_checks = 0
    start_time = time.time()

    graph = initialize_graph(image)
    boundary_stack = initialize_boundary_stack(image)
    max_stack_size = len(boundary_stack)

    while not goalTest(boundary_stack):
        num_iterations += 1
        image, boundary_stack, pixel_updates, condition_checks, stack_size = moveGen_dfs(image, boundary_stack)

        total_pixel_updates += pixel_updates
        total_condition_checks += condition_checks
        max_stack_size = max(max_stack_size, stack_size)

    end_time = time.time()
    time_taken = end_time - start_time

    print("Number of iterations:", num_iterations)
    print("Total pixel updates:", total_pixel_updates)
    print("Total Zhang-Suen condition checks:", total_condition_checks)
    print("Maximum boundary stack size:", max_stack_size)
    print("Total time taken (seconds):", time_taken)
    
    return image

##__main__##

# Reading the Image
image = cv2.imread('./image.png', cv2.IMREAD_GRAYSCALE)
image = cv2.resize(image, (100, 100))
image = np.where(image > 128, 1, 0)

# Displaying the Original Image
plt.imshow(image, cmap='gray')
plt.title("Original Image")
plt.show()

# Applying DFS Traversal for Image Skeletonization
skeletonized_image = dfs_traversal(image)

# Displaying the Skeletonized Image
plt.imshow(skeletonized_image, cmap='gray')
plt.title("Skeletonized Image")
plt.show()

# Saving the Skeletonized Image
cv2.imwrite('./skeletonized_image.png', skeletonized_image * 255)
