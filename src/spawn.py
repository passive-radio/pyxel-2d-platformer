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
    entity = world.create_entity()
    world.add_component_to_entity(entity, TileCollidable, surface_height=surface_height)
    world.add_component_to_entity(entity, TileMap, id=tilemap_id)
    return entity


def spawn_background(world: World, tilemap_id: int):
    entity = world.create_entity()
    world.add_component_to_entity(entity, TileMap, id=tilemap_id)
    return entity


def spawn_goal_marker_tilemap(world: World, tilemap_id: int):
    entity = world.create_entity()
    world.add_component_to_entity(entity, GoalMarkerTileMap, id=tilemap_id)
    world.add_component_to_entity(entity, TileCollidable, surface_height=0)
    world.add_component_to_entity(entity, TileMap, id=tilemap_id)
    return entity


def spawn_stage(
    world: World, id: int, time_remaining: float, init_enemy_positions: list[tuple[int, int]]
):
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
    entity = world.create_entity()
    world.add_component_to_entity(entity, Collectible)
    world.add_component_to_entity(entity, Coin)
    world.add_component_to_entity(entity, Position2D, x=x, y=y)
    world.add_component_to_entity(entity, CoinState, is_collected=False)
    world.add_component_to_entity(entity, CircleRigidBody, radius=8)
    return entity
