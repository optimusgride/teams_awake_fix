import pyautogui
import time
import random
import keyboard
import ctypes

# Screen center calculations and small movement range (1% of screen width)
screen_width, screen_height = pyautogui.size()
center_x, center_y = screen_width // 2, screen_height // 2  # Center of screen
movement_range = int(screen_width * 0.01)  # 1% of screen width

# Set left and right bounds around the center for 1% movement range
left_edge = center_x - movement_range // 2
right_edge = center_x + movement_range // 2

# Flag to control the movement loop
running = False

# Use ctypes to set system to stay awake
ctypes.windll.kernel32.SetThreadExecutionState(0x80000002)

def toggle_movement():
    global running
    running = not running  # Toggle the running state

    if running:
        print("Mouse and keyboard activity started.")
        horizontal_mouse_movement()
    else:
        print("Mouse and keyboard activity stopped.")
        # Revert to default power settings
        ctypes.windll.kernel32.SetThreadExecutionState(0x80000000)

def horizontal_mouse_movement():
    global running
    # Start position at the center of the screen
    pyautogui.moveTo(center_x, center_y)
    moving_right = True

    while running:
        # Check if Esc is pressed to stop the loop
        if keyboard.is_pressed('esc'):
            running = False
            print("Stopping mouse and keyboard activity...")
            ctypes.windll.kernel32.SetThreadExecutionState(0x80000000)  # Revert settings on stop
            break

        # Move a small amount around the center
        if moving_right:
            for x in range(center_x, right_edge, 1):  # Small movement in increments of 1 pixel
                if not running or keyboard.is_pressed('esc'):
                    running = False
                    print("Stopping mouse and keyboard activity...")
                    ctypes.windll.kernel32.SetThreadExecutionState(0x80000000)  # Revert settings on stop
                    return
                pyautogui.moveTo(x, center_y)
                time.sleep(0.01)
        else:
            for x in range(center_x, left_edge, -1):  # Small movement in increments of 1 pixel
                if not running or keyboard.is_pressed('esc'):
                    running = False
                    print("Stopping mouse and keyboard activity...")
                    ctypes.windll.kernel32.SetThreadExecutionState(0x80000000)  # Revert settings on stop
                    return
                pyautogui.moveTo(x, center_y)
                time.sleep(0.01)

        # Toggle direction
        moving_right = not moving_right

        # Simulate additional activity every 30 seconds
        if time.time() % 30 < 0.1:
            pyautogui.press('shift')

# Hotkey to start/stop the movement
keyboard.add_hotkey('ctrl+alt+1', toggle_movement)

# Keep the script running to listen for the hotkey
print("Press Ctrl+Alt+1 to toggle mouse and keyboard activity. Press Esc to exit.")
keyboard.wait('esc')  # Press Esc to exit

# Revert settings in case of exit without toggling off
ctypes.windll.kernel32.SetThreadExecutionState(0x80000000)
