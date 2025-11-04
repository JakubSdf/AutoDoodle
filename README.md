# AutoDoodle - Instagram DM Drawing Bot

AutoDoodle is a Python bot that automatically draws any image as a sketch directly inside **Instagram DMs**.

It is designed to run on a PC using an **Android emulator** (e.g., BlueStacks) with the Instagram app running. It processes a source image and then takes control of your mouse to draw the sketch line by line.

## 1. Prerequisites

Before you begin, you **must** have the following installed and configured:

1.  **Android Emulator:** This bot is tested and designed for **BlueStacks**.
2.  **Instagram App:** The official Instagram app must be installed *inside* the emulator.
3.  **Python 3.x:** Must be installed on your computer.
4.  **Logged In:** You must be logged into Instagram *inside the emulator*.

## 2. Installation

1.  **Clone the repository:**
    ```sh
    git clone https://github.com/JakubSdf/AutoDoodle.git
    cd AutoDoodle
    ```

2.  **Install the required libraries:**
    ```sh
    pip install -r requirements.txt
    ```

## 3. How to Use

1.  **Configure the Script:**
    * Place the image you want to draw into the `images/` folder (e.g., `images/test_image.png`).
    * Open `main.py` and set `INPUT_IMAGE_PATH = "images/test_image.png"`.

2.  **Prepare the Emulator:**
    * Open BlueStacks and the Instagram app.
    * Go to your DMs and open the conversation where you want to draw.

3.  **Run the Script:**
    * Run the script from your terminal:
        ```sh
        python main.py
        ```
    * The script will prompt you to calibrate. Click the **top-left** corner and then the **bottom-right** corner of the drawing area *inside the emulator*.

4.  **Watch and Stop:**
    * The bot will now take control and start drawing. **Do not touch your mouse!**
    * To stop the bot at any time, press and hold the **'q'** key.