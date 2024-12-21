from pigframe import World
from component import *


def spawn_player(
    world: World,
    x: int,
    y: int,
    width: int,
    height: int,
    jump_power: int = 2,
    move_speed: float = 0.15,
):
    """プレイヤーをスポーンする関数

    Args:
        world (World): ゲームのワールド
        x (int): 初期X座標
        y (int): 初期Y座標
        width (int): プレイヤーの幅
        height (int): プレイヤーの高さ
        jump_power (int, optional): ジャンプ力. Defaults to 2.
        move_speed (float, optional): 移動速度. Defaults to 0.15.
    """
    entity = world.create_entity()
    world.add_component_to_entity(entity, BaseCollidable)
    world.add_component_to_entity(entity, RectRigidBody, width=width, height=height)
    world.add_component_to_entity(entity, Position2D, x=x, y=y, prev_x=x, prev_y=y)
    world.add_component_to_entity(entity, Velocity2D, x=0, y=0)
    world.add_component_to_entity(entity, CollisionInfo)
    world.add_component_to_entity(entity, Player)
    world.add_component_to_entity(entity, Movable, speed=move_speed, jump_power=jump_power)
    world.add_component_to_entity(entity, Animation)
    return entity


def spawn_collidable_tilemap(world: World, tilemap_id: int, surface_height: int):
    """衝突可能なタイルマップをスポーンする関数

    Args:
        world (World): ゲームのワールド
        tilemap_id (int): タイルマップのID
        surface_height (int): 表面の高さ
    """
    entity = world.create_entity()
    world.add_component_to_entity(entity, TileCollidable, surface_height=surface_height)
    world.add_component_to_entity(entity, TileMap, id=tilemap_id)
    return entity


def spawn_background(world: World, tilemap_id: int):
    """背景をスポーンする関数

    Args:
        world (World): ゲームのワールド
        tilemap_id (int): タイルマップのID
    """
    entity = world.create_entity()
    world.add_component_to_entity(entity, TileMap, id=tilemap_id)
    return entity


def spawn_goal_marker_tilemap(world: World, tilemap_id: int):
    """ゴールマーカーのタイルマップをスポーンする関数

    Args:
        world (World): ゲームのワールド
        tilemap_id (int): タイルマップのID
    """
    entity = world.create_entity()
    world.add_component_to_entity(entity, GoalMarkerTileMap, id=tilemap_id)
    world.add_component_to_entity(entity, TileCollidable, surface_height=0)
    world.add_component_to_entity(entity, TileMap, id=tilemap_id)
    return entity


def spawn_stage(
    world: World, id: int, time_remaining: float, init_enemy_positions: list[tuple[int, int]]
):
    """ステージをスポーンする関数

    Args:
        world (World): ゲームのワールド
        id (int): ステージのID
        time_remaining (float): 残り時間
        init_enemy_positions (list[tuple[int, int]]): 敵の初期位置
    """
    entity = world.create_entity()
    world.add_component_to_entity(
        entity,
        StageState,
        id=id,
        time_remaining=time_remaining,
        init_enemy_positions=init_enemy_positions,
    )

    enemy_entities = []
    for pos in init_enemy_positions:
        enemy_entities.append(spawn_enemy(world, 0, pos[0], pos[1]))
    return entity, enemy_entities


def spawn_enemy(world: World, species_id: int, x: int, y: int):
    """敵をスポーンする関数

    Args:
        world (World): ゲームのワールド
        species_id (int): 敵の種別ID
        x (int): 初期X座標
        y (int): 初期Y座標
    """
    entity = world.create_entity()
    world.add_component_to_entity(entity, Enemy, species_id=species_id)
    world.add_component_to_entity(entity, Movable)
    world.add_component_to_entity(entity, RectRigidBody, width=16, height=16)
    world.add_component_to_entity(entity, Position2D, x=x, y=y, prev_x=x, prev_y=y)
    world.add_component_to_entity(entity, Velocity2D, x=0, y=0)
    world.add_component_to_entity(entity, MoveMethodWalk)
    world.add_component_to_entity(entity, EnemyState, is_dead=False)
    world.add_component_to_entity(entity, EnemyAnimation, frame=0, timer=0, is_running=True)
    world.add_component_to_entity(entity, BaseCollidable)
    world.add_component_to_entity(entity, CollisionInfo)
    return entity


def spawn_coin(world: World, x: int, y: int):
    """コインをスポーンする関数

    Args:
        world (World): ゲームのワールド
        x (int): 初期X座標
        y (int): 初期Y座標
    """
    entity = world.create_entity()
    world.add_component_to_entity(entity, Collectible)
    world.add_component_to_entity(entity, Coin)
    world.add_component_to_entity(entity, Position2D, x=x, y=y)
    world.add_component_to_entity(entity, CoinState, is_collected=False)
    world.add_component_to_entity(entity, CircleRigidBody, radius=8)
    return entity
