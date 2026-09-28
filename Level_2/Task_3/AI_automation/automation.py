import os
import webbrowser
import pyautogui
from datetime import datetime


def automate(command):
    c = command.lower()

    # Websites
    if "youtube" in c:
        webbrowser.open("https://youtube.com")
        return "YouTube opened"

    elif "google" in c:
        webbrowser.open("https://google.com")
        return "Google opened"

    elif "gmail" in c:
        webbrowser.open("https://gmail.com")
        return "Gmail opened"

    # Google search
    elif "search" in c:
        query = c.replace("search", "").strip()
        webbrowser.open("https://www.google.com/search?q=" + query)
        return "Searching Google"

    # Create folder
    elif "create folder" in c:
        name = c.replace("create folder", "").strip()
        os.makedirs(name, exist_ok=True)
        return f"Folder '{name}' created"

    # Screenshot
    elif "screenshot" in c:
        name = datetime.now().strftime("screenshot_%H%M%S.png")
        pyautogui.screenshot(name)
        return f"Screenshot saved as {name}"

    # Date and time
    elif "time" in c:
        return datetime.now().strftime("Time: %I:%M %p")

    elif "date" in c:
        return datetime.now().strftime("Date: %d-%m-%Y")

    # Open applications
    elif "calculator" in c:
        os.system("calc")
        return "Calculator opened"

    elif "notepad" in c:
        os.system("notepad")
        return "Notepad opened"

    # Show files
    elif "files" in c:
        return "\n".join(os.listdir())[:1000]

    # Screen information
    elif "screen size" in c:
        w, h = pyautogui.size()
        return f"Screen: {w} x {h}"

    else:
        return "Command not supported yet"
