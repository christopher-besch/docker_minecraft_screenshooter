from typing import List

from state import State, ScreenshotPos


def load_instructions(state: State) -> List[ScreenshotPos]:
    return [ScreenshotPos(0, 0, 0, 0, 0, "this_is_a_test")]

