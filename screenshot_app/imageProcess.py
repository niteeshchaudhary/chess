import cv2
import numpy as np

# Load the image
image = cv2.imread('screenshot.png')


white_rgb = np.array([255, 255, 255])  # White in BGR format

# Create a mask where pixels exactly match the white color
# This compares each pixel in the image to the white color
mask = np.all(image == white_rgb, axis=-1)

# Create a black canvas of the same size as the image
black_canvas = np.zeros_like(image)

# Black out the areas where the mask is True (white pixels)
image[mask] = [0, 0, 0]  




# Define the target color (BGR format: [236, 243, 254] which is RGB: 254, 243, 236)
target_rgb = np.array([254, 243, 236])
# target_rgb = np.array([242,242,242])

# Define a range around the target color to account for slight variations
# lower_bound = np.array([235, 230, 225])  # Lower bound for the color range
# upper_bound = np.array([255, 250, 245])  # Upper bound for the color range

# Create a mask where the pixels fall within the color range
mask = cv2.inRange(image, target_rgb, target_rgb)

# Perform dilation to expand the mask and include the inside of the color block
kernel = np.ones((10,10), np.uint8)  # The size of the kernel determines how much the mask expands
expanded_mask = cv2.dilate(mask, kernel, iterations=1)

# Create a black canvas of the same size as the original image
black_canvas = np.zeros_like(image)

# Use the expanded mask to replace matching areas with black
image[expanded_mask != 0] = [0, 0, 0]





# target_rgb = np.array([254, 243, 236])
target_rgb = np.array([0,0,0])

# Define a range around the target color to account for slight variations
# lower_bound = np.array([235, 230, 225])  # Lower bound for the color range
# upper_bound = np.array([255, 250, 245])  # Upper bound for the color range

# Create a mask where the pixels fall within the color range
mask = cv2.inRange(image, target_rgb, target_rgb)

# Perform dilation to expand the mask and include the inside of the color block
kernel = np.ones((10,10), np.uint8)  # The size of the kernel determines how much the mask expands
expanded_mask = cv2.dilate(mask, kernel, iterations=1)

# Create a black canvas of the same size as the original image
black_canvas = np.zeros_like(image)

# Use the expanded mask to replace matching areas with black
image[expanded_mask != 0] = [0, 0, 0]


# Save the modified image
cv2.imwrite('output_image.jpg', image)

