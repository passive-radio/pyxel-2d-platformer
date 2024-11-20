from pigframe import *
from dataclasses import dataclass
import math

@dataclass
class BaseCollidable:
    """衝突判定を行うオブジェクト"""
    pass

@dataclass
class TileCollidable:
    """タイルの衝突判定を行うオブジェクト"""
    surface_height: int = None

@dataclass
class RectRigidBody:
    """長方形で衝突判定を行うオブジェクト"""
    width: int
    height: int
    flip_x: bool = False

@dataclass
class CollisionInfo:
    """衝突情報を持つオブジェクト"""
    left: bool = False
    right: bool = False
    top: bool = False
    bottom: bool = False

@dataclass
class Movable:
    """移動可能なオブジェクト"""
    speed: float = 1.0
    jump_power: int = 2
@dataclass
class Base2DPhysicsQuantity:
    """2次元物理量を持つオブジェクト"""
    x: int
    y: int
    next_x: int = 0
    next_y: int = 0
    prev_x: int = 0
    prev_y: int = 0
    
    def __add__(self, other):
        return Base2DPhysicsQuantity(self.x + other.x, self.y + other.y)
    
    def __sub__(self, other):
        return Base2DPhysicsQuantity(self.x - other.x, self.y - other.y)
    
    def __mul__(self, other):
        return Base2DPhysicsQuantity(self.x * other, self.y * other)
    
    def __truediv__(self, other):
        return Base2DPhysicsQuantity(self.x / other, self.y / other)
    
    def size(self):
        return math.sqrt(self.x ** 2 + self.y ** 2)
    
    def normalize(self):
        size = self.size()
        return Base2DPhysicsQuantity(self.x / size, self.y / size)
    
    def dot(self, other):
        return self.x * other.x + self.y * other.y
    
    def cross(self, other):
        return self.x * other.y - self.y * other.x

@dataclass
class Position2D(Base2DPhysicsQuantity):
    """2次元座標を持つオブジェクト"""
    
    def __add__(self, other):
        result = super().__add__(other)
        return Position2D(result.x, result.y)
    
    def __sub__(self, other):
        result = super().__sub__(other)
        return Position2D(result.x, result.y)
    
    def __mul__(self, other):
        result = super().__mul__(other)
        return Position2D(result.x, result.y)
    
    def __truediv__(self, other):
        result = super().__truediv__(other)
        return Position2D(result.x, result.y)
    
    def size(self):
        result = super().size()
        return result
    
    def normalize(self):
        result = super().normalize()
        return Position2D(result.x, result.y)
    
    def dot(self, other):
        result = super().dot(other)
        return result
    
    def cross(self, other):
        result = super().cross(other)
        return result

@dataclass
class Velocity2D(Base2DPhysicsQuantity):
    """2次元速度を持つオブジェクト"""
    
    def __add__(self, other):
        result = super().__add__(other)
        return Velocity2D(result.x, result.y)
    
    def __sub__(self, other):
        result = super().__sub__(other)
        return Velocity2D(result.x, result.y)
    
    def __mul__(self, other):
        result = super().__mul__(other)
        return Velocity2D(result.x, result.y)
    
    def __truediv__(self, other):
        result = super().__truediv__(other)
        return Velocity2D(result.x, result.y)
    
    def size(self):
        result = super().size()
        return result
    
    def normalize(self):
        result = super().normalize()
        return Velocity2D(result.x, result.y)
    
    def dot(self, other):
        result = super().dot(other)
        return result
    
    def cross(self, other):
        result = super().cross(other)
        return result

@dataclass
class TileMap:
    """タイルマップを持つオブジェクト"""
    id: int
    pixel_size: int = 8

@dataclass
class Player:
    """プレイヤーを表すオブジェクト"""
    pass

@dataclass
class Animation:
    """アニメーション情報を持つオブジェクト"""
    frame: int = 0
    timer: int = 0
    is_running: bool = False
    is_jumping: bool = False
    is_falling: bool = False
    is_crouching: bool = False
    sprite_x: int = 0
    sprite_y: int = 8*11  # Default idle position

@dataclass
class GoalMarkerTileMap:
    """ゴールマーカーを表すオブジェクト"""
    id: int
    pixel_size: int = 8
    
@dataclass
class StageState:
    """ステージの状態を表すオブジェクト"""
    is_goal: bool = False
    game_over: bool = False
    id: int = 0
    time_remaining: float = 60.0

@dataclass
class Enemy:
    """敵を表すオブジェクト"""
    species_id: int

@dataclass
class EnemyState:
    """敵の状態を表すオブジェクト"""
    is_dead: bool = False
    
@dataclass
class EnemyAnimation:
    """敵のアニメーション情報を持つオブジェクト"""
    frame: int = 0
    timer: int = 0
    is_running: bool = False
    sprite_x: int = 0
    sprite_y: int = 8*7
    
@dataclass
class MoveMethodWalk:
    """歩く敵を表すオブジェクト"""
    pass

if __name__ == "__main__":
    v1 = Velocity2D(3, 4)
    v2 = Velocity2D(6, 8)
    v3 = v1 + v2 
    print(v3.size())
    print(v3.normalize())