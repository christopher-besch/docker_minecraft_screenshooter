import os
from easyprocess import EasyProcess
from pyvirtualdisplay.smartdisplay import SmartDisplay
from typing import Any


class State:
    disp: SmartDisplay
    pyautogui: Any
    proc: EasyProcess
    def __init__(self):
        self.email = os.environ['MICROSOFT_EMAIL']
        self.password = os.environ['MICROSOFT_PASSWORD']
        self.server_address = os.environ['SERVER_ADDRESS']
        self.wet_init = os.environ['WET_INIT'].lower() == "true"
        self.frame_time = float(os.environ['FRAME_TIME'])
        self.instructions_path = os.environ['INSTRUCTIONS_PATH']

class ScreenshotPos:
    def __init__(self, x: float, y: float, z: float, x_rot: float, y_rot: float, name: str):
        self.x = x
        self.y = y
        self.z = z
        self.x_rot = x_rot
        self.y_rot = y_rot
        self.name = name

