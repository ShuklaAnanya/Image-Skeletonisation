# Importing Libraries
import time
import numpy as np
import cv2
import heapq                        # Priority Queue
import matplotlib.pyplot as plt

# Image to Graph Representation (Adjacency List)
def initialize_graph(image):
    graph = {}
    rows, cols = image.shape
    for x in range(rows):
        for y in range(cols):
            if image[x][y] == 1:  # Processing Foreground Pixels (White) Only
                pixel = (x, y)
                graph[pixel] = get_8_neighbors(image, x, y) # Storing its 8-Neighbors
    return graph

'''
Heuristic Function Logic
Calculates the Number of Black Pixels in the 8-Neighbors of a Pixel, which is used to Prioritize Pixels

The more background pixels surrounding the current pixel, the higher its heuristic value. 
This means the pixel is closer to the edge of the foreground and is more likely to be considered for removal (skeletonization) in the next step. 
'''
def heuristic(image, x, y):
    return sum(1 for nx, ny in get_8_neighbors(image, x, y) if image[nx][ny] == 0)

# Initialize a Priority Queue with Boundary Pixels and their Heuristic Values
def initialize_boundary_priority_queue(image):
    boundary_queue = []
    rows, cols = image.shape
    for x in range(1, rows - 1): # Ignore Boundary Pixels
        for y in range(1, cols - 1):
            if image[x][y] == 1 and has_background_neighbor(image, x, y):
                priority = heuristic(image, x, y)
                heapq.heappush(boundary_queue, (priority, (x, y))) # Enqueue with Priority (Heuristic) Pixels
    return boundary_queue

# Check if the Pixel has any Background Neighbor (Black Pixel)
def has_background_neighbor(image, x, y):
    neighbors = get_8_neighbors(image, x, y)
    return any(image[nx][ny] == 0 for nx, ny in neighbors)

# Get the 8-Neighbors of a Pixel while Ensuring they are within the Image Bounds
def get_8_neighbors(image, x, y):
    rows, cols = image.shape
    neighbors = []
    neighbor_positions = [(-1,  0), (-1,  1), ( 0,  1), ( 1,  1), ( 1,  0), ( 1, -1), ( 0, -1), (-1, -1)]
    for dx, dy in neighbor_positions:
        nx, ny = x + dx, y + dy
        if 0 <= nx < rows and 0 <= ny < cols:
            neighbors.append((nx, ny))
    return neighbors

# Count the Number of 0 -> 1 Transitions in the 8-Neighbors of a Pixel
def transitions(neighbors):
    n = neighbors + neighbors[0:1]
    return sum((n1, n2) == (0, 1) for n1, n2 in zip(n, n[1:]))

def moveGen(image, priority_queue):
    next_priority_queue = []
    pixel_updates = 0
    condition_checks = 0
    while priority_queue:
        _, (x, y) = heapq.heappop(priority_queue)

        # Getting the 8-Neighbors of the Pixel
        neighbors_coords = get_8_neighbors(image, x, y)
        if len(neighbors_coords) < 8:
            continue

        P2, P3, P4, P5, P6, P7, P8, P9 = [image[nx][ny] for nx, ny in neighbors_coords]
        n = [P2, P3, P4, P5, P6, P7, P8, P9]

        # Apply Zhang-Suen Conditions (Check if the Pixel can be Removed)
        condition_checks += 1
        if (image[x][y] == 1 and 2 <= sum(n) <= 6 and transitions(n) == 1 and
                P2 * P4 * P6 == 0 and P4 * P6 * P8 == 0):
            image[x][y] = 0
            pixel_updates += 1

            # Enqueuing its Neighbors as Potential New Boundary Pixels with Updated Heuristic Values
            for nx, ny in neighbors_coords:
                if image[nx][ny] == 1:
                    priority = heuristic(image, nx, ny)
                    heapq.heappush(next_priority_queue, (priority, (nx, ny)))

    return image, next_priority_queue, pixel_updates, condition_checks, len(next_priority_queue)

# Check if the Priority Queue is Empty (Goal Test)
def goalTest(priority_queue):
    return len(priority_queue) == 0

# Best First Search Traversal for Image Skeletonization
def best_first_search_traversal(image):
    num_iterations = 0
    total_pixel_updates = 0
    total_condition_checks = 0
    start_time = time.time()

    graph = initialize_graph(image)
    priority_queue = initialize_boundary_priority_queue(image)
    max_queue_size = len(priority_queue)

    while not goalTest(priority_queue):
        num_iterations += 1
        image, priority_queue, pixel_updates, condition_checks, queue_size = moveGen(image, priority_queue)
        total_pixel_updates += pixel_updates
        total_condition_checks += condition_checks
        max_queue_size = max(max_queue_size, queue_size)

    end_time = time.time()
    time_taken = end_time - start_time

    print("Number of iterations:", num_iterations)
    print("Total pixel updates:", total_pixel_updates)
    print("Total Zhang-Suen condition checks:", total_condition_checks)
    print("Maximum priority queue size:", max_queue_size)
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
skeletonized_image = best_first_search_traversal(image)

# Displaying the Skeletonized Image
plt.imshow(skeletonized_image, cmap='gray')
plt.title("Skeletonized Image")
plt.show()

# Saving the Skeletonized Image
cv2.imwrite('./skeletonized_image.png', skeletonized_image * 255)