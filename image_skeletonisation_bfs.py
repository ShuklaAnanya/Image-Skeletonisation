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


# Image to Graph Representation (Adjacency List) : Each Pixel is a Node and its 8-Neighbors are its Adjacent Nodes
def initialize_graph(image):
    graph = {}
    rows, cols = image.shape
    
    # Travering through the Foreground (White) Image Pixels
    for x in range(rows):
        for y in range(cols):
            if image[x][y] == 1:  # Only process foreground (white) pixels
                pixel = (x, y)
                graph[pixel] = get_8_neighbors(image, x, y)  # Store its 8-neighbors
    return graph

# Enqueuing the Initial Boundary Pixels of the Object in the Image
def initialize_boundary_queue(image):
    boundary_queue = Queue()
    rows, cols = image.shape
    
    # Traversing through the Foreground (White) Image Pixels and Enqueuing the Boundary Pixels
    for x in range(1, rows - 1):  # Ignore Boundary Pixels
        for y in range(1, cols - 1):
            if image[x][y] == 1 and has_background_neighbor(image, x, y):
                boundary_queue.put((x, y))
    return boundary_queue

# Check if the Pixel has any Background Neighbor (Black Pixel)
def has_background_neighbor(image, x, y):
    neighbors = get_8_neighbors(image, x, y)
    return any(image[nx][ny] == 0 for nx, ny in neighbors)

# Get the 8-Neighbors of a Pixel while Ensuring they are within the Image Bounds
def get_8_neighbors(image, x, y):
    rows, cols = image.shape
    neighbors = []
    
    neighbor_positions = [(-1,  0), (-1,  1), ( 0,  1), ( 1,  1),( 1,  0), ( 1, -1), ( 0, -1), (-1, -1)]
    
    # Check if the Neighbors are within the Image Bounds
    for dx, dy in neighbor_positions:
        nx, ny = x + dx, y + dy
        if 0 <= nx < rows and 0 <= ny < cols:
            neighbors.append((nx, ny))
    
    return neighbors

# Count the Number of 0 -> 1 Transitions in the 8-Neighbors of a Pixel
def transitions(neighbors):
    n = neighbors + neighbors[0:1]
    return sum((n1, n2) == (0, 1) for n1, n2 in zip(n, n[1:]))

'''
Logic of the moveGen Function:

Dequeue the Boundary Pixel from the Queue while there are Boundary Pixels to Process and get the 8-Neighbors of the Pixel (P2, P3, P4, P5, P6, P7, P8, P9)
Apply the Zhang-Suen Conditions to Check if the Pixel can be Removed or Not, and then Convert the Pixel to Background (Black) Pixel along with Enqueuing its 
Neighbors as Potential New Boundary Pixels so that they can be Processed in the Next Iteration
'''

def moveGen(image, queue):
    # Initializing a Queue (to Store the Next Set of Boundary Pixels)
    next_boundary_queue = Queue()

    # Initialize Counters for Pixel Updates and Constraint Condition Checks
    pixel_updates = 0
    condition_checks = 0

    # While there are Boundary Pixels to Process
    while not queue.empty():
        x, y = queue.get()

        # Getting the 8-Neighbors of the Pixel
        neighbors_coords = get_8_neighbors(image, x, y)
        # Skip if the pixel has less than 8 neighbors
        if len(neighbors_coords) < 8:
            continue

        P2, P3, P4, P5, P6, P7, P8, P9 = [image[nx][ny] for nx, ny in neighbors_coords]
        n = [P2, P3, P4, P5, P6, P7, P8, P9]
        
        # Apply Zhang-Suen Conditions (Check if the Pixel can be Removed)
        condition_checks += 1  # Updating the Condition Checks Counter (When each Pixel is Checked for Constraint Conditions)
        if (image[x][y] == 1 and                # Condition 0: Pixel is a Foreground Pixel (White Pixel)
            2 <= sum(n) <= 6 and                # Condition 1: 2 <= N(P1) <= 6 (Number of Foreground Pixels in the 8-Neighbors is between 2 and 6)
            transitions(n) == 1 and             # Condition 2: S(P1) == 1 (Number of 0 -> 1 Transitions in the 8-Neighbors is 1)
            P2 * P4 * P6 == 0 and               # Condition 3: P2 * P4 * P6 == 0 (P2, P4, P6 are Foreground Pixels)
            P4 * P6 * P8 == 0):                 # Condition 4: P4 * P6 * P8 == 0 (P4, P6, P8 are Foreground Pixels)

            # Mark the Pixel for Removal (1 -> 0 or Background or Black Pixel)
            image[x][y] = 0
            pixel_updates += 1 # Updating the Pixel Updates Counter (When each Pixel is Marked for Removal)

            # Enqueuing its Neighbors as Potential New Boundary Pixels
            for nx, ny in neighbors_coords:
                if image[nx][ny] == 1:  # Ensure it's a Foreground Pixel
                    next_boundary_queue.put((nx, ny))
    # Return Updated Image, Next Set of Boundary Pixels, Pixel Updates, Condition Checks, and Number of Boundary Pixels
    return image, next_boundary_queue, pixel_updates, condition_checks, next_boundary_queue.qsize()

'''
Logic of the goalTest Function:
To Check if the Queue is Empty, i.e., No More Pixels to Process the Goal State is Reached
'''
def goalTest(queue):
    return queue.empty()

# Breadth First Search Traversal
def bfs_traversal(image): 
    
    # Initialize Counters and Timers for the BFS Traversal (Skeletonization)
    num_iterations = 0 # Number of Iterations (Number of Pixels Processed)
    total_pixel_updates = 0 # Total Number of Pixels Updated (Marked for Removal)
    total_condition_checks = 0 # Total Number of Zhang-Suen Condition Checks (Constraint Checks)
    start_time = time.time() # Start Time of the BFS Traversal
    
    # Initialize the Image into a Graph Representation (Adjacency List) and Enqueue the Initial Boundary Pixels
    graph = initialize_graph(image)
    boundary_queue = initialize_boundary_queue(image)
    max_queue_size = boundary_queue.qsize() # Tracking the Maximum Queue Size
    
    # Traversing through the Boundary Pixels and Applying Zhang-Suen Conditions
    while not goalTest(boundary_queue):
        num_iterations += 1
        image, boundary_queue, pixel_updates, condition_checks, queue_size = moveGen(image, boundary_queue) # Moving to the Next Boundary Pixel, Applying Conditions, and Enqueuing New Boundary Pixels
        
        total_pixel_updates += pixel_updates # 
        total_condition_checks += condition_checks
        max_queue_size = max(max_queue_size, queue_size) 
    
    end_time = time.time() # End Time of the BFS Traversal
    
    # Time Taken for the BFS Traversal
    time_taken = end_time - start_time
    
    print("Number of iterations:", num_iterations)
    print("Total pixel updates:", total_pixel_updates)
    print("Total Zhang-Suen condition checks:", total_condition_checks)
    print("Maximum boundary queue size:", max_queue_size)
    print("Total time taken (seconds):", time_taken)
    
    return image

##__main__##

# Reading the Image
image = cv2.imread('./image.png', cv2.IMREAD_GRAYSCALE)
image = cv2.resize(image, (100, 100))
image = np.where(image > 128, 1, 0)  # Binarize the Image

# Displaying the Original Image
plt.imshow(image, cmap='gray')
plt.title("Original Image")
plt.show()

# Applying BFS Traversal for Image Skeletonization
skeletonized_image = bfs_traversal(image)

# Displaying the Skeletonized Image
plt.imshow(skeletonized_image, cmap='gray')
plt.title("Skeletonized Image")
plt.show()

# Saving the Skeletonized Image
cv2.imwrite('./skeletonized_image.png', skeletonized_image * 255)