import os
import subprocess
from easyprocess import EasyProcess
from time import sleep
from pyvirtualdisplay.smartdisplay import SmartDisplay

from gui_interaction import get_pyautogui, wait, wait_and_click, wait_and_text
from state import ScreenshotPos, State


def start_minecraft(state: State) -> None:
    print('starting minecraft')
    wait_and_click(state, 'microsoft_login_btn.png', 500, click_when_seen='delete_user.png')
    wait_and_text(state, 'microsoft_email_text.png', state.email, 120)
    wait_and_click(state, 'microsoft_email_next.png', 60)
    wait_and_text(state, 'microsoft_password_text.png', state.password, 120)
    wait_and_click(state, 'microsoft_password_next.png', 60)
    wait_and_click(state, 'microsoft_login_next.png', 120)
    wait_and_click(state, 'play_btn.png', 120)

    if state.wet_init:
        wait(state, 'multiplayer_btn.png', 500)
    else:
        wait(state, 'low_res_multiplayer_btn.png', 1000, click_when_seen='low_res_continue.png')


def join_server(state: State) -> None:
    print('join server')
    start_minecraft(state)
    
    wait_and_click(state, 'multiplayer_btn.png', 60)
    wait_and_click(state, 'proceed_btn.png', 60)
    wait_and_click(state, 'direct_connection.png', 60)
    wait_and_text(state, 'server_address_text.png', state.server_address, 60)
    wait_and_click(state, 'join_server.png', 60)

    wait(state, 'menu_background.png', 120, done_when_not_seen=True)
    sleep(10)


def quit_game_low_res(state: State) -> None:
    print('quit')
    wait_and_click(state, 'low_res_quit_game.png', 500)
    while(state.proc.is_alive()):
        sleep(1)


def set_cfg(key: str, value: str) -> None:
    options_path = '/root/.minecraft/options.txt'
    subprocess.run(['/bin/sed', '-i', f's/^{key}:.*$/{key}:{value}/', options_path]).check_returncode()


def init(state: State) -> None:
    if state.wet_init:
        print('wet init')
        set_cfg('lastServer', '')
    else:
        print('dry init')
        options_path = '/root/.minecraft/options.txt'
        # always behave the same
        if os.path.exists(options_path):
            os.remove(options_path)
        with SmartDisplay(use_xauth=True, size=(1920, 1080)) as disp:
            state.disp = disp
            state.pyautogui = get_pyautogui()
            with EasyProcess(['minecraft-launcher']) as proc:
                state.proc = proc
                start_minecraft(state)
                wait_and_click(state, 'low_res_options.png', 60)
                wait_and_click(state, 'low_res_minecraft_done.png', 60)
                quit_game_low_res(state)

        print("setting config.txt")
        set_cfg('tutorialStep', 'none')
        set_cfg('maxFps', '10')
        set_cfg('fullscreen', 'true')
        set_cfg('renderDistance', '32')
    state.wet_init = True


def msg(state, msg: str) -> None:
    state.pyautogui.press('T')
    sleep(0.5)
    print(msg)
    state.pyautogui.write(msg)
    sleep(0.5)
    state.pyautogui.press('enter')


def tp(state: State, pos: ScreenshotPos) -> None:
    msg(state, f'/tp @p {pos.x} {pos.y} {pos.z} {pos.y_rot} {pos.x_rot}')

