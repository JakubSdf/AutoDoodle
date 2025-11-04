import pyautogui
import time
import os
import keyboard
import mouse
import image_processor 

# --- 1. MAIN CONFIGURATION ---
INPUT_IMAGE_PATH = "images/test_image2.png" # Updated to your last request
PLUS_ICON_FILE = "plus_icon.png"
THICKNESS_SLIDER_HANDLE_FILE = "thickness_slider_handle.png"
THICKNESS_SLIDER_HANDLE_ALT_FILE = "thickness_slider_handle_alt.png" # Alternate slider handle
DRAW_BUTTON_Y_OFFSET = 75 
THICKNESS_ADJUST_OFFSET_Y = 20 # Pixels to click *below* the handle for a thinner line

STOP_KEY = 'q'
DRAWING_SPEED = 0 # This is the pause between each pyautogui action

# --- 2. HELPER FUNCTIONS ---

def calibrate_canvas():
    """Asks the user to click the corners of the target drawing area."""
    print("\n--- STEP 1: MANUAL CANVAS CALIBRATION ---")
    try:
        print("\nPlease CLICK the TOP-LEFT corner of the drawing area...")
        mouse.wait(mouse.LEFT, target_types=mouse.DOWN)
        x1, y1 = pyautogui.position()
        mouse.wait(mouse.LEFT, target_types=mouse.UP)
        print(f"Top-left corner set to: ({x1}, {y1})")
        time.sleep(0.5)
        
        print("\nGreat. Now CLICK the BOTTOM-RIGHT corner of the drawing area...")
        mouse.wait(mouse.LEFT, target_types=mouse.DOWN)
        x2, y2 = pyautogui.position()
        mouse.wait(mouse.LEFT, target_types=mouse.UP)
        print(f"Bottom-right corner set to: ({x2}, {y2})")
        time.sleep(0.5)
        
        w = x2 - x1
        h = y2 - y1
        if w <= 0 or h <= 0:
            print("Error: Invalid dimensions.")
            return None
        center_x = x1 + w / 2.0
        center_y = y1 + h / 2.0
        return (x1, y1, w, h, center_x, center_y)
    except Exception as e:
        print(f"An error occurred during calibration: {e}")
        return None

# --- 3. MAIN SCRIPT LOGIC ---
def main():
    # Step 1: Calibrate
    canvas_info = calibrate_canvas()
    if canvas_info is None: return
    canvas_x, canvas_y, canvas_w, canvas_h, canvas_center_x, canvas_center_y = canvas_info
    print(f"\nCanvas calibrated successfully! Dimensions: {canvas_w}x{canvas_h}")

    # Step 2: Open "Draw" UI
    print("\n--- STEP 2: UI AUTOMATION ---")
    plus_coords = None
    try:
        plus_coords = pyautogui.locateCenterOnScreen(PLUS_ICON_FILE, confidence=0.8)
    except Exception as e:
        print(f"Error finding 'plus' icon: {e}")
        return
        
    if plus_coords:
        pyautogui.click(plus_coords)
        time.sleep(0.5)
        pyautogui.click(plus_coords.x, plus_coords.y - DRAW_BUTTON_Y_OFFSET)
        print("Successfully opened drawing interface.")
        time.sleep(1)
    else:
        print(f"Could not find 'plus' icon ('{PLUS_ICON_FILE}'). Exiting.")
        return

    # Step 2.5: Set Brush Thickness
    print("\n--- STEP 2.5: SETTING BRUSH THICKNESS ---")
    thickness_handle_coords = None
    
    # Try to find the primary handle image
    try:
        thickness_handle_coords = pyautogui.locateCenterOnScreen(THICKNESS_SLIDER_HANDLE_FILE, confidence=0.8)
        if thickness_handle_coords:
            print(f"Found primary thickness slider: '{THICKNESS_SLIDER_HANDLE_FILE}'.")
    except Exception:
        pass # Silently fail, will try alternate
        
    # If primary not found, try alternate
    if not thickness_handle_coords:
        try:
            thickness_handle_coords = pyautogui.locateCenterOnScreen(THICKNESS_SLIDER_HANDLE_ALT_FILE, confidence=0.8)
            if thickness_handle_coords:
                print(f"Found alternate thickness slider: '{THICKNESS_SLIDER_HANDLE_ALT_FILE}'.")
        except Exception:
            pass # Silently fail

    if thickness_handle_coords:
        # Click below the found handle to set a thinner line
        target_x = thickness_handle_coords.x
        target_y = thickness_handle_coords.y + THICKNESS_ADJUST_OFFSET_Y
        pyautogui.click(target_x, target_y)
        print(f"Brush thickness set by clicking at ({target_x}, {target_y}).")
        time.sleep(0.5)
    else:
        print(f"Warning: Could not find any thickness slider icon. Using default thickness.")

    # Step 3: Process Image
    print("\n--- STEP 3: IMAGE PROCESSING ---")
    contours_list, img_info, _ = image_processor.generate_sketch_contours(
        INPUT_IMAGE_PATH
    )
    if contours_list is None:
        print("Image processing failed. Exiting.")
        return
        
    img_width, img_height = img_info["width"], img_info["height"]
    img_center_x, img_center_y = img_info["center_x"], img_info["center_y"]
    print(f"Image loaded (Dimensions: {img_width}x{img_height})")
    
    # Step 4: Calculate Scale
    print("\n--- STEP 4: CALCULATING SCALE ---")
    scale_x = canvas_w / img_width
    scale_y = canvas_h / img_height
    SCALE_FACTOR = min(scale_x, scale_y) * 0.9 # 0.9 = 90% margin
    print(f"Auto-calculated scale factor: {SCALE_FACTOR:.2f}")

    # Step 5: Draw
    print(f"\n--- STEP 5: DRAWING ---")
    print(f"Drawing {len(contours_list)} contours...")
    print(f"ATTENTION: Drawing will begin in 3 seconds.")
    print(f"TO STOP IMMEDIATELY: Press and hold the '{STOP_KEY}' key.")
    
    time.sleep(3)
    pyautogui.PAUSE = DRAWING_SPEED

    try:
        for contour in contours_list:
            if keyboard.is_pressed(STOP_KEY): raise KeyboardInterrupt
            
            # Skip very small contours (likely noise)
            if len(contour) < 4:
                continue

            first_point = contour[0][0]
            scaled_x = int(canvas_center_x + (first_point[0] - img_center_x) * SCALE_FACTOR)
            scaled_y = int(canvas_center_y + (first_point[1] - img_center_y) * SCALE_FACTOR)
            
            pyautogui.moveTo(scaled_x, scaled_y)
            pyautogui.mouseDown()

            for point in contour[1:]:
                if keyboard.is_pressed(STOP_KEY): raise KeyboardInterrupt
                
                scaled_x = int(canvas_center_x + (point[0][0] - img_center_x) * SCALE_FACTOR)
                scaled_y = int(canvas_center_y + (point[0][1] - img_center_y) * SCALE_FACTOR)
                pyautogui.dragTo(scaled_x, scaled_y)

            pyautogui.mouseUp()
        
        print("\nDone! Drawing complete.")

    except KeyboardInterrupt:
        print(f"\nSTOP: '{STOP_KEY}' key detected. Stopping script.")
    except pyautogui.FailSafeException:
        print(f"\nSTOP: Failsafe triggered (mouse moved to corner). Stopping script.")
    except Exception as e:
        print(f"\nAn error occurred during drawing: {e}")
    finally:
        pyautogui.mouseUp() # Ensure mouse is always released on exit
        print("Mouse button released. Script terminating.")

if __name__ == "__main__":
    main()