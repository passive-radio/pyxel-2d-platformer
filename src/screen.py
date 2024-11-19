from pigframe import Screen
import pyxel
from component import *

class ScTileMaps(Screen):
    def __init__(self, world, priority: int = 0, **kwargs) -> None:
        super().__init__(world, priority, **kwargs)
    
    def draw(self):
        for entity, tilemap in self.world.get_component(TileMap):
            pyxel.bltm(0, 0, tilemap.id, 0, 0, pyxel.width, pyxel.height, 0)

class ScPlayer(Screen):
    def __init__(self, world, priority: int = 0, **kwargs) -> None:
        super().__init__(world, priority, **kwargs)
    
    def draw(self):
        sprite_x = 0  # Base sprite x position in tileset
        sprite_y = 8*11
        for entity, (player, body, pos, vel) in self.world.get_components(Player, RectRigidBody, Position2D, Velocity2D):
            pyxel.blt(
            pos.x,
            pos.y,
            0,  # image bank
            sprite_x,  # sprite x in tileset
            sprite_y,  # sprite y in tileset
            -body.width if vel.x < 0 else body.width,  # width (negative for left flip)
            body.height,  # height
            0  # colorkey
        )