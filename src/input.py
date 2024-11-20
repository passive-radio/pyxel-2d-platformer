from pigframe import ActionMap
import pyxel

from dataclasses import dataclass

@dataclass
class Input(ActionMap):
    """入力を管理するオブジェクト"""
    jump: tuple = pyxel.btnp, pyxel.KEY_SPACE, pyxel.GAMEPAD1_BUTTON_A, pyxel.GAMEPAD2_BUTTON_A, pyxel.GAMEPAD3_BUTTON_A, pyxel.GAMEPAD4_BUTTON_A
    left: tuple = pyxel.btn, pyxel.KEY_LEFT, pyxel.KEY_A, pyxel.GAMEPAD1_BUTTON_DPAD_LEFT, pyxel.GAMEPAD2_BUTTON_DPAD_LEFT, pyxel.GAMEPAD3_BUTTON_DPAD_LEFT, pyxel.GAMEPAD4_BUTTON_DPAD_LEFT
    right: tuple = pyxel.btn, pyxel.KEY_RIGHT, pyxel.KEY_D, pyxel.GAMEPAD1_BUTTON_DPAD_RIGHT, pyxel.GAMEPAD2_BUTTON_DPAD_RIGHT, pyxel.GAMEPAD3_BUTTON_DPAD_RIGHT, pyxel.GAMEPAD4_BUTTON_DPAD_RIGHT
    # up: tuple = pyxel.btn, pyxel.KEY_UP, pyxel.KEY_W
    # down: tuple = pyxel.btn, pyxel.KEY_DOWN, pyxel.KEY_S
    crouch: tuple = pyxel.btn, pyxel.KEY_DOWN, pyxel.KEY_S, pyxel.GAMEPAD1_BUTTON_DPAD_DOWN, pyxel.GAMEPAD2_BUTTON_DPAD_DOWN, pyxel.GAMEPAD3_BUTTON_DPAD_DOWN, pyxel.GAMEPAD4_BUTTON_DPAD_DOWN
    menu: tuple = pyxel.btnp, pyxel.KEY_ESCAPE, pyxel.GAMEPAD1_BUTTON_START, pyxel.GAMEPAD2_BUTTON_START, pyxel.GAMEPAD3_BUTTON_START, pyxel.GAMEPAD4_BUTTON_START
    restart: tuple = pyxel.btnp, pyxel.KEY_RETURN, pyxel.GAMEPAD1_BUTTON_B, pyxel.GAMEPAD2_BUTTON_B