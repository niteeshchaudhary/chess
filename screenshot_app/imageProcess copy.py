import cv2
import numpy as np

# Load the image
image = cv2.imread('sample.png')

# Convert to HSV color space
hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

# Define color ranges for green and red
green_lower = np.array([35, 50, 50])  # Adjust HSV values as needed
green_upper = np.array([85, 255, 255])

red_lower1 = np.array([0, 50, 50])
red_upper1 = np.array([10, 255, 255])
red_lower2 = np.array([170, 50, 50])
red_upper2 = np.array([180, 255, 255])

# Create masks for green and red
green_mask = cv2.inRange(hsv, green_lower, green_upper)
red_mask1 = cv2.inRange(hsv, red_lower1, red_upper1)
red_mask2 = cv2.inRange(hsv, red_lower2, red_upper2)
red_mask = cv2.bitwise_or(red_mask1, red_mask2)

# Create a black canvas
black_canvas = np.zeros_like(image)

# Apply the green mask
green_boxes = cv2.bitwise_and(image, image, mask=green_mask)

# Black out red boxes
red_boxes_blacked_out = cv2.bitwise_and(black_canvas, black_canvas, mask=red_mask)

# Combine green boxes with blacked-out image
output = cv2.add(green_boxes, red_boxes_blacked_out)

# Save the output image
cv2.imwrite('output_image.jpg', output)
