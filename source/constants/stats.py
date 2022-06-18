'''
Contains the statistics of in-game entities.
'''
from source.constants.settings import TILE_SIZE

STATS = {
    "player": {
        "ammo": {
            "current": None,
            "max": 16
        },
        "attack": {
            "cooldown": 750,
            "damage": 1,
            "type": "ranged"
        },
        "health": {
            "current": None,
            "max": 6
        },
        "i_frames": 750,
        "knockback_resistance": 7,
        "range": {
            "aggression_radius": None,
            "vision_radius": None
        },
        "speed": 5
    },
    "ghost": {
        "ammo": {
            "current": None,
            "max": None
        },
        "attack": {
            "cooldown": 2000,
            "damage": 2,
            "type": "melee"
        },
        "health": {
            "current": None,
            "max": 1
        },
        "i_frames": 500,
        "knockback_resistance": 7,
        "range": {
            "aggression_radius": TILE_SIZE * 1,
            "vision_radius": TILE_SIZE * 6
        },
        "speed": 3
    },
    "skeleton": {
        "ammo": {
            "current": None,
            "max": None
        },
        "attack": {
            "cooldown": 1000,
            "damage": 2,
            "type": "ranged"
        },
        "health": {
            "current": None,
            "max": 2
        },
        "i_frames": 500,
        "knockback_resistance": 7,
        "range": {
            "aggression_radius": TILE_SIZE * 4,
            "vision_radius": TILE_SIZE * 6
        },
        "speed": 4
    },
    "slime": {
        "ammo": {
            "current": None,
            "max": None
        },
        "attack": {
            "cooldown": 1500,
            "damage": 1,
            "type": "melee"
        },
        "health": {
            "current": None,
            "max": 2
        },
        "i_frames": 500,
        "knockback_resistance": 7,
        "range": {
            "aggression_radius": TILE_SIZE * 1,
            "vision_radius": TILE_SIZE * 4
        },
        "speed": 2
    },
    "rat": {
        "ammo": {
            "current": None,
            "max": None
        },
        "attack": {
            "cooldown": 1500,
            "damage": 2,
            "type": "ranged"
        },
        "health": {
            "current": None,
            "max": 3
        },
        "i_frames": 500,
        "knockback_resistance": 7,
        "range": {
            "aggression_radius": TILE_SIZE * 4,
            "vision_radius": TILE_SIZE * 6
        },
        "speed": 4
    }
}
