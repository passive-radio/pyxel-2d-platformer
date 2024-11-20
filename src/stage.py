from spawn import *

def reset_stage(world: World, enemy_positions: list[tuple[int, int]]):
    for pos in enemy_positions:
        spawn_enemy(world, 0, pos[0], pos[1])
    
    for coin_ent, (_, coin_state) in world.get_components(Coin, CoinState):
        coin_state.is_collected = False
