from pigframe import ActionMap
import pyxel

from dataclasses import dataclass

@dataclass
class Input(ActionMap):
    """入力を管理するオブジェクト"""
    jump: tuple = pyxel.btnp, pyxel.KEY_SPACE
    left: tuple = pyxel.btn, pyxel.KEY_LEFT, pyxel.KEY_A
    right: tuple = pyxel.btn, pyxel.KEY_RIGHT, pyxel.KEY_D
    # up: tuple = pyxel.btn, pyxel.KEY_UP, pyxel.KEY_W
    # down: tuple = pyxel.btn, pyxel.KEY_DOWN, pyxel.KEY_S
    crouch: tuple = pyxel.btn, pyxel.KEY_DOWN, pyxel.KEY_S
    menu: tuple = pyxel.btnp, pyxel.KEY_ESCAPE