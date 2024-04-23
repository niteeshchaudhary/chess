import cv2
import numpy as np

# Load the image
image = cv2.imread('images/2.jpg')

# Convert the image to grayscale
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Detect edges using Canny edge detection
edges = cv2.Canny(gray, 50, 150, apertureSize=3)

# Find contours in the edge-detected image
contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Filter out contours based on their area to detect the chessboard
for contour in contours:
    area = cv2.contourArea(contour)
    if area > 50000:  # Adjust the threshold based on your image
        peri = cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, 0.02 * peri, True)
        if len(approx) == 4:  # If the contour has 4 corners
            cv2.drawContours(image, [approx], 0, (0, 255, 0), 5)  # Outline the chessboard

            # Draw a grid over the chessboard
            rows, cols = 8, 8
            for i in range(rows + 1):
                cv2.line(image, tuple(approx[0][0]), tuple(approx[0][0] + [0, i * (approx[1][0][1] - approx[0][0][1]) // rows]), (0, 0, 255), 2)
            for i in range(cols + 1):
                cv2.line(image, tuple(approx[0][0]), tuple(approx[0][0] + [i * (approx[3][0][0] - approx[0][0][0]) // cols, 0]), (0, 0, 255), 2)

# Display the result
cv2.imshow('Chessboard Detection', image)
cv2.waitKey(0)
cv2.destroyAllWindows()
