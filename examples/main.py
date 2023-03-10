import os
from typing import Optional
from easyprocess import EasyProcess
from time import sleep
from pyvirtualdisplay.smartdisplay import SmartDisplay


def wait_and_click(disp: SmartDisplay, pyautogui, button_image: str, tries: int, try_duration = 1, click_when_seen: Optional[str] = None):
    print(f'clicking {button_image}', end='\r')
    i = 0
    while((microsoft_login_btn := pyautogui.locateCenterOnScreen(button_image)) is None):
        print(f'clicking {button_image}: {i}', end='\r')
        disp.waitgrab().save(f'notfound_{button_image}')

        i += 1
        if i == tries:
            raise AssertionError('Exceeded max tries, something is fishy')

        if click_when_seen is not None and (other_btn := pyautogui.locateCenterOnScreen(click_when_seen)) is not None:
            print(f'clicked {click_when_seen}')
            pyautogui.click(*other_btn)
        sleep(try_duration)
    print()
    pyautogui.click(*microsoft_login_btn)


def wait_and_text(disp: SmartDisplay, pyautogui, text_box_image: str, text: str, tries, try_duration = 1, click_when_seen: Optional[str] = None):
    wait_and_click(disp, pyautogui, text_box_image, tries, try_duration, click_when_seen)
    sleep(try_duration)
    pyautogui.write(text)


def microsoft_login(disp: SmartDisplay, pyautogui, email: str, password: str, server_address: str):
    wait_and_click(disp, pyautogui, 'microsoft_login_btn.png', 500, click_when_seen='delete_user.png')
    wait_and_text(disp, pyautogui, 'microsoft_email_text.png', email, 60)
    wait_and_click(disp, pyautogui, 'microsoft_email_next.png', 120)
    wait_and_text(disp, pyautogui, 'microsoft_password_text.png', password, 60)
    wait_and_click(disp, pyautogui, 'microsoft_password_next.png', 120)
    wait_and_click(disp, pyautogui, 'microsoft_login_next.png', 120)
    wait_and_click(disp, pyautogui, 'play_btn.png', 120)
    wait_and_click(disp, pyautogui, 'multiplayer_btn.png', 500)
    wait_and_click(disp, pyautogui, 'proceed_btn.png', 60)
    wait_and_click(disp, pyautogui, 'direct_connection.png', 60)
    wait_and_text(disp, pyautogui, 'server_address_text.png', server_address, 60)


def main():
    with SmartDisplay(use_xauth=True, size=(1920, 1080)) as disp:
        import pyautogui
        with EasyProcess(['minecraft-launcher']):
            microsoft_login(disp, pyautogui,
                            os.environ['MICROSOFT_EMAIL'],
                            os.environ['MICROSOFT_PASSWORD'],
                            os.environ['SERVER_ADDRESS'])
            while(True):
                sleep(1)
                disp.waitgrab().save('something.png')


if __name__ == '__main__':
    main()

