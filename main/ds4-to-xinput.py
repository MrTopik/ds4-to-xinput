import pygame
import vgamepad as vg
import math
import json
import os

MAPPING_FILE = 'ds4_mapping.json'

DEFAULT_MAPPING = {
    "0": "XUSB_GAMEPAD_A",            # Cross
    "1": "XUSB_GAMEPAD_B",            # Circle
    "2": "XUSB_GAMEPAD_X",            # Square
    "3": "XUSB_GAMEPAD_Y",            # Triangle
    "4": "XUSB_GAMEPAD_BACK",         # Share
    "6": "XUSB_GAMEPAD_START",        # Options
    "9": "XUSB_GAMEPAD_LEFT_SHOULDER",# L1
    "10": "XUSB_GAMEPAD_RIGHT_SHOULDER",# R1
    "7": "XUSB_GAMEPAD_LEFT_THUMB",   # L3
    "8": "XUSB_GAMEPAD_RIGHT_THUMB",  # R3
    "12": "XUSB_GAMEPAD_DPAD_DOWN",   # D-Pad Down
    "13": "XUSB_GAMEPAD_DPAD_LEFT",   # D-Pad Left
    "14": "XUSB_GAMEPAD_DPAD_RIGHT",  # D-Pad Right
    "11": "XUSB_GAMEPAD_DPAD_UP"      # D-Pad Up
}

def load_mapping():
    if os.path.exists(MAPPING_FILE):
        try:
            print(f"Loading mapping from {MAPPING_FILE}...")
            with open(MAPPING_FILE, 'r') as f:
                raw_mapping = json.load(f)
        except (IOError, json.JSONDecodeError) as e:
            print(f"Error loading/decoding {MAPPING_FILE} ({e}). Creating default file.")
            raw_mapping = DEFAULT_MAPPING
            write_mapping(raw_mapping)
    else:
        print(f"Mapping file {MAPPING_FILE} not found. Creating default file.")
        raw_mapping = DEFAULT_MAPPING
        write_mapping(raw_mapping)
        
    try:
        DS4_TO_XINPUT = {
            int(k): getattr(vg.XUSB_BUTTON, v) 
            for k, v in raw_mapping.items() 
            if hasattr(vg.XUSB_BUTTON, v) 
        }
        if len(DS4_TO_XINPUT) < len(DEFAULT_MAPPING):
            print("Warning: Some mapping entries were invalid or missing in the file.")
            
        return DS4_TO_XINPUT
        
    except ValueError as e:
        print(f"Error: Non-integer key found in mapping file. Please check {MAPPING_FILE}.")
        return {int(k): getattr(vg.XUSB_BUTTON, v) for k, v in DEFAULT_MAPPING.items()}
        

def write_mapping(mapping_data):
    with open(MAPPING_FILE, 'w') as f:
        json.dump(mapping_data, f, indent=4)

pygame.init()
pygame.joystick.init()

DS4_TO_XINPUT = load_mapping()

lx = ly = rx = ry = 0.0
MIN_AXIS_LIMIT = -1.0
MAX_AXIS_LIMIT = 1.0

def clamp(value, min_val, max_val):
    return max(min_val, min(value, max_val))

if pygame.joystick.get_count() > 0:
    joystick = pygame.joystick.Joystick(0)
    joystick.init()

    gamepad = vg.VX360Gamepad()
    print(f"\nController connected: {joystick.get_name()}")
    if joystick.get_name() != "PS4 Controller":
        print("This program is designed to work with a PS4 Controller, \nuse another controller after you change the mapping.")

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            #Button translation
            elif event.type == pygame.JOYBUTTONDOWN:
                if event.button in DS4_TO_XINPUT:
                    gamepad.press_button(button=DS4_TO_XINPUT[event.button])
            elif event.type == pygame.JOYBUTTONUP:
                if event.button in DS4_TO_XINPUT:
                    gamepad.release_button(button=DS4_TO_XINPUT[event.button])

            #AXIS translation
            elif event.type == pygame.JOYAXISMOTION:
                if event.axis == 0:          # left X - Left joystick horizontal
                    lx = clamp(event.value, MIN_AXIS_LIMIT, MAX_AXIS_LIMIT)
                elif event.axis == 1:        # left Y - Left joystick vertical
                    ly = -event.value
                    ly = clamp(ly, MIN_AXIS_LIMIT, MAX_AXIS_LIMIT)
                elif event.axis == 2:        # right X - Right joystick horizontal
                    rx = clamp(event.value, MIN_AXIS_LIMIT, MAX_AXIS_LIMIT)
                elif event.axis == 3:        # right Y - Right joystick vertical
                    ry = -event.value
                    ry = clamp(ry, MIN_AXIS_LIMIT, MAX_AXIS_LIMIT)
                elif event.axis == 5:  # R2
                    gamepad.right_trigger(int((event.value + 1) * 127.5))
                elif event.axis == 4:  # L2
                    gamepad.left_trigger(int((event.value + 1) * 127.5))
                gamepad.left_joystick_float(lx, ly)
                gamepad.right_joystick_float(rx, ry)

            elif pygame.joystick.get_count() <= 1:
                print("Controller Disconnected")
                pygame.quit()
            
            gamepad.update()

    pygame.joystick.quit()
    pygame.quit()
else:
    input("\nNo gamepad found. Press Enter to close...")

