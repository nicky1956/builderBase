import cv2
import numpy as np
import pyautogui
import pygetwindow as gw
import time
import pydirectinput
import os
import sys

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)
        
def wait_for_window(title, timeout=10):
    start_time = time.time()

    while time.time() - start_time < timeout:
        windows = gw.getWindowsWithTitle(title)

        if windows:
            return True

        time.sleep(1)  # Wait for 1 second before checking again

    return False
        
def getWindow(title):
    target_monitor = gw.getWindowsWithTitle(title)

    if target_monitor:
        target_monitor = target_monitor[0]

        screenshot = pyautogui.screenshot(region=(target_monitor.left, target_monitor.top,
                                                  target_monitor.width, target_monitor.height))
        screenshot_np = np.array(screenshot)

        # Return the color image directly (no need to convert to grayscale)
        threshold_image = cv2.cvtColor(screenshot_np, cv2.COLOR_RGB2BGR)

    return target_monitor, threshold_image
    
def move_mouse_to_middle_of_window():
    window_title = 'Clash of Clans'
    target_window = gw.getWindowsWithTitle(window_title)

    if target_window:
        target_window = target_window[0]
        
        window_width = target_window.width
        window_height = target_window.height
        window_height_adj = window_height*.1

        # Calculate the coordinates of the middle of the window
        middle_x = target_window.left + target_window.width // 2
        middle_y = target_window.top + target_window.height // 2
        
        bottom_middle = (target_window.left + window_width // 2, 
                         target_window.top + window_height - window_height_adj)

        # Move the mouse to the middle of the window
        pyautogui.moveTo(middle_x, middle_y)
        pyautogui.mouseDown()

        # Move the mouse to the bottom middle of the window
        pyautogui.moveTo(bottom_middle[0], bottom_middle[1])

        # Release mouse1
        time.sleep(.5)
        pyautogui.mouseUp()
        print("Mouse moved to the middle of the window.")
    else:
        print(f"Window not found: {window_title}")

def close_clash_of_clans():
    target_window_title = 'Clash of Clans'
    target_window = gw.getWindowsWithTitle(target_window_title)

    if target_window:
        target_window[0].close()
        print(f"Closed the window: {target_window_title}")
    else:
        print(f"Window not found: {target_window_title}")

def drag_to_bottom():
    # Get the Clash of Clans window
    target_monitor_title = 'Clash of Clans'
    target_monitor = gw.getWindowsWithTitle(target_monitor_title)

    if target_monitor:
        #scroll out on the attack so you can view the whole battlefield
        time.sleep(5)
        pyautogui.scroll(-10000)
        pyautogui.scroll(-10000)
        pyautogui.scroll(-10000)
        pyautogui.scroll(-10000)
        pyautogui.scroll(-10000)
        pyautogui.scroll(-10000)
        
        target_monitor = target_monitor[0]
        window_width = target_monitor.width
        window_height = target_monitor.height

        # Calculate the coordinates for the middle of the window (excluding the menu bar)
        top_middle = (target_monitor.left + window_width // 2, target_monitor.top + 100)  # Adjust 30 pixels as needed
        bottom_middle = (target_monitor.left + window_width // 2, target_monitor.top + window_height - 1)

        # Move the mouse to the top middle of the window and press mouse1
        pyautogui.moveTo(top_middle[0], top_middle[1])
        pyautogui.mouseDown()

        # Move the mouse to the bottom middle of the window
        pyautogui.moveTo(bottom_middle[0], bottom_middle[1])

        # Release mouse1
        pyautogui.mouseUp()

        print("Mouse dragged from top middle to bottom middle.")

def click_image_location(template_paths, title='Clash of Clans', bottom_right=False,
                          scale=True):
    # Get target window and color image for the Clash window
    target_monitor, threshold_image = getWindow(title)
    # cv2.imshow("Threshold Image", threshold_image)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    
    # Check if template_paths is a list; if not, cast it
    if not isinstance(template_paths, list):
        template_paths = list([template_paths])

    for template_path in template_paths:
        # Load a color template image
        template = cv2.imread(template_path)

        # Rescale the template based on the screenshot resolution
        if scale:
            width_scale = threshold_image.shape[1] / 2422
            height_scale = threshold_image.shape[0] / 1393
            
            print("Width_Scale:",width_scale,"\nHieght_Scale:",height_scale)
            template = cv2.resize(template, None, fx=width_scale, fy=height_scale,
                                  interpolation = cv2.INTER_CUBIC)

        # Use template matching to find the location of the template in the threshold image
        result = cv2.matchTemplate(threshold_image, template, cv2.TM_CCOEFF_NORMED)
        _, max_val, _, max_loc = cv2.minMaxLoc(result)

        # If the correlation is above a certain threshold, consider it a match
        correlation_threshold = 0.7  # Adjust this threshold as needed
        print(template_path, ":", max_val)
        if max_val > correlation_threshold:
            cx, cy = max_loc

            if bottom_right:
                # Click on the bottom right corner of the template match
                click_coordinates = (cx + target_monitor.left + template.shape[1],
                                      cy + target_monitor.top + template.shape[0])
            else:
                # Click on the center of the template match
                click_coordinates = (cx + target_monitor.left + template.shape[1] // 2,
                                      cy + target_monitor.top + template.shape[0] // 2)

            print(f"Found word at coordinates: {click_coordinates}")

            # Click on the location
            pyautogui.click(click_coordinates[0], click_coordinates[1])
            print(f"Clicked on the location of the word in template: {template_path}")

            return click_coordinates # Exit the function if any template is found and clicked

    print("No matching templates found.")
    return None

def main():
    #Click on play button
    time.sleep(1)
    if click_image_location([resource_path(r"assets\play.png"),
                                                resource_path(r"assets\play2.png")],
                                                title='Google Play Games beta',
                                                scale = False) == None:
        print("Cannot find play button")
        time.sleep(1)
        return
    
    #wait for COC to launch
    if not wait_for_window('Clash of Clans'):
        return
    
    #wait for COC to load once it is launched
    time.sleep(7)
    
    #scroll all the way out and then drag down so we see top half of the base
    move_mouse_to_middle_of_window()
    pyautogui.scroll(-10000)
    pyautogui.scroll(-10000)
    pyautogui.scroll(-10000)
    pyautogui.scroll(-10000)
    pyautogui.scroll(-10000)
    pyautogui.scroll(-10000)
    
    #click on the elixir cart
    if click_image_location([resource_path(r"assets\elixirElixir.png"),
                          resource_path(r"assets\elixirFight.png"),
                          resource_path(r"assets\elixirBase.png"),
                          resource_path(r"assets\elixirElixir2.png")]) == None:
        print("Cannot find elixir cart")
        close_clash_of_clans()
        return
    
    #click on the collect button
    time.sleep(.5)
    if click_image_location(resource_path(r"assets\collect.png")) == None:
        print("Cannot find elixir cart collect button")
    pydirectinput.press('esc')
    time.sleep(1.5)
    
    #use attack template to find and click
    click_image_location([resource_path(r"assets\attack.png"),
                          resource_path(r"assets\attack2.png")])
    
    #use  find now template to find and click, wait for attack click to go through
    time.sleep(1)
    click_image_location(resource_path(r"assets\findnow.png"))
    
    #scroll all the way out and then drag down so we see top half of the base
    drag_to_bottom()
    
    #deploy troops
    click_coordinates = click_image_location([resource_path(r"assets\secondDirty.png"),
                                              resource_path(r"assets\secondClean.png"),
                                              resource_path(r"assets\secondSkin.png")],
                                             bottom_right=True)
    if click_coordinates == None:
        close_clash_of_clans()
        return
    key_presses = ['q','1','2','3','4','5','6','7','8','9','0']
    for k in key_presses:
        pydirectinput.press(k)
        pyautogui.click(click_coordinates[0], click_coordinates[1])
    
    #close clash of clans
    close_clash_of_clans()
    
if __name__ == "__main__":
    try:
        while True:
            main()
    except Exception as e:
        print(e)
        input("Press enter to continue...")
