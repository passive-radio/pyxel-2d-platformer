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
        for entity, (_, position, body, animation) in self.world.get_components(
            Player, Position2D, RectRigidBody, Animation
        ):
            # Draw player with animation
            pyxel.blt(
                pyxel.width // 2,
                position.y,
                0,  # image bank
                animation.sprite_x,  # sprite x in tileset
                animation.sprite_y,  # sprite y in tileset
                -body.width if body.flip_x else body.width,  # width (negative for left flip)
                body.height,  # height
                0,  # colorkey
            )


class ScStageClock(Screen):
    def __init__(self, world, priority: int = 0) -> None:
        super().__init__(world, priority)

    def draw(self):
        stage_state_entity, stage_state = self.world.get_component(StageState)[0]
        pyxel.text(2, 2, f"TIME: {stage_state.time_remaining:.1f}", 1)


class ScGameOver(Screen):
    def __init__(self, world, priority: int = 0) -> None:
        super().__init__(world, priority)

    def draw(self):
        stage_state_entity, stage_state = self.world.get_component(StageState)[0]
        if stage_state.game_over:
            message = "GAME OVER"
            pos_x = pyxel.width // 2 - len(message)
            pyxel.text(pos_x, pyxel.height // 2, message, 1)


class ScGoal(Screen):
    def __init__(self, world, priority: int = 0) -> None:
        super().__init__(world, priority)

    def draw(self):
        stage_state_entity, stage_state = self.world.get_component(StageState)[0]
        if stage_state.is_goal:
            message = "GOAL!"
            pos_x = pyxel.width // 2 - len(message)
            pyxel.text(pos_x, pyxel.height // 2, message, 1)


class ScEnemy(Screen):
    def __init__(self, world, priority: int = 0) -> None:
        super().__init__(world, priority)

    def draw(self):
        player_ent, (_, player_pos) = self.world.get_components(Player, Position2D)[0]
        for entity, (_, position, body, animation) in self.world.get_components(
            Enemy, Position2D, RectRigidBody, EnemyAnimation
        ):
            diff_from_center_x = position.x - player_pos.x
            diff_from_center_y = position.y
            # player の位置を基準に描画
            local_x = pyxel.width // 2 + diff_from_center_x
            local_y = diff_from_center_y
            pyxel.blt(
                local_x,
                local_y,
                0,  # image bank
                animation.sprite_x,  # sprite x in tileset
                animation.sprite_y,  # sprite y in tileset
                -body.width if body.flip_x else body.width,  # width (negative for left flip)
                body.height,  # height
                0,  # colorkey
            )


class ScDebugColorPalette(Screen):
    def __init__(self, world, priority: int = 0) -> None:
        super().__init__(world, priority)

    def draw(self):
        base_x = 120
        base_y = 2
        for x in range(8):
            for y in range(3):
                color_id = x + y * 8
                pyxel.rect(base_x + x * 8, base_y + y * 8, 8, 8, color_id)


class ScDebugPlayer(Screen):
    def __init__(self, world, priority: int = 0) -> None:
        super().__init__(world, priority)

    def draw(self):
        for entity, (_, position) in self.world.get_components(Player, Position2D):
            pyxel.text(50, 2, f"x: {position.x:.1f}, y: {position.y:.1f}", 1)


class ScCoin(Screen):
    def __init__(self, world, priority: int = 0) -> None:
        super().__init__(world, priority)

    def draw(self):
        player_ent, (_, player_pos) = self.world.get_components(Player, Position2D)[0]
        for entity, (_, state, position, body) in self.world.get_components(
            Coin, CoinState, Position2D, CircleRigidBody
        ):
            if state.is_collected:
                continue
            diff_from_center_x = position.x - player_pos.x
            diff_from_center_y = position.y
            local_x = pyxel.width // 2 + diff_from_center_x
            local_y = diff_from_center_y
            pyxel.blt(local_x, local_y, 0, 16, 8 + 16 * 4, body.radius * 2, body.radius * 2, 0)


class ScLives(Screen):
    def __init__(self, world, priority: int = 0) -> None:
        super().__init__(world, priority)

    def draw(self):
        stage_state_entity, stage_state = self.world.get_component(StageState)[0]
        life_sprite_x = 8 * 3
        life_sprite_y = 8 * 0
        for i in range(stage_state.lives):
            pyxel.blt(2 + i * 10, 8, 0, life_sprite_x, life_sprite_y, 8, 8, 0)


class ScCoinCount(Screen):
    def __init__(self, world, priority: int = 0) -> None:
        super().__init__(world, priority)

    def draw(self):
        stage_state_entity, stage_state = self.world.get_component(StageState)[0]
        sprite_x = 8 * 4
        sprite_y = 8 * 0
        base_x = 38
        pyxel.blt(base_x, 8, 0, sprite_x, sprite_y, 8, 8, 0)
        pyxel.text(base_x + 11, 9, "x", 1)
        pyxel.text(base_x + 16, 9, f"{int(stage_state.coins)}", 1)
