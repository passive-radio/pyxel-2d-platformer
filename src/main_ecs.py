from pigframe import World
from screen import *
from system import *
from spawn import *
from input import Input

SCREEN_SIZE = (8*34, 8*2*10) # (288, 160)
image_filepath = "assets/2d-platformer.png"
tilemap_filepath = "assets/map01.tmx"
title = "2d-platformer"
FPS = 60

class Game(World):
    def __init__(self):
        super().__init__()
        self.screen_size = SCREEN_SIZE
        self.init()
        
    def init(self):
        pyxel.init(self.screen_size[0], self.screen_size[1], title=title, fps=FPS)
        pyxel.images[0] = pyxel.Image.from_image(image_filepath, incl_colors=True)
        for i in range(0,4,1):
            pyxel.tilemaps[i] = pyxel.Tilemap.from_tmx(tilemap_filepath, i)
        
    def draw(self):
        self.process_screens()
        
    def process(self):
        self.scene_manager.process()
        self.process_user_actions()
        self.process_systems()
        self.process_events()
    
    def run(self):
        pyxel.run(self.process, self.draw)

if __name__ == "__main__":
    game = Game()
    game.add_scenes(["playable"])
    game.set_user_actions_map(Input())
    game.current_scene = "playable"
    
    # Spawn entities
    spawn_player(game, 8*10, 8*10, 16, 16, jump_power=2, move_speed=1.5)
    spawn_background(game, 0)
    spawn_background(game, 1)
    spawn_floor(game, 2, 2)
    spawn_background(game, 3)
    
    # Add systems
    game.add_system_to_scenes(SysFloorCollision, "playable", 0)
    game.add_system_to_scenes(SysSimulateGravity, "playable", 1)
    game.add_system_to_scenes(SysPlayerMovement, "playable", 2)
    game.add_system_to_scenes(SysPlayerControl, "playable", 3)
    game.add_system_to_scenes(SysUpdatePosition, "playable", 4)
    
    # Add screens
    game.add_screen_to_scenes(ScTileMaps, "playable", 0)
    game.add_screen_to_scenes(ScPlayer, "playable", 100)
    
    game.run()