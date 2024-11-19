from pigframe import Screen
import pyxel
from component import *

class ScTileMaps(Screen):
    def __init__(self, world, priority: int = 0, **kwargs) -> None:
        super().__init__(world, priority, **kwargs)
    
    def draw(self):
        player_ent, (_, player_pos) = self.world.get_components(Player, Position2D)[0]
        camera_x = player_pos.x - pyxel.width // 2
        camera_y = 0

        for entity, tilemap in self.world.get_component(TileMap):
            pyxel.bltm(0, 0, tilemap.id, camera_x, camera_y, pyxel.width, pyxel.height, 0)

class ScPlayer(Screen):
    def __init__(self, world, priority: int = 0) -> None:
        super().__init__(world, priority)
    
    def draw(self):
        for entity, (_, position, body, animation) in self.world.get_components(Player, Position2D, RectRigidBody, Animation):
            # Draw player with animation
            pyxel.blt(
                pyxel.width//2,
                position.y,
                0,  # image bank
                animation.sprite_x,  # sprite x in tileset
                animation.sprite_y,  # sprite y in tileset
                -body.width if body.flip_x else body.width,  # width (negative for left flip)
                body.height,  # height
                0  # colorkey
            )