import cv2
import easyocr
from PIL import ImageGrab
import pyautogui as pg
import numpy as np
import requests
import time
import os
import math
import random
from groq import Groq
import re
import base64
import gchatimageprocess as gimp

# Function to encode the image
def encode_image(image_path):
  with open(image_path, "rb") as image_file:
    return base64.b64encode(image_file.read()).decode('utf-8')

def clean_text(text):
    text = re.sub(r'[^\x00-\x7F]+', '', text) 
    text = re.sub(r'\s+', ' ', text) 
    return text.strip()


# Initialize EasyOCR reader
reader = easyocr.Reader(['en'])

def merge_arrays(arr1, arr2):
    # Reverse both arrays to start from the end
    arr1.reverse()
    arr2.reverse()

    # Initialize an empty list to hold the merged result
    merged = []

    # Iterate through both arrays and merge them alternately
    while arr1 or arr2:
        if arr1:
            merged.append("other: "+arr1.pop(0))  # Add element from the first array
        if arr2:
            merged.append("me: "+arr2.pop(0))  # Add element from the second array

    return merged

# # Example usage
# arr1 = ["first1", "first2", "first3"]
# arr2 = ["second1", "second2", "second3"]

# result = merge_arrays(arr1, arr2)


def preprocess_image(image):
    """Preprocess the image to enhance text detection."""
    # Thresholding to highlight text
    _, binary_image = cv2.threshold(image, 150, 255, cv2.THRESH_BINARY_INV)
    
    # Dilation to make text more visible
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2))
    dilated_image = cv2.dilate(binary_image, kernel, iterations=1)
    return dilated_image

def extract_text_from_image(image):
    """Extract text from an image using EasyOCR."""
    mine=[254, 243, 236]
    opp=[242,242,242]
    img=image.copy()
    my_chat=gimp.get_req_image(img,opp)
    my=[text for _, text, _ in reader.readtext(my_chat)]
    img=image.copy()
    other_chat=gimp.get_req_image(img,mine)
    other=[text for _, text, _ in reader.readtext(other_chat)]
    cv2.imwrite('other_chat.jpg', other_chat)
    results = reader.readtext(image)
    print("~"*25)
    print(my)
    print("--"*25)
    print(other)
    # Concatenate detected text into a single string
    extracted_text = " ".join([text for _, text, _ in results])
    print("**"*25)

    
    return merge_arrays(other, my)


img=cv2.imread("screenshot.png")
print(extract_text_from_image(img)[::-1])

