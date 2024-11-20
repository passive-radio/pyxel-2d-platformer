import pyxel
from component import *

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
            tile_top = yi * 8 + (8 - surface_height)
            tile_bottom = tile_top + surface_height
            
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