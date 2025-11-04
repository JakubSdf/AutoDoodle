import cv2
import numpy as np
import os

def generate_sketch_contours(image_path):
    """
    Loads an image, uses Canny edge detection to create a sketch,
    and returns ALL contours of that sketch (outer and inner).
    This function is designed to work for any general image.
    """
    print(f"Processing image: {image_path}")
    if not os.path.exists(image_path):
        print(f"Error: Image '{image_path}' not found.")
        return None, None, None
    
    image = cv2.imread(image_path)
    if image is None:
        print("Error: Failed to load image.")
        return None, None, None
        
    img_height, img_width, _ = image.shape
    img_info = {
        "height": img_height,
        "width": img_width,
        "center_x": img_width / 2.0,
        "center_y": img_height / 2.0,
    }

    # 1. Convert to grayscale
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # 2. Apply Gaussian blur to reduce noise (crucial for Canny)
    blurred_image = cv2.GaussianBlur(gray_image, (5, 5), 0)

    # 3. Calculate adaptive Canny thresholds
    # This makes the detector more robust for different images.
    v = np.median(blurred_image)
    sigma = 0.33
    lower_thresh = int(max(0, (1.0 - sigma) * v))
    upper_thresh = int(min(255, (1.0 + sigma) * v))

    # 4. Apply Canny edge detection
    edges = cv2.Canny(blurred_image, lower_thresh, upper_thresh)

    # 5. Find contours from the edges
    # cv2.RETR_LIST finds all contours, which we need for inner details.
    contours, _ = cv2.findContours(edges, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE) 
    
    if contours:
        print(f"  -> Found {len(contours)} sketch contours (including details).")
    else:
        print(f"  -> No contours found for the sketch.")

    return contours, img_info, image


# --- Standalone Test Block ---
if __name__ == "__main__":
    
    # Use the image path from main.py for consistency
    DEFAULT_INPUT_IMAGE = "images/test_image2.png" 
    DEFAULT_OUTPUT_IMAGE = "sketch.png"       

    print("--- Running standalone image processing test (Canny Edge Sketch) ---")
    
    contours, img_info, _ = generate_sketch_contours(DEFAULT_INPUT_IMAGE)
    
    if contours and img_info:
        # Create a white canvas
        canvas = np.ones((img_info["height"], img_info["width"], 3), dtype=np.uint8) * 255
        print("Rendering preview...")
        
        # Draw all found contours in black
        cv2.drawContours(canvas, contours, -1, (0, 0, 0), 1) 
        
        cv2.imwrite(DEFAULT_OUTPUT_IMAGE, canvas)
        print(f"Successfully created sketch preview: '{DEFAULT_OUTPUT_IMAGE}' (Total {len(contours)} contours)")
    else:
        print("Failed to process image.")