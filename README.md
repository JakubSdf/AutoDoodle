# AutoDoodle - Instagram DM Drawing Bot

AutoDoodle is a Python bot that automatically draws any image as a sketch directly inside **Instagram DMs**.

It is designed to run on a PC using an **Android emulator** (e.g., BlueStacks) with the Instagram app running. It processes a source image and then takes control of your mouse to draw the sketch line by line.

## 1. What You Need Before You Start

Before you type the first command, you **must** have these 4 things installed and set up on your computer:

1.  **Python (and Pip)**
    * **What it is:** The programming language that runs the bot. `pip` is a tool included with Python that installs the bot's "add-ons".
    * **Where to get it:** [https://www.python.org/downloads/](https://www.python.org/downloads/)
    * *(During installation, make sure to check the box that says "Add Python to PATH")*

2.  **Git**
    * **What it is:** A tool that lets you "clone" (copy) the bot's code from the internet to your computer.
    * **Where to get it:** [https://git-scm.com/downloads](https://git-scm.com/downloads)

3.  **Android Emulator (BlueStacks Recommended)**
    * **What it is:** A program that simulates an Android phone on your PC. This bot is tested and designed for **BlueStacks**.
    * **Where to get it:** [https://www.bluestacks.com/](https://www.bluestacks.com/)

4.  **Instagram App**
    * **What it is:** The normal Instagram app, which must be installed *inside* your emulator (inside BlueStacks).
    * **How to set up:** Open BlueStacks, launch the Instagram app, and **log in to your account**.

## 2. Installation (In 2 Steps)

Once you have everything from Section 1 ready, open your terminal (like "Command Prompt" or "PowerShell" in Windows) and follow these steps:

1.  **Clone the repository:**
    This command downloads the bot's code to your computer.
    ```sh
    git clone https://github.com/JakubSdf/AutoDoodle.git
    ```

2.  **Move into the folder and install libraries:**
    First, you need to move into the new folder you just downloaded:
    ```sh
    cd AutoDoodle
    ```
    Then, run this command to install the required "add-ons" (libraries):
    ```sh
    pip install -r requirements.txt
    ```

## 3. How to Use

1.  **Configure the Script:**
    * Place the image you want to draw into the `images/` folder (e.g., `images/my_cat.png`).
    * Open the `main.py` file (in any text editor, like Notepad) and change the `INPUT_IMAGE_PATH` at the top to match your file's name:
        `INPUT_IMAGE_PATH = "images/my_cat.png"`

2.  **Prepare the Emulator:**
    * Open BlueStacks and the Instagram app.
    * Go to your DMs and open the conversation where you want to draw.

3.  **Run the Script:**
    * Go back to your terminal (Command Prompt) and run this command:
        ```sh
        python main.py
        ```
    * The script will prompt you to calibrate. Click the **top-left** corner and then the **bottom-right** corner of the drawing area *inside the emulator*.

## 4. Watch and Stop

* After calibration, the bot will take control and start drawing. **Do not touch your mouse!**
* To stop the bot at any time, press and hold the **'q'** key.

## 5. Common Errors

* **Error: Bot can't find the 'plus' button and stops.**
    * **Cause:** This happens when the bot can't see the `plus_icon.png` image on your screen. The most common reasons are:
        1.  Your emulator window is too small.
        2.  Your Instagram DMs are using a colorful "Theme" (like a gradient background), which makes the white plus icon hard to find.
    * **Solution:**
        1.  Make sure the emulator window is large and that the Instagram DM chat is set to the default (black or white) theme.
        2.  If it still fails, take your own screenshot of *just* the plus button from your emulator.
        3.  Save your new screenshot as `plus_icon.png` and use it to **replace** the original `plus_icon.png` file in the bot's folder.