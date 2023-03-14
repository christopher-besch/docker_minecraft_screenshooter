from time import sleep
from typing import List, Optional
import yaml

from state import State, ScreenshotPos


def load_instructions(state: State) -> Optional[List[ScreenshotPos]]:
    try:
        with open(state.instructions_path, "r") as file:
            yaml_load = yaml.safe_load(file.read())

        instructions: List[ScreenshotPos] = []
        for name, pos in yaml_load['instructions'].items():
            instructions.append(ScreenshotPos(
                float(pos['x']),
                float(pos['y']),
                float(pos['z']),
                float(pos['x_rot']),
                float(pos['y_rot']),
                name,
            ))
    except:
        print('failed to parse instructions.yaml')
        return None
    return instructions


def ensure_load_instructions(state: State) -> List[ScreenshotPos]:
    while(True):
        instructions = load_instructions(state)
        if instructions is not None:
            return instructions
        sleep(10)

