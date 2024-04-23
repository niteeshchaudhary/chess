import cv2
import numpy as np

# Load the image
image_path = 'boardimages/2.png'
image = cv2.imread(image_path)
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Apply Gaussian blur to reduce noise
gray_blur = cv2.GaussianBlur(gray, (5, 5), 0)

# Threshold the image to create a binary image
_, binary = cv2.threshold(gray_blur, 180, 255, cv2.THRESH_BINARY_INV)

# Find contours in the binary image
contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Find the contour with the maximum area
max_contour = max(contours, key=cv2.contourArea)

# Find the convex hull of the largest contour
hull = cv2.convexHull(max_contour)

# Get the bounding rectangle of the convex hull
x, y, w, h = cv2.boundingRect(hull)

# Draw the bounding rectangle on the original image
cv2.rectangle(image, (x, y), (x + w, y + h), (0, 0, 255), 2)

# Display the original image with the outer rectangle
cv2.imshow('Chessboard Detection', image)
cv2.waitKey(0)
cv2.destroyAllWindows()
