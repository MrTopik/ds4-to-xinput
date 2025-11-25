import pygame
import vgamepad as vg
import math

pygame.init()
pygame.joystick.init()

DS4_TO_XINPUT = {
    0: vg.XUSB_BUTTON.XUSB_GAMEPAD_A,      # Cross
    1: vg.XUSB_BUTTON.XUSB_GAMEPAD_B,      # Circle
    2: vg.XUSB_BUTTON.XUSB_GAMEPAD_X,      # Square
    3: vg.XUSB_BUTTON.XUSB_GAMEPAD_Y,      # Triangle
    4: vg.XUSB_BUTTON.XUSB_GAMEPAD_BACK,
    6: vg.XUSB_BUTTON.XUSB_GAMEPAD_START,
    9: vg.XUSB_BUTTON.XUSB_GAMEPAD_LEFT_SHOULDER,
    10: vg.XUSB_BUTTON.XUSB_GAMEPAD_RIGHT_SHOULDER,
    7: vg.XUSB_BUTTON.XUSB_GAMEPAD_LEFT_THUMB,
    8: vg.XUSB_BUTTON.XUSB_GAMEPAD_RIGHT_THUMB,
    12: vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_DOWN,
    13: vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_LEFT,
    14: vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_RIGHT,
    11: vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_UP
}

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
                if event.axis == 0:          # left X
                    lx = clamp(event.value, MIN_AXIS_LIMIT, MAX_AXIS_LIMIT)
                elif event.axis == 1:        # left Y
                    ly = -event.value
                    ly = clamp(ly, MIN_AXIS_LIMIT, MAX_AXIS_LIMIT)
                elif event.axis == 2:        # right X
                    rx = clamp(event.value, MIN_AXIS_LIMIT, MAX_AXIS_LIMIT)
                elif event.axis == 3:        # right Y
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
