import pyxel
from pigframe import *

SCREEN_SIZE = (8*34, 8*2*10) # (288, 160)
image_filepath = "assets/2d-platformer.png"
tilemap_filepath = "assets/map01.tmx"

def is_colliding(x, y):
    x1 = pyxel.floor(x) // 8
    y1 = pyxel.floor(y) // 8
    x2 = (pyxel.ceil(x) + 15) // 8
    y2 = (pyxel.ceil(y) + 15) // 8
    for yi in range(y1, y2 + 1):
        for xi in range(x1, x2 + 1):
            if pyxel.tilemaps[2].pget(xi, yi) != (0,0):
                return True
    return False


class App(World):
    def __init__(self):
        super().__init__()
        self.screen_size = SCREEN_SIZE
        self.init()

    
    def init(self):
        pyxel.init(self.screen_size[0], self.screen_size[1], title="2d-platformer", fps=60)
        pyxel.images[0] = pyxel.Image.from_image(
            image_filepath, incl_colors=True
        )
        
        for i in range(0,4,1):
            print(i)
            pyxel.tilemaps[i] = pyxel.Tilemap.from_tmx(tilemap_filepath, i)
        
        self.player_pos = [8, 8*8]
        self.player_vel = [0.0,0.0]
        self.player_jumping = False
        self.player_jump_number = 0
        self.player_died = False
        self.facing_left = False
        self.is_running = False
        self.animation_frame = 0
        self.animation_timer = 0
    
    def reset(self):
        self.player_pos = [8, 8*8]
        self.player_vel = [0.0,0.0]
        self.player_jumping = False
        self.player_jump_number = 0
        self.player_died = False
        self.facing_left = False
        self.is_running = False
        self.animation_frame = 0
        self.animation_timer = 0
    
    def draw(self):
        pyxel.cls(0)
        # Calculate camera offset to center on player
        camera_x = self.player_pos[0] - pyxel.width // 2
        camera_y = 0
        
        # Draw all tilemap layers with camera offset
        pyxel.bltm(0, 0, 0, camera_x, camera_y, pyxel.width, pyxel.height, 0)
        pyxel.bltm(0, 0, 1, camera_x, camera_y, pyxel.width, pyxel.height, 0)
        pyxel.bltm(0, 0, 2, camera_x, camera_y, pyxel.width, pyxel.height, 0)
        pyxel.bltm(0, 0, 3, camera_x, camera_y, pyxel.width, pyxel.height, 0)
        
        # Draw player at center of screen
        # Player sprite drawing with animation
        sprite_x = 0  # Base sprite x position in tileset
        sprite_y = 8*11
        if self.is_running:
            sprite_x = (0 if self.animation_frame == 1 else 16)  # Running frames at x=16 and x=32
            sprite_y = 8*13
            # print(sprite_x, sprite_y)
        
        # Draw player with appropriate sprite and flipping
        pyxel.blt(
            pyxel.width//2,  # screen x
            self.player_pos[1],  # screen y
            0,  # image bank
            sprite_x,  # sprite x in tileset
            sprite_y,  # sprite y in tileset
            -16 if self.facing_left else 16,  # width (negative for left flip)
            16,  # height
            0  # colorkey
        )
        # pyxel.blt(pyxel.width//2, self.player_pos[1], 0, 0, 8*11, 16, 16, 0)
        
        if self.player_died:
            # pyxel.cls(5)
            message = "You died..."
            pyxel.text(pyxel.width//2 - len(message), pyxel.height//2 - 5, message, 0)
    
    def process(self):
        super().process()
        self.player_vel[1] += 0.1
        
        # Check ground collision and reset jump state
        if is_colliding(self.player_pos[0], self.player_pos[1]-8):
            self.player_jumping = False
            self.player_jump_number = 0
            self.player_vel[1] = 0
        
        # Horizontal movement
        if pyxel.btn(pyxel.KEY_A):
            self.player_vel[0] = -1.5
        elif pyxel.btn(pyxel.KEY_D):
            self.player_vel[0] = 1.5
        else:
            self.player_vel[0] = 0
        
        if pyxel.btnp(pyxel.KEY_RETURN):
            self.reset()
        
        # Vertical movement (removed W/S controls for platformer physics)
        if pyxel.btnp(pyxel.KEY_SPACE):
            if not self.player_jumping:  # First jump
                self.player_vel[1] = -2
                self.player_jumping = True
                self.player_jump_number = 1
            elif self.player_jump_number < 2:  # Second jump
                self.player_vel[1] = -2
                self.player_jump_number = 2
        
        if self.player_pos[1] > pyxel.height + 20:
            # die
            self.player_died = True
        
        self.player_pos[0] += self.player_vel[0]
        self.player_pos[1] += self.player_vel[1]
        print(self.player_pos, self.player_vel)
        
        # Update animation state
        self.is_running = self.player_vel[0] != 0
        if self.player_vel[0] < 0:
            self.facing_left = True
        elif self.player_vel[0] > 0:
            self.facing_left = False
        
        # Update animation timer and frame
        if self.is_running:
            self.animation_timer += 1
            if self.animation_timer > 6:  # Adjust this number to control animation speed
                self.animation_timer = 0
                self.animation_frame = (self.animation_frame + 1) % 2  # Toggle between 0 and 1
    
    def run(self):
        pyxel.run(self.process, self.draw)
        

if __name__ == "__main__":
    app = App()
    app.run()