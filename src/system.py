from pigframe import System
from component import *
import pyxel

def check_collision(pos: Position2D, body: RectRigidBody, tilemap_id: int, surface_height: int = None):
    # Convert pixel coordinates to tile coordinates
    tile_x1 = pyxel.floor(pos.x) // 8
    tile_y1 = pyxel.floor(pos.y) // 8
    tile_x2 = (pyxel.ceil(pos.x) + body.width - 1) // 8
    tile_y2 = (pyxel.ceil(pos.y) + body.height - 1) // 8
    
    collisions = {
        "left": False,
        "right": False,
        "top": False,
        "bottom": False
    }
    
    for yi in range(tile_y1, tile_y2 + 1):
        for xi in range(tile_x1, tile_x2 + 1):
            col, colkey = pyxel.tilemaps[tilemap_id].pget(xi, yi)
            if col == 0:  # Assuming 0 means empty/no collision
                continue
                
            # Get tile boundaries in pixel coordinates
            tile_left = xi * 8
            tile_right = tile_left + 8
            tile_top = yi * 8 + 6
            tile_bottom = tile_top + 2
            
            # プレイヤーの実際の判定範囲（surface heightを考慮）
            player_bottom = pos.y + body.height
            player_adjusted_bottom = player_bottom - surface_height  # surface_height pixels を無視
            
            # 左右の衝突判定は、surface heightによるオーバーラップを除外
            if not (player_bottom > tile_top and player_adjusted_bottom < tile_top):
                if tile_left <= pos.x + body.width <= tile_right:
                    collisions["right"] = True
                if tile_left <= pos.x <= tile_right:
                    collisions["left"] = True
            if tile_top <= pos.y + body.height <= tile_bottom:
                collisions["bottom"] = True
            if tile_top <= pos.y <= tile_bottom:
                collisions["top"] = True
    return collisions

class SysSimulateGravity(System):
    def __init__(self, world, priority: int = 0, **kwargs) -> None:
        super().__init__(world, priority, **kwargs)
        self.gravity = kwargs.get("gravity", 0.1)
    
    def process(self):
        for entity, (_, velocity) in self.world.get_components(BaseCollidable, Velocity2D):
            velocity.y += self.gravity

class SysFloorCollision(System):
    def __init__(self, world, priority: int = 0, **kwargs) -> None:
        super().__init__(world, priority, **kwargs)

    def process(self):
        # Assumes there is only one floor entity
        floor_entity, floor_collidable = self.world.get_component(TileCollidable)[0]
        floor_tilemap = self.world.get_entity_object(floor_entity)[TileMap]
        
        # Update collision info of RigidBody objects (RectRigidBody)
        for entity, (_, body, position, collision_info) in self.world.get_components(BaseCollidable, RectRigidBody, Position2D, CollisionInfo):
            collisions = check_collision(position, body, floor_tilemap.id, floor_collidable.surface_height)
            if collisions["bottom"]:
                collision_info.bottom = True
            else:
                collision_info.bottom = False
            if collisions["top"]:
                collision_info.top = True
            else:
                collision_info.top = False
            if collisions["left"]:
                collision_info.left = True
            else:
                collision_info.left = False
            if collisions["right"]:
                collision_info.right = True
            else:
                collision_info.right = False

class SysPlayerMovement(System):
    def __init__(self, world, priority: int = 0, **kwargs) -> None:
        super().__init__(world, priority, **kwargs)

    def process(self):
        for entity, (_, position, velocity, collision_info) in self.world.get_components(BaseCollidable, Position2D, Velocity2D, CollisionInfo):
            # Handle vertical movement
            if collision_info.bottom and velocity.y > 0:
                velocity.y = 0
                position.next_y = position.y
            elif collision_info.top and velocity.y < 0:
                velocity.y = 0
                position.next_y = position.y
            else:
                position.next_y = position.y + velocity.y
            
            # Handle horizontal movement
            if collision_info.left:
                velocity.x = 0
                position.next_x = position.x
            elif collision_info.right:
                velocity.x = 0
                position.next_x = position.x
            else:
                position.next_x = position.x + velocity.x

class SysUpdatePosition(System):
    def __init__(self, world, priority: int = 0, **kwargs) -> None:
        super().__init__(world, priority, **kwargs)

    def process(self):
        for entity, position in self.world.get_component(Position2D):
            position.x = position.next_x
            position.y = position.next_y

class SysPlayerControl(System):
    def __init__(self, world, priority: int = 0, **kwargs) -> None:
        super().__init__(world, priority, **kwargs)
    
    def process(self):
        for entity, (_, movable, velocity, collision_info) in self.world.get_components(Player, Movable, Velocity2D, CollisionInfo):
            # Only allow jumping when on the ground
            print("jump", self.world.actions.jump)
            if self.world.actions.jump and collision_info.bottom:
                print("player jump")
                velocity.y = -movable.jump_power
            
            # Horizontal movement
            if self.world.actions.left:
                velocity.x = -movable.speed
            elif self.world.actions.right:
                velocity.x = movable.speed
            else:
                velocity.x = 0
