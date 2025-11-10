import cv2
import numpy as np
import os
import colorama
from colorama import Fore, Style

def generate_sketch_contours(image_path, status_callback=None):
    
    def log_status(message):
        """Helper to print to console AND send to GUI if available"""
        print(message)
        if status_callback:
            status_callback(message)

    log_status(f"{Fore.CYAN}Processing image: {image_path}")
    if not os.path.exists(image_path):
        log_status(f"{Fore.RED}Error: Image '{image_path}' not found.")
        return None, None, None
    
    image = cv2.imread(image_path)
    if image is None:
        log_status(f"{Fore.RED}Error: Failed to load image.")
        return None, None, None
        
    img_height, img_width, _ = image.shape
    img_info = {
        "height": img_height,
        "width": img_width,
        "center_x": img_width / 2.0,
        "center_y": img_height / 2.0,
    }

    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    blurred_image = cv2.GaussianBlur(gray_image, (5, 5), 0)

    v = np.median(blurred_image)
    sigma = 0.33
    lower_thresh = int(max(0, (1.0 - sigma) * v))
    upper_thresh = int(min(255, (1.0 + sigma) * v))

    edges = cv2.Canny(blurred_image, lower_thresh, upper_thresh)

    contours, _ = cv2.findContours(edges, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE) 
    
    if contours:
        log_status(f"{Fore.GREEN}  -> Found {len(contours)} sketch contours (including details).")
    else:
        log_status(f"{Fore.YELLOW}  -> No contours found for the sketch.")

    return contours, img_info, image

if __name__ == "__main__":
    
    colorama.init(autoreset=True)

    DEFAULT_INPUT_IMAGE = "images/test_image2.png" 
    DEFAULT_OUTPUT_IMAGE = "sketch.png"       

    print(f"{Fore.CYAN}{Style.BRIGHT}--- Running standalone image processing test (Canny Edge Sketch) ---")
    
    contours, img_info, _ = generate_sketch_contours(DEFAULT_INPUT_IMAGE)
    
    if contours and img_info:
        canvas = np.ones((img_info["height"], img_info["width"], 3), dtype=np.uint8) * 255
        print(f"{Fore.YELLOW}Rendering preview...")
        
        cv2.drawContours(canvas, contours, -1, (0, 0, 0), 1) 
        
        cv2.imwrite(DEFAULT_OUTPUT_IMAGE, canvas)
        print(f"{Fore.GREEN}{Style.BRIGHT}Successfully created sketch preview: '{DEFAULT_OUTPUT_IMAGE}' (Total {len(contours)} contours)")
    else:
        print(f"{Fore.RED}Failed to process image.")