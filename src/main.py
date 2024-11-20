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

COINS_POSITIONS = [
    (8*1, 8*5),
    (8*36, 8*10),
]

def get_coin_positions_from_tilemap(tilemap_id: int = 7) -> list[tuple[int, int]]:
    """Convert coin tilemap to list of coin positions.
    
    Args:
        tilemap_id (int): Tilemap ID for coins (default: 7)
    
    Returns:
        list[tuple[int, int]]: List of coin positions in pixel coordinates [(x, y), ...]
    """
    coin_positions = []
    coins_pixels_width = 2
    coins_pixels_height = 2
    
    # Get tilemap dimensions
    tilemap = pyxel.tilemaps[tilemap_id]
    # width, height = tilemap.width, tilemap.height
    height = 20
    width = 120
    
    # Scan each tile
    for y in range(0, height, coins_pixels_height):
        for x in range(0, width, coins_pixels_width):
            col, colkey = tilemap.pget(x, y)
            print(col, colkey)
            if col != 0:  # Non-zero means coin placement
                # Convert tile coordinates to pixel coordinates
                pixel_x = x * 8
                pixel_y = y * 8
                coin_positions.append((pixel_x, pixel_y))
    
    print(coin_positions)
    return coin_positions

class Game(World):
    def __init__(self):
        super().__init__()
        self.screen_size = SCREEN_SIZE
        self.fps = FPS
        self.init()
        
    def init(self):
        pyxel.init(self.screen_size[0], self.screen_size[1], title=title, fps=self.fps)
        pyxel.images[0] = pyxel.Image.from_image(image_filepath, incl_colors=True)
        for i in range(7):
            pyxel.tilemaps[i] = pyxel.Tilemap.from_tmx(tilemap_filepath, i)
        
    def draw(self):
        pyxel.cls(0)
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
    
    # Spawn entities with adjusted parameters
    spawn_player(game, 8*10, 8*10, 16, 16, jump_power=3.6, move_speed=2.0)
    spawn_background(game, 0)
    spawn_background(game, 2)
    spawn_collidable_tilemap(game, 4, 2)
    spawn_collidable_tilemap(game, 3, 8)
    # spawn_collidable_tilemap(game, 1, 8)
    spawn_goal_marker_tilemap(game, 1)
    spawn_collidable_tilemap(game, 5, 8)
    spawn_stage_state(game, 0, 60.0)
    spawn_enemy(game, 0, 8*12, 8*10)
    spawn_enemy(game, 0, 8*62, 8*10)
    # Spawn coins using positions from tilemap
    coin_positions = get_coin_positions_from_tilemap(6)
    for pos in coin_positions:
        spawn_coin(game, pos[0], pos[1])
    
    # spawn_floor(game, 0, 8)
    # spawn_background(game, 3)
    
    # Add systems with adjusted parameters
    game.add_system_to_scenes(SysTilemapCollision, "playable", 1)
    game.add_system_to_scenes(SysSimulateGravity, "playable", 5, gravity=0.2, max_fall_speed=2.0)
    game.add_system_to_scenes(SysCharacterMovement, "playable", 2)
    game.add_system_to_scenes(SysPlayerControl, "playable", 3, acceleration=0.5, friction=0.85)
    game.add_system_to_scenes(SysPlayerAnimation, "playable", 6, animation_speed=6)
    game.add_system_to_scenes(SysUpdatePosition, "playable", 4)
    game.add_system_to_scenes(SysRestartStage, "playable", 100)
    game.add_system_to_scenes(SysPlayerGoal, "playable", 200)
    game.add_system_to_scenes(SysUpdateStageState, "playable", 300)
    game.add_system_to_scenes(SysPlayerDieFromFall, "playable", 400)
    
    ## Enemy
    game.add_system_to_scenes(SysEnemyWalk, "playable", 100)
    # game.add_system_to_scenes(SysEnemyMovement, "playable", 200)
    game.add_system_to_scenes(SysEnemyAnimation, "playable", 300)
    
    # Add screens
    game.add_screen_to_scenes(ScTileMaps, "playable", 0)
    game.add_screen_to_scenes(ScPlayer, "playable", 100)
    game.add_screen_to_scenes(ScStageClock, "playable", 1000)
    game.add_screen_to_scenes(ScGameOver, "playable", 2000)
    game.add_screen_to_scenes(ScGoal, "playable", 3000)
    
    ## Enemy
    game.add_screen_to_scenes(ScEnemy, "playable", 4000)
    
    ## Debug
    game.add_screen_to_scenes(ScDebugPlayer, "playable", 5000)
    
    ## Coin
    game.add_screen_to_scenes(ScCoin, "playable", 50)
    
    game.run()