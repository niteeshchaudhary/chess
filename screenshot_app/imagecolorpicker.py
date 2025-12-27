import cv2

# Load the image
image = cv2.imread('screenshot.png')

# Specify the coordinates (x, y)
x, y = 400, 150  # Replace with your desired coordinates

# Get the RGB value of the pixel at (x, y)
rgb_value = image[y, x]  # OpenCV loads image in BGR format, so the order is [B, G, R]
print(f"Original RGB value at ({x},{y}): {rgb_value}")

# Change the pixel color to red (RGB: 255, 0, 0)

image[y-10:y+10, x-10:x+10] = [0, 0, 255]  # In OpenCV, BGR format is used, so Red is [0, 0, 255]
image[y,x] = [255, 0, 0] 
# Save the modified image
cv2.imwrite('output_image.jpg', image)

# Optionally, display the modified image
