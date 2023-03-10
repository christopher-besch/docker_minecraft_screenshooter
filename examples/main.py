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
    importlib.reload(pyautogui)
    pyautogui._pyautogui_x11._display = Xlib.display.Display(os.environ['DISPLAY'])
    return pyautogui


def wait(disp: SmartDisplay, pyautogui, image_to_wait_for: str, tries: int, try_duration = 1, click_when_seen: Optional[str] = None):
    def get_status(i: int):
        return f'waiting for {image_to_wait_for}: {i}'

    i = 0
    print(get_status(i), end='\r')
    while((image_center := pyautogui.locateCenterOnScreen(image_to_wait_for)) is None):
        i += 1
        if i == tries:
            raise DisplayTimeoutError('Exceeded max tries, something is fishy')
        print(get_status(i), end='\r')
        disp.waitgrab().save(f'notfound_{image_to_wait_for}')

        if click_when_seen is not None and (other_btn := pyautogui.locateCenterOnScreen(click_when_seen)) is not None:
            print(f'{get_status(i)}      : clicked {click_when_seen}', end='\r')
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


def start_minecraft(disp: SmartDisplay, pyautogui, email: str, password: str):
    print('starting minecraft')
    wait_and_click(disp, pyautogui, 'microsoft_login_btn.png', 500, click_when_seen='delete_user.png')
    wait_and_text(disp, pyautogui, 'microsoft_email_text.png', email, 60)
    wait_and_click(disp, pyautogui, 'microsoft_email_next.png', 120)
    wait_and_text(disp, pyautogui, 'microsoft_password_text.png', password, 60)
    wait_and_click(disp, pyautogui, 'microsoft_password_next.png', 120)
    wait_and_click(disp, pyautogui, 'microsoft_login_next.png', 120)
    wait_and_click(disp, pyautogui, 'play_btn.png', 120)

    wait(disp, pyautogui, 'multiplayer_btn.png', 500)


def join_server(disp: SmartDisplay, pyautogui, email: str, password: str, server_address: str):
    print('join server')
    start_minecraft(disp, pyautogui, email, password)
    
    wait_and_click(disp, pyautogui, 'multiplayer_btn.png', 60)
    wait_and_click(disp, pyautogui, 'proceed_btn.png', 60)
    wait_and_click(disp, pyautogui, 'direct_connection.png', 60)
    wait_and_text(disp, pyautogui, 'server_address_text.png', server_address, 60)
    wait_and_click(disp, pyautogui, 'join_server.png', 60)

    # TODO: wait for something


def quit_game(disp: SmartDisplay, pyautogui):
    print('quit')
    wait_and_click(disp, pyautogui, 'quit_game.png', 500)


def init(email: str, password: str):
    print('init')
    with SmartDisplay(use_xauth=True) as disp:
        pyautogui = get_pyautogui()
        with EasyProcess(['minecraft-launcher']):
            start_minecraft(disp, pyautogui, email, password)
            quit_game(disp, pyautogui)

    subprocess.run(['/bin/sed', '-i', 's/^tutorialStep:.*$/tutorialStep:none/', '/root/.minecraft/options.txt'])

    with SmartDisplay(use_xauth=True) as disp:
        pyautogui = get_pyautogui()
        with EasyProcess(['minecraft-launcher']):
            start_minecraft(disp, pyautogui, email, password)
            while(True):
                sleep(1)
                disp.waitgrab().save('something.png')


def main():
    email = os.environ['MICROSOFT_EMAIL']
    password = os.environ['MICROSOFT_PASSWORD']
    server_address = os.environ['SERVER_ADDRESS']

    while (True):
        try:
            init(email, password)
            break
        except DisplayTimeoutError as e:
            print(e)


if __name__ == '__main__':
    main()

# while(True):
#     sleep(1)
#     disp.waitgrab().save('something.png')
