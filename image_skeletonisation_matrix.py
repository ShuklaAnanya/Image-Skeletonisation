'''
Image Skeletonisation using Zhang-Suen Algorithm (Matrix Implementation)

Reference:
Page 48-50
"Character Recognition Systems: A Guide for Students and Practitioners" 
By Mohamed Cheriet, Nawwaf Kharma, Cheng-Lin Liu, Ching Suen
'''

# Importing Libraries
import numpy as np
import time
import matplotlib.pyplot as plt
from skimage import io
from skimage.filters import threshold_otsu

# Neighbors Function
'''
P1 - Current Pixel
P2, P3, P4, P5 - Top, Top Right, Right, Bottom Right
P6, P7, P8, P9 - Bottom, Bottom Left, Left, Top Left
'''
def neighbours(x, y, image):
    x1, y1 = x - 1, y - 1
    x2, y2 = x + 1, y + 1
    return [image[x1][y], image[x1][y2], image[x][y2], image[x2][y2],  # P2, P3, P4, P5
            image[x2][y], image[x2][y1], image[x][y1], image[x1][y1]]  # P6, P7, P8, P9

# Transition Count Function (Counting 0-1 Transitions)
def transitions(neighbours):
    n = neighbours + neighbours[0:1]  # Circular List
    return sum((n1, n2) == (0, 1) for n1, n2 in zip(n, n[1:]))

# Zhang-Suen Thinning Algorithm
def zhangSuen_with_metrics(image):
    # Initialize Counters
    num_iterations = 0
    total_pixel_updates = 0
    total_condition_checks = 0
    start_time = time.time()
    
    Image_Thinned = image.copy()
    changing1 = changing2 = True
    
    rows, columns = Image_Thinned.shape  # Image Dimensions
    
    while changing1 or changing2:  # Iterate until no more changes
        changing1 = []
        num_iterations += 1
        
        # Zhang-Suen Thinning Algorithm - Checking
        for x in range(1, rows - 1):
            for y in range(1, columns - 1):
                P2, P3, P4, P5, P6, P7, P8, P9 = n = neighbours(x, y, Image_Thinned)
                total_condition_checks += 1  # Counting each pixel check
                if (Image_Thinned[x][y] == 1 and
                    2 <= sum(n) <= 6 and
                    transitions(n) == 1 and
                    P2 * P4 * P6 == 0 and
                    P4 * P6 * P8 == 0):
                    changing1.append((x, y))
        
        # Applying Changes
        for x, y in changing1:
            Image_Thinned[x][y] = 0
            total_pixel_updates += 1
        
        # Zhang-Suen Thinning Algorithm - Removing
        changing2 = []
        for x in range(1, rows - 1):
            for y in range(1, columns - 1):
                P2, P3, P4, P5, P6, P7, P8, P9 = n = neighbours(x, y, Image_Thinned)
                total_condition_checks += 1  # Count each pixel check
                if (Image_Thinned[x][y] == 1 and
                    2 <= sum(n) <= 6 and
                    transitions(n) == 1 and
                    P2 * P4 * P8 == 0 and
                    P2 * P6 * P8 == 0):
                    changing2.append((x, y))
        
        # Updating the Image
        for x, y in changing2:
            Image_Thinned[x][y] = 0
            total_pixel_updates += 1
    
    end_time = time.time()
    time_taken = end_time - start_time
    
    print(f"Number of iterations: {num_iterations}")
    print(f"Total pixel updates: {total_pixel_updates}")
    print(f"Total Zhang-Suen condition checks: {total_condition_checks}")
    print(f"Total time taken (seconds): {time_taken:.4f}")
    
    return Image_Thinned

# Image Generation and Skeletonization
image1 = "/Users/ananyashukla/Desktop/Ananya_Shukla/Semester 5/SMAI/blob.png"
image2 = "/Users/ananyashukla/Desktop/Ananya_Shukla/Semester 5/SMAI/connectfour.png"
image3 = "/Users/ananyashukla/Desktop/Ananya_Shukla/Semester 5/SMAI/dots.png"
image4 = "/Users/ananyashukla/Desktop/Ananya_Shukla/Semester 5/SMAI/fist.jpeg"
image5 = "/Users/ananyashukla/Desktop/Ananya_Shukla/Semester 5/SMAI/hand.jpeg"
image6 = "/Users/ananyashukla/Desktop/Ananya_Shukla/Semester 5/SMAI/horse.png"
image7 = "/Users/ananyashukla/Desktop/Ananya_Shukla/Semester 5/SMAI/lines.png"
image8 = "/Users/ananyashukla/Desktop/Ananya_Shukla/Semester 5/SMAI/multi_shapes.png"
image9 = "/Users/ananyashukla/Desktop/Ananya_Shukla/Semester 5/SMAI/shape.png"
image10 = "/Users/ananyashukla/Desktop/Ananya_Shukla/Semester 5/SMAI/tree.png"

# Make a dict to store all image paths
images = {
    "blob": image1,
    "connectfour": image2,
    "dots": image3,
    "fist": image4,
    "hand": image5,
    "horse": image6,
    "lines": image7,
    "multi_shapes": image8,
    "shape": image9,
    "tree": image10
}

print("Image Skeletonization using BFS Traversal Algorithm")
# For all images
for image_name, image_path in images.items():
    print("\nImage:", image_name)
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    image = cv2.resize(image, (100, 100))
    image = np.where(image > 127, 1, 0)

    # Displaying the Original Image
    plt.figure(figsize=(10, 10))
    plt.subplot(1, 2, 1)
    plt.title("Original Image")
    plt.imshow(image, cmap='gray')

    # Applying Zhang-Suen Thinning Algorithm
    skeletonized_image = zhangSuen_with_metrics(image)

    # Displaying the Skeletonized Image
    plt.subplot(1, 2, 2)
    plt.title("Skeletonized Image")
    plt.imshow(skeletonized_image, cmap='gray')
    plt.show()
