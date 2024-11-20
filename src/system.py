from pigframe import System
from component import *
from utils import *
from stage import reset_stage

class SysSimulateGravity(System):
    def __init__(self, world, priority: int = 0, **kwargs) -> None:
        super().__init__(world, priority, **kwargs)
        self.gravity = kwargs.get("gravity", 0.2)
        self.max_fall_speed = kwargs.get("max_fall_speed", 4.0)
    
    def process(self):
        for entity, (_, velocity) in self.world.get_components(BaseCollidable, Velocity2D):
            velocity.y += self.gravity
            # Limit maximum falling speed
            velocity.y = min(velocity.y, self.max_fall_speed)

class SysTilemapCollision(System):
    def __init__(self, world, priority: int = 0, **kwargs) -> None:
        super().__init__(world, priority, **kwargs)

    def process(self):
        # Assumes there is only one floor entity
        
        for entity, (_, _, body, position, collision_info) in self.world.get_components(BaseCollidable, Movable,RectRigidBody, Position2D, CollisionInfo):
            bottom = False
            top = False
            left = False
            right = False
            for entity, (tile_collidable, tilemap) in self.world.get_components(TileCollidable, TileMap): 
                # Update collision info of RigidBody objects (RectRigidBody)
                collisions = check_collision_tilemap(position, body, tilemap.id, tile_collidable.surface_height)
                if collisions["bottom"]:
                    bottom = True
                if collisions["top"]:
                    top = True
                if collisions["left"]:
                    left = True
                if collisions["right"]:
                    right = True
            
            collision_info.bottom = bottom
            collision_info.top = top
            collision_info.left = left
            collision_info.right = right

class SysCharacterCollision(System):
    def __init__(self, world, priority: int = 0, **kwargs) -> None:
        super().__init__(world, priority, **kwargs)
    
    def process(self):
        for entity, (_, position, body, collision_info) in self.world.get_components(BaseCollidable, Position2D, RectRigidBody, CollisionInfo):
            bottom = False
            top = False
            left = False
            right = False
            for entity2, (_, position2, body2, collision_info2) in self.world.get_components(BaseCollidable, Position2D, RectRigidBody, CollisionInfo):
                if entity == entity2:
                    continue
                collisions = check_collision_rect_rect(position, body, position2, body2)
                if collisions["left"]:
                    left = True
                if collisions["right"]:
                    right = True
                if collisions["bottom"]:
                    bottom = True
                if collisions["top"]:
                    top = True
            
            collision_info.bottom = bottom
            collision_info.top = top
            collision_info.left = left
            collision_info.right = right

class SysCharacterMovement(System):
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
            if collision_info.left and velocity.x < 0:
                velocity.x = 0
                position.next_x = position.x
            elif collision_info.right and velocity.x > 0:
                velocity.x = 0
                position.next_x = position.x
            else:
                position.next_x = position.x + velocity.x

class SysUpdatePosition(System):
    def __init__(self, world, priority: int = 0, **kwargs) -> None:
        super().__init__(world, priority, **kwargs)

    def process(self):
        for entity, (movable, position) in self.world.get_components(Movable, Position2D):
            position.x = position.next_x
            position.y = position.next_y

class SysPlayerControl(System):
    def __init__(self, world, priority: int = 0, **kwargs) -> None:
        super().__init__(world, priority, **kwargs)
        self.acceleration = kwargs.get("acceleration", 0.5)
        self.friction = kwargs.get("friction", 0.7)
    
    def process(self):
        for entity, (_, movable, body, velocity, collision_info) in self.world.get_components(Player, Movable, RectRigidBody, Velocity2D, CollisionInfo):
            # Only allow jumping when on the ground
            ignore_value = 10000
            gamepad_input_x = pyxel.btnv(pyxel.GAMEPAD1_AXIS_LEFTX)
            gamepad_input_y = pyxel.btnv(pyxel.GAMEPAD1_AXIS_LEFTY)
            print("gamepad input:", gamepad_input_x, gamepad_input_y)

            if self.world.actions.jump and collision_info.bottom:
                velocity.y = -movable.jump_power
            
            # Horizontal movement with acceleration
            if self.world.actions.left:
                velocity.x -= self.acceleration
                velocity.x = max(velocity.x, -movable.speed)
                body.flip_x = True
            elif self.world.actions.right:
                velocity.x += self.acceleration
                velocity.x = min(velocity.x, movable.speed)
                body.flip_x = False
            elif gamepad_input_x < -ignore_value:
                velocity.x -= self.acceleration
                velocity.x = max(velocity.x, -movable.speed)
                body.flip_x = True
            elif gamepad_input_x > ignore_value:
                velocity.x += self.acceleration
                velocity.x = min(velocity.x, movable.speed)
                body.flip_x = False
            else:
                # Apply friction when no movement keys are pressed
                velocity.x *= self.friction
                # Stop completely if velocity is very small
                if abs(velocity.x) < 0.1:
                    velocity.x = 0
            
class SysPlayerAnimation(System):
    def __init__(self, world, priority: int = 0, **kwargs) -> None:
        super().__init__(world, priority, **kwargs)
        self.animation_speed = kwargs.get("animation_speed", 6)
    
    def process(self):
        for entity, (_, velocity, body, animation) in self.world.get_components(Player, Velocity2D, RectRigidBody, Animation):
            # Update running state
            animation.is_running = abs(velocity.x) > 0.1
            animation.is_jumping = velocity.y < -0.5
            gamepad_ignore_value = 10000
            gamepad_input_y = pyxel.btnv(pyxel.GAMEPAD1_AXIS_LEFTY)
            animation.is_crouching = self.world.actions.crouch or gamepad_input_y > gamepad_ignore_value
            # animation.is_falling = velocity.y > 0.5
            
            sprite_x = 0
            sprite_y = 8*11
            if animation.is_running:
                animation.timer += 1
                if animation.timer > self.animation_speed:
                    animation.timer = 0
                    animation.frame = (animation.frame + 1) % 2
                sprite_x = 16 if animation.frame == 1 else 0
                sprite_y = 8*13
            
            if animation.is_jumping:
                sprite_x = 16
                sprite_y = 8*11
                
            if animation.is_crouching:
                sprite_x = 48
                sprite_y = 8*11
            
            # if animation.is_falling:
            #     sprite_x = 32
            #     sprite_y = 8*11
            
            animation.sprite_x = sprite_x
            animation.sprite_y = sprite_y

class SysRestartStage(System):
    def __init__(self, world, priority: int = 0, **kwargs) -> None:
        super().__init__(world, priority, **kwargs)

    def process(self):
        if self.world.actions.restart:
            player_entity, (_, position, velocity) = self.world.get_components(Player, Position2D, Velocity2D)[0]
            stage_state_entity, stage_state = self.world.get_component(StageState)[0]
            stage_state.time_remaining = 60.0
            stage_state.game_over = False
            stage_state.is_goal = False
            stage_state.lives = 3
            stage_state.coins = 0
            position.x = 8*10
            position.y = 8*10
            velocity.x = 0
            velocity.y = 0
            reset_stage(self.world, stage_state.init_enemy_positions)

class SysPlayerGoal(System):
    def __init__(self, world, priority: int = 0, **kwargs) -> None:
        super().__init__(world, priority, **kwargs)

    def process(self):
        goal_marker_entity, goal_marker_tilemap = self.world.get_component(GoalMarkerTileMap)[0]
        player_entity, (_, position, body) = self.world.get_components(Player, Position2D, RectRigidBody)[0]
        collisions = check_collision_tilemap(position, body, goal_marker_tilemap.id, goal_marker_tilemap.pixel_size)
        stage_state_entity, stage_state = self.world.get_component(StageState)[0]
        if collisions["bottom"] or collisions["left"]:
            stage_state.is_goal = True

class SysUpdateStageState(System):
    def __init__(self, world, priority: int = 0, **kwargs) -> None:
        super().__init__(world, priority, **kwargs)

    def process(self):
        for entity, stage_state in self.world.get_component(StageState):
            if not stage_state.game_over and not stage_state.is_goal:
                stage_state.time_remaining -= 1 / 60
                if stage_state.time_remaining <= 0:
                    stage_state.game_over = True

class SysEnemyWalk(System):
    def __init__(self, world, priority: int = 0, **kwargs) -> None:
        super().__init__(world, priority, **kwargs)

    def process(self):
        for entity, (_, _, body, velocity, collision_info) in self.world.get_components(Enemy, MoveMethodWalk, RectRigidBody, Velocity2D, CollisionInfo):
            if collision_info.left:
                velocity.x = 1.0
                body.flip_x = False
            elif collision_info.right:
                velocity.x = -1.0
                body.flip_x = True

class SysEnemyMovement(System):
    def __init__(self, world, priority: int = 0, **kwargs) -> None:
        super().__init__(world, priority, **kwargs)

    def process(self):
        for entity, (_, position, velocity) in self.world.get_components(Enemy, Position2D, Velocity2D):
            position.next_x = position.x + velocity.x
            position.next_y = position.y + velocity.y

class SysEnemyAnimation(System):
    def __init__(self, world, priority: int = 0, **kwargs) -> None:
        super().__init__(world, priority, **kwargs)
        self.animation_speed = kwargs.get("animation_speed", 6)
    
    def process(self):
        for entity, (_, body, animation) in self.world.get_components(Enemy, RectRigidBody, EnemyAnimation):
            sprite_x = 32
            sprite_y = 8*7
            animation.timer += 1
            if animation.timer > self.animation_speed:
                animation.timer = 0
                animation.frame = (animation.frame + 1) % 4
            
            if animation.frame == 1:
                sprite_x = 48
                sprite_y = 8*7
            elif animation.frame == 2:
                sprite_x = 64
                sprite_y = 8*7
            elif animation.frame == 3:
                sprite_x = 48
                sprite_y = 8*7
            
            animation.sprite_x = sprite_x
            animation.sprite_y = sprite_y

class SysPlayerDieFromFall(System):
    def __init__(self, world, priority: int = 0, **kwargs) -> None:
        super().__init__(world, priority, **kwargs)

    def process(self):
        player_entity, (_, position, body, velocity, collision_info) = self.world.get_components(Player, Position2D, RectRigidBody, Velocity2D, CollisionInfo)[0]
        if position.y > 8*15:
            stage_state_entity, stage_state = self.world.get_component(StageState)[0]
            # stage_state.time_remaining = 60.0
            stage_state.game_over = False
            stage_state.is_goal = False
            position.x = 8*10
            position.y = 8*10
            velocity.x = 0
            velocity.y = 0
            if stage_state.lives > 0:
                stage_state.lives -= 1
                reset_stage(self.world, stage_state.init_enemy_positions)

class SysPlayerDieNoHP(System):
    def __init__(self, world, priority: int = 0, **kwargs) -> None:
        super().__init__(world, priority, **kwargs)
    
    def process(self):
        player_entity, (_, position, body, velocity, collision_info) = self.world.get_components(Player, Position2D, RectRigidBody, Velocity2D, CollisionInfo)[0]
        stage_state_entity, stage_state = self.world.get_component(StageState)[0]
        if stage_state.lives <= 0:
            stage_state.game_over = True

class SysCollectCoin(System):
    def __init__(self, world, priority: int = 0, **kwargs) -> None:
        super().__init__(world, priority, **kwargs)

    def process(self):
        player_entity, (_, position, body) = self.world.get_components(Player, Position2D, RectRigidBody)[0]
        stage_state_entity, stage_state = self.world.get_component(StageState)[0]
        for entity, (_, _, coin_state, coin_position, coin_body) in self.world.get_components(Coin, Collectible, CoinState, Position2D, CircleRigidBody):
            if coin_state.is_collected:
                continue
            if check_intersection_rect_circle(position, body, coin_position, coin_body):
                coin_state.is_collected = True
                stage_state.coins += 1

class SysPlayerEnemyCollision(System):
    def __init__(self, world, priority: int = 0, **kwargs) -> None:
        super().__init__(world, priority, **kwargs)

    def process(self):
        player_entity, (_, position, body) = self.world.get_components(Player, Position2D, RectRigidBody)[0]
        stage_state_entity, stage_state = self.world.get_component(StageState)[0]
        for entity, (_, velocity, enemy_position, enemy_body) in self.world.get_components(Enemy, Velocity2D, Position2D, RectRigidBody):
            collisions = check_collision_rect_rect(position, body, enemy_position, enemy_body)
            intersection_angle = check_intersection_angle(position, body, enemy_position, enemy_body)
            
            # if angle is less than 45 degrees, it is a hit from the side
            if abs(intersection_angle) < math.pi / 4 and (collisions["left"] or collisions["right"]):
                print("hit enemy")
                if stage_state.lives > 0:
                    stage_state.lives -= 1
                    velocity.x *= -1
                    enemy_body.flip_x = not enemy_body.flip_x
                    
                    break
            if abs(intersection_angle) > math.pi / 4 and collisions["bottom"]:
                print("step on enemy")
                self.world.remove_entity(entity)
                
class SysExitGame(System):
    def __init__(self, world, priority: int = 0, **kwargs) -> None:
        super().__init__(world, priority, **kwargs)

    def process(self):
        if self.world.actions.exit:
            pyxel.quit()
