# AutoDoodle - Instagram DM Drawing Bot

AutoDoodle is a Python bot that automatically draws any image as a sketch directly inside **Instagram DMs**.

It uses a modern GUI control panel to manage the entire process, from file selection to calibration, and includes an embedded console for status updates. It is designed to run on a PC using an **Android emulator** (e.g., BlueStacks) with the Instagram app running.

## 1. What You Need Before You Start

1.  **Python (and Pip)**: [https://www.python.org/downloads/](https://www.python.org/downloads/)
    *(During installation, make sure to check the box that says "Add Python to PATH")*
2.  **Git**: [https://git-scm.com/downloads](https://git-scm.com/downloads)
3.  **Android Emulator (BlueStacks Recommended)**: [https://www.bluestacks.com/](https://www.bluestacks.com/)
4.  **Instagram App**: Installed *inside* your emulator and logged in.

## 2. Installation

1.  **Clone the repository:**
    ```sh
    git clone https://github.com/JakubSdf/AutoDoodle.git
    ```
2.  **Move into the folder and install libraries:**
    ```sh
    cd AutoDoodle
    pip install -r requirements.txt
    ```
    *(This will install `pyautogui`, `opencv-python`, `ttkbootstrap`, and all other required libraries.)*

## 3. Configuration

1.  **`config.json`:**
    * Open `config.json` in a text editor.
    * Review all settings. You can add your own UI-matching images (like `plus_icon_dark.png`) to the lists. The script will *not* crash if an image is missing; it will just print a warning and skip it.
    * Set the hotkeys (`stop_key`, `pause_key`) to your preference.

## 4. How to Use

1.  **Prepare the Emulator:**
    * Open BlueStacks and the Instagram app.
    * Go to your DMs and open the conversation where you want to draw.

2.  **Run the Script:**
    * Run the main script from your terminal:
        ```sh
        python main.py
        ```
    * The **AutoDoodle Control Panel** GUI will appear.

3.  **Using the GUI:**
    * **Step 0: Select Image:** Click "Select Image" and choose the picture you want to draw.
    * **Step 1: Calibrate:** Click "1. Calibrate Canvas". The GUI will disappear.
        * Follow the prompts in that terminal (click top-left, then bottom-right of the drawing area).
        * The GUI will reappear when done.
    * **Step 2: Start:** Click "2. Start Drawing". The bot will now take over your mouse.
    * **Step 3: Select Color:** The bot will open the draw interface and pause. Select your color in the app, then **click your mouse** to confirm and start the drawing.
    * **Console:** Check the "Show Console" box in the GUI to see a live feed of the bot's status and actions, all in one window.

## 5. Drawing Controls (Hotkeys)

* **PAUSE / RESUME:** Press the **'space'** key (or your key from `config.json`) to pause the drawing. This allows you to change colors. Press it again to resume.
* **STOP:** To stop the bot completely, press and hold the **'q'** key (or your key from `config.json`).