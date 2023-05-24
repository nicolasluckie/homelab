import pyautogui
import time
import keyboard
import random
import win32api, win32con


def click(x, y):
    """
    Moves the mouse to a location given an x and y position.
    :param x: x position
    :param y: y position
    :return:
    """
    win32api.SetCursorPos((x, y))
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0)
    time.sleep(0.01)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)


if __name__ == '__main__':
    print("> Hold \"Q\" to terminate the script.")

    """
    Main loop
    """
    while not keyboard.is_pressed('q'):

        image = pyautogui.locateCenterOnScreen('image.png', grayscale=False, confidence=0.8)
        if image is not None:
            click(image.x, image.y)
            print(f"Click ({image.x}, {image.y})")

    print("> Script terminated.")
    exit(0)
