import os
from typing import List
from easyprocess import EasyProcess
from time import sleep, time
from pyvirtualdisplay.smartdisplay import SmartDisplay, DisplayTimeoutError

from gui_interaction import connection_lost, get_pyautogui
from mincraft_interaction import join_server, tp, init
from state import State, ScreenshotPos
from load_instructions import load_instructions


def take_screenshots(state: State, instructions: List[ScreenshotPos]) -> None:
    for pos in instructions:
        dir = f'/mc_scr/captures/{pos.name}'
        os.makedirs(dir, exist_ok=True)

        idx = len(os.listdir(dir))
        file = f'{dir}/{idx:04d}.png'
        tp(state, pos)
        sleep(0.5)
        print(f'capturing {file}')
        state.disp.waitgrab().save(file)


def run(state: State, instructions: List[ScreenshotPos]) -> None:
    if len(instructions) == 0:
        return
    with SmartDisplay(use_xauth=True, size=(1920, 1080)) as disp:
        state.disp = disp
        state.pyautogui = get_pyautogui()
        with EasyProcess(['minecraft-launcher']) as proc:
            state.proc = proc
            join_server(state)
            sleep(2)
            state.pyautogui.press('F1')
            while(len(instructions) != 0):
                if connection_lost(state):
                    print('connection lost')
                    break
                start = time()
                take_screenshots(state, instructions)
                end = time()
                sleep_dur = state.frame_time - (end - start)
                if sleep_dur > 0:
                    sleep(sleep_dur)


def main() -> None:
    print("docker_minecraft_screenshooter booting up")
    state = State()

    for _ in range(0, 100):
        for _ in range(0, 5):
            try:
                while(True):
                    instructions = load_instructions(state)
                    init(state)
                    run(state, instructions)
            except DisplayTimeoutError as e:
                print(e)
        print('removing minecraft dir')
        if os.path.exists('/root/.minecraft'):
            os.removedirs('/root/.minecraft')


if __name__ == '__main__':
    main()

