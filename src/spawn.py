from pigframe import World
from component import *
from system import *

def spawn_player(world: World, x: int, y: int, width: int, height: int, jump_power: int = 2, move_speed: float = 0.15):
    entity = world.create_entity()
    world.add_component_to_entity(entity, BaseCollidable)
    world.add_component_to_entity(entity, RectRigidBody, width=width, height=height)
    world.add_component_to_entity(entity, Position2D, x=x, y=y)
    world.add_component_to_entity(entity, Velocity2D, x=0, y=0)
    world.add_component_to_entity(entity, CollisionInfo)
    world.add_component_to_entity(entity, Player)
    world.add_component_to_entity(entity, Movable, speed=move_speed, jump_power=jump_power)
    return entity

def spawn_floor(world: World, tilemap_id: int, surface_height: int):
    entity = world.create_entity()
    world.add_component_to_entity(entity, TileCollidable, surface_height=surface_height)
    world.add_component_to_entity(entity, TileMap, id=tilemap_id)
    return entity

def spawn_background(world: World, tilemap_id: int):
    entity = world.create_entity()
    world.add_component_to_entity(entity, TileMap, id=tilemap_id)
    return entity
