import pyautogui
import time

def drag_and_drop(start_x, start_y, end_x, end_y, duration=1):
    pyautogui.moveTo(start_x, start_y)
    pyautogui.mouseDown()
    # time.sleep(duration)  # Adjust duration as needed
    pyautogui.moveTo(end_x, end_y)
    pyautogui.mouseUp()

# Example usage
start_position = (590, 260)
end_position = (680, 460)
drag_and_drop(start_position[0], start_position[1], end_position[0], end_position[1])
