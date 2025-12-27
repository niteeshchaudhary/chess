import cv2
import numpy as np

def find_and_outline_blocks(image_path, target_colors, tolerance=20):
    # Read the image
    image = cv2.imread(image_path)
    # Convert the image to RGB (OpenCV loads images in BGR format)
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    all_contours = []

    # Loop through each target color
    for target_color in target_colors:
        # Define the target color range with some tolerance
        lower_bound = np.array([max(0, target_color[0] - tolerance),
                                max(0, target_color[1] - tolerance),
                                max(0, target_color[2] - tolerance)])
        upper_bound = np.array([min(255, target_color[0] + tolerance),
                                min(255, target_color[1] + tolerance),
                                min(255, target_color[2] + tolerance)])

        # Create a mask for the target color
        mask = cv2.inRange(image_rgb, lower_bound, upper_bound)

        # Find contours in the mask
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # Append the contours to the list
        all_contours.extend(contours)

    # Sort all contours by the vertical (y-coordinate) position of the bounding box
    all_contours = sorted(all_contours, key=lambda c: cv2.boundingRect(c)[1])

    # Draw bounding boxes and add numbers to each block
    for idx, contour in enumerate(all_contours):
        # Get the bounding box of each contour
        x, y, w, h = cv2.boundingRect(contour)

        # Draw a red rectangle around the block
        cv2.rectangle(image, (x, y), (x + w, y + h), (255, 0, 255), 2)

        # Add sequential numbering to the block
        cv2.putText(image, str(idx + 1), (x + 5, y + 15), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)

    # Save or display the result
    result_image_path = 'outlined_blocks.jpg'
    cv2.imwrite(result_image_path, image)

    return result_image_path

# Example usage
target_colors = [(242, 242, 242), (236, 243, 254)]  # Red and Green colors in RGB format
image_path = 'screenshot.png'  # Replace with your image path
find_and_outline_blocks(image_path, target_colors)
