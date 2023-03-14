import os
from typing import Any, Optional, Tuple
from time import sleep
from pyvirtualdisplay.smartdisplay import DisplayTimeoutError
import Xlib.display

from state import State


def get_pyautogui() -> Any:
    import pyautogui
    pyautogui._pyautogui_x11._display = Xlib.display.Display(os.environ['DISPLAY'])
    return pyautogui


def connection_lost(state) -> bool:
    img = 'ref_imgs/back_to_server_list.png'
    return state.pyautogui.locateCenterOnScreen(img) is not None


def wait(state: State, image_to_wait_for: str, tries: int, try_duration = 1, click_when_seen: Optional[str] = None, done_when_not_seen=False) -> Tuple[float, float]:
    wait_img = f'ref_imgs/{image_to_wait_for}'
    notfound_img = f'notfound/{image_to_wait_for}'
    click_img = f'ref_imgs/{click_when_seen}' if click_when_seen is not None else None
    print(f'waiting for {image_to_wait_for}{" to go away" if done_when_not_seen else ""}')

    i = 0
    print(f'{i}/{tries}')
    while(((image_center := state.pyautogui.locateCenterOnScreen(wait_img)) is not None) == done_when_not_seen):
        i += 1
        if i == tries:
            raise DisplayTimeoutError('Exceeded max tries, something is fishy')
        print(f'{i}/{tries}')
        state.disp.waitgrab().save(notfound_img)

        if click_img is not None and (other_btn := state.pyautogui.locateCenterOnScreen(click_img)) is not None:
            print(f'clicked {click_img}')
            state.pyautogui.click(*other_btn)
        sleep(try_duration)
    return image_center


def wait_and_click(state: State, button_image: str, tries: int, try_duration = 1, click_when_seen: Optional[str] = None) -> None:
    btn_center = wait(state, button_image, tries, try_duration, click_when_seen)
    print('click')
    state.pyautogui.click(*btn_center)


def wait_and_text(state, text_box_image: str, text: str, tries, try_duration = 1, click_when_seen: Optional[str] = None) -> None:
    wait_and_click(state, text_box_image, tries, try_duration, click_when_seen)
    sleep(try_duration)
    print('write text')
    state.pyautogui.write(text)

