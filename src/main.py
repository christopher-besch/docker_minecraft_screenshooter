import os
import subprocess
from typing import Optional
from easyprocess import EasyProcess
from time import sleep
from pyvirtualdisplay.smartdisplay import SmartDisplay, DisplayTimeoutError
import importlib
import Xlib.display


def get_pyautogui():
    import pyautogui
    pyautogui._pyautogui_x11._display = Xlib.display.Display(os.environ['DISPLAY'])
    return pyautogui


def wait(disp: SmartDisplay, pyautogui, image_to_wait_for: str, tries: int, try_duration = 1, click_when_seen: Optional[str] = None, done_when_not_seen=False):
    wait_img = f'ref_imgs/{image_to_wait_for}'
    notfound_img = f'notfound/{image_to_wait_for}'
    click_img = f'ref_imgs/{click_when_seen}' if click_when_seen is not None else None
    def get_status(i: int):
        return f'waiting for{" to go away" if done_when_not_seen else ""} {image_to_wait_for}: {i}/{tries}'

    i = 0
    print(get_status(i), end='\r')
    while(((image_center := pyautogui.locateCenterOnScreen(wait_img)) is not None) == done_when_not_seen):
        i += 1
        if i == tries:
            raise DisplayTimeoutError('Exceeded max tries, something is fishy')
        print(get_status(i), end='\r')
        disp.waitgrab().save(notfound_img)

        if click_img is not None and (other_btn := pyautogui.locateCenterOnScreen(click_img)) is not None:
            print(f'{get_status(i)}        : clicked {click_img}', end='\r')
            pyautogui.click(*other_btn)
        sleep(try_duration)
    print()
    return image_center


def wait_and_click(disp: SmartDisplay, pyautogui, button_image: str, tries: int, try_duration = 1, click_when_seen: Optional[str] = None):
    btn_center = wait(disp, pyautogui, button_image, tries, try_duration, click_when_seen)
    print('click')
    pyautogui.click(*btn_center)


def wait_and_text(disp: SmartDisplay, pyautogui, text_box_image: str, text: str, tries, try_duration = 1, click_when_seen: Optional[str] = None):
    wait_and_click(disp, pyautogui, text_box_image, tries, try_duration, click_when_seen)
    sleep(try_duration)
    print('write text')
    pyautogui.write(text)


def start_minecraft(disp: SmartDisplay, pyautogui, email: str, password: str, initial_start: bool):
    print('starting minecraft')
    wait_and_click(disp, pyautogui, 'microsoft_login_btn.png', 500, click_when_seen='delete_user.png')
    disp.waitgrab().save('notfound/1.png')
    wait_and_text(disp, pyautogui, 'microsoft_email_text.png', email, 120)
    disp.waitgrab().save('notfound/2.png')
    wait_and_click(disp, pyautogui, 'microsoft_email_next.png', 60)
    disp.waitgrab().save('notfound/3.png')
    wait_and_text(disp, pyautogui, 'microsoft_password_text.png', password, 120)
    disp.waitgrab().save('notfound/4.png')
    wait_and_click(disp, pyautogui, 'microsoft_password_next.png', 60)
    disp.waitgrab().save('notfound/5.png')
    wait_and_click(disp, pyautogui, 'microsoft_login_next.png', 120)
    disp.waitgrab().save('notfound/6.png')
    wait_and_click(disp, pyautogui, 'play_btn.png', 120)
    disp.waitgrab().save('notfound/7.png')

    if initial_start:
        wait(disp, pyautogui, 'low_res_multiplayer_btn.png', 1000)
    else:
        wait(disp, pyautogui, 'multiplayer_btn.png', 500)


def join_server(disp: SmartDisplay, pyautogui, email: str, password: str, server_address: str):
    print('join server')
    start_minecraft(disp, pyautogui, email, password, False)
    
    wait_and_click(disp, pyautogui, 'multiplayer_btn.png', 60)
    wait_and_click(disp, pyautogui, 'proceed_btn.png', 60)
    wait_and_click(disp, pyautogui, 'direct_connection.png', 60)
    wait_and_text(disp, pyautogui, 'server_address_text.png', server_address, 60)
    wait_and_click(disp, pyautogui, 'join_server.png', 60)

    wait(disp, pyautogui, 'menu_background.png', 120, done_when_not_seen=True)
    pyautogui.press('F1')


def quit_game(disp: SmartDisplay, pyautogui, proc: EasyProcess):
    print('quit')
    wait_and_click(disp, pyautogui, 'low_res_quit_game.png', 500)
    while(proc.is_alive()):
        sleep(1)


def init(email: str, password: str):
    options_path = '/root/.minecraft/options.txt'
    print('init')
    # always behave the same
    if os.path.exists(options_path):
        os.remove(options_path)
    with SmartDisplay(use_xauth=True, size=(1920, 1080)) as disp:
        pyautogui = get_pyautogui()
        with EasyProcess(['minecraft-launcher']) as proc:
            start_minecraft(disp, pyautogui, email, password, True)
            wait_and_click(disp, pyautogui, 'low_res_options.png', 60)
            wait_and_click(disp, pyautogui, 'low_res_minecraft_done.png', 60)
            quit_game(disp, pyautogui, proc)

    def set_cfg(key: str, value: str):
        subprocess.run(['/bin/sed', '-i', f's/^{key}:.*$/{key}:{value}/', options_path]).check_returncode()
    print("setting config.txt")
    set_cfg('tutorialStep', 'none')
    set_cfg('maxFps', '10')
    set_cfg('fullscreen', 'true')


def run(email: str, password: str, server_address: str):
    init(email, password)

    with SmartDisplay(use_xauth=True, size=(1920, 1080)) as disp:
        pyautogui = get_pyautogui()
        with EasyProcess(['minecraft-launcher']):
            join_server(disp, pyautogui, email, password, server_address)
            print('taking screenshot')
            while(True):
                sleep(1)
                disp.waitgrab().save('notfound/something.png')


def main():
    print("docker_minecraft_screenshooter booting up")
    email = os.environ['MICROSOFT_EMAIL']
    password = os.environ['MICROSOFT_PASSWORD']
    server_address = os.environ['SERVER_ADDRESS']

    while (True):
        for _ in range(0, 5):
            try:
                run(email, password, server_address)
                return
            except DisplayTimeoutError as e:
                print(e)
        print('removing minecraft dir')
        if os.path.exists('/root/.minecraft'):
            os.removedirs('/root/.minecraft')


if __name__ == '__main__':
    main()
