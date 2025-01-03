import pyxel
from component import *


def check_collision_tilemap(
    pos: Position2D, body: RectRigidBody, tilemap_id: int, surface_height: int = None
):
    """タイルマップとの衝突をチェックする関数

    Args:
        pos (Position2D): オブジェクトの位置
        body (RectRigidBody): オブジェクトのボディ
        tilemap_id (int): タイルマップのID
        surface_height (int, optional): 表面の高さ. Defaults to None.
    """
    # Convert pixel coordinates to tile coordinates
    tile_x1 = pyxel.floor(pos.x) // 8
    tile_y1 = pyxel.floor(pos.y) // 8
    tile_x2 = (pyxel.ceil(pos.x) + body.width - 1) // 8
    tile_y2 = (pyxel.ceil(pos.y) + body.height - 1) // 8

    collisions = {"left": False, "right": False, "top": False, "bottom": False}

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
    """コインのタイルマップをコインの位置リストに変換する関数

    Args:
        tilemap_id (int): コインのタイルマップID (default: 7)

    Returns:
        list[tuple[int, int]]: ピクセル座標のコイン位置リスト [(x, y), ...]
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
            if col != 0:  # Non-zero means coin placement
                # Convert tile coordinates to pixel coordinates
                pixel_x = x * 8
                pixel_y = y * 8
                coin_positions.append((pixel_x, pixel_y))

    return coin_positions


def check_intersection_rect(
    pos1: Position2D, body1: RectRigidBody, pos2: Position2D, body2: RectRigidBody
):
    """長方形同士の交差をチェックする関数

    Args:
        pos1 (Position2D): オブジェクト1の位置
        body1 (RectRigidBody): オブジェクト1のボディ
        pos2 (Position2D): オブジェクト2の位置
        body2 (RectRigidBody): オブジェクト2のボディ
    """
    return (
        pos1.x + body1.width > pos2.x
        and pos1.x < pos2.x + body2.width
        and pos1.y + body1.height > pos2.y
        and pos1.y < pos2.y + body2.height
    )


def check_intersection_rect_circle(
    pos1: Position2D, body1: RectRigidBody, pos2: Position2D, body2: CircleRigidBody
):
    """長方形と円の交差をチェックする関数

    Args:
        pos1 (Position2D): 長方形の位置
        body1 (RectRigidBody): 長方形のボディ
        pos2 (Position2D): 円の位置
        body2 (CircleRigidBody): 円のボディ
    """
    center_x = pos1.x + body1.width // 2
    center_y = pos1.y + body1.height // 2
    center_x2 = pos2.x + body2.radius
    center_y2 = pos2.y + body2.radius
    margin = 1.2
    return (center_x - center_x2) ** 2 + (center_y - center_y2) ** 2 <= (body2.radius * margin) ** 2


def check_collision_rect_rect(
    pos1: Position2D, body1: RectRigidBody, pos2: Position2D, body2: RectRigidBody
):
    """長方形同士の衝突をチェックする関数

    Args:
        pos1 (Position2D): オブジェクト1の位置
        body1 (RectRigidBody): オブジェクト1のボディ
        pos2 (Position2D): オブジェクト2の位置
        body2 (RectRigidBody): オブジェクト2のボディ
    """
    collisions = {"left": False, "right": False, "top": False, "bottom": False}

    if not check_intersection_rect(pos1, body1, pos2, body2):
        return collisions

    if pos2.x <= pos1.x + body1.width <= pos2.x + body2.width:
        collisions["right"] = True
    if pos2.x <= pos1.x <= pos2.x + body2.width:
        collisions["left"] = True
    if pos2.y <= pos1.y + body1.height <= pos2.y + body2.height:
        collisions["bottom"] = True
    if pos2.y <= pos1.y <= pos2.y + body2.height:
        collisions["top"] = True
    return collisions


def check_intersection_angle(
    pos1: Position2D, body1: RectRigidBody, pos2: Position2D, body2: RectRigidBody
):
    """2つの長方形の交差角度をチェックする関数

    Args:
        pos1 (Position2D): オブジェクト1の位置
        body1 (RectRigidBody): オブジェクト1のボディ
        pos2 (Position2D): オブジェクト2の位置
        body2 (RectRigidBody): オブジェクト2のボディ
    """
    center_x1 = pos1.x + body1.width // 2
    center_y1 = pos1.y + body1.height // 2
    center_x2 = pos2.x + body2.width // 2
    center_y2 = pos2.y + body2.height // 2
    return math.atan2(center_y2 - center_y1, center_x2 - center_x1)
