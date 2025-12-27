import cv2
import numpy as np
from PIL import ImageGrab
import pyautogui
import time


def capture_chat_window(bbox): #bbox
    """Capture a specific region of the screen."""
    screenshot = ImageGrab.grab(bbox=bbox)  # Capture only the chat window
    screenshot_np = np.array(screenshot)  # Convert to numpy array
    print(screenshot_np)
    # screenshot_gray = cv2.cvtColor(screenshot_np, cv2.COLOR_BGR2GRAY)
    return screenshot_np #screenshot_gray

def detect_first_blue_dot(image_path):
    # Load the image
    image = cv2.imread(image_path)
    if image is None:
        print(f"Error: Unable to load image at {image_path}")
        return None

    # Convert the image to HSV color space
    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # Define the range for the blue color
    lower_blue = np.array([155, 92, 0])  # Adjust these values if necessary
    upper_blue = np.array([155, 92, 0])

    # Create a mask for the blue color
    blue_mask = cv2.inRange(hsv_image, lower_blue, upper_blue)

    # Apply morphological operations to reduce noise
    kernel = np.ones((3, 3), np.uint8)
    blue_mask = cv2.morphologyEx(blue_mask, cv2.MORPH_OPEN, kernel, iterations=2)
    blue_mask = cv2.dilate(blue_mask, kernel, iterations=1)

    # Find contours in the mask
    contours, _ = cv2.findContours(blue_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if not contours:
        print("No blue dots detected.")
        return None

    # Sort contours by area, largest to smallest
    contours = sorted(contours, key=cv2.contourArea, reverse=True)

    # Select the first contour
    first_contour = contours[0]

    # Get the bounding box coordinates of the first blue dot
    x, y, w, h = cv2.boundingRect(first_contour)

    # Print the location of the first blue dot
    print(f"First blue dot found at: x={x}, y={y}, width={w}, height={h}")

    # Return the center point of the detected blue dot for clicking
    center_x = x + w // 2
    center_y = y + h // 2
    return (center_x, center_y)

def click_on_blue_dot(image_path):
    # Detect the blue dot location
    dot_location = detect_first_blue_dot(image_path)

    if dot_location is not None:
        # Move the mouse to the detected location and click
        pyautogui.moveTo(dot_location[0], dot_location[1], duration=0.5)  # Move to the location
        pyautogui.click()  # Perform the click
        print("Mouse clicked at the blue dot location.")
    else:
        print("No blue dot to click.")


def monitor_chat(bbox):
    """Continuously monitor chat window for new messages."""
    last_text = ""
    while True:
        # Capture chat window and preprocess image
        screenshot = capture_chat_window(bbox)
        cv2.imwrite("ss.png", screenshot)
        click_on_blue_dot("ss.png")
        
        # processed_image = preprocess_image(screenshot)
        
        # # Extract text from the processed image
        # current_text = extract_text_from_image(processed_image)

        # # Check for new message
        # if detect_new_message(last_text, current_text):
        #     print(f"New message detected: {current_text}")
        #     # reply_to_message(current_text)
        #     last_text = current_text  # Update last text

        # Pause for a short period before capturing again
        time.sleep(10)

# Example usage
if __name__ == "__main__":
    
    # Define the bounding box (bbox) for the Google Chat window (left, top, right, bottom)
    # Adjust coordinates based on your screen resolution and chat window location
    CHAT_WINDOW_BBOX = (0, 0, 1900, 1100)  # Example coordinates

    monitor_chat(CHAT_WINDOW_BBOX)
    
