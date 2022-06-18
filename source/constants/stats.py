'''
Contains the statistics of in-game entities.
'''
from source.constants.settings import TILE_SIZE

STATS = {
    "player": {
        "ammo": 16,
        "attack": {
            "cooldown": 750,
            "damage": 1,
            "type": "ranged"
        },
        "hp": 6,
        "i_frames": 750,
        "knockback_resistance": 7,
        "range": {
            "aggression_radius": None,
            "vision_radius": None
        },
        "speed": 5
    },
    "ghost": {
        "ammo": None,
        "attack": {
            "cooldown": 2000,
            "damage": 2,
            "type": "melee"
        },
        "hp": 1,
        "i_frames": 500,
        "knockback_resistance": 7,
        "range": {
            "aggression_radius": TILE_SIZE * 1,
            "vision_radius": TILE_SIZE * 6
        },
        "speed": 3
    },
    "skeleton": {
        "ammo": None,
        "attack": {
            "cooldown": 1000,
            "damage": 2,
            "type": "ranged"
        },
        "hp": 3,
        "i_frames": 500,
        "knockback_resistance": 7,
        "range": {
            "aggression_radius": TILE_SIZE * 4,
            "vision_radius": TILE_SIZE * 6
        },
        "speed": 4
    },
    "slime": {
        "ammo": None,
        "attack": {
            "cooldown": 1500,
            "damage": 1,
            "type": "melee"
        },
        "hp": 2,
        "i_frames": 500,
        "knockback_resistance": 7,
        "range": {
            "aggression_radius": TILE_SIZE * 1,
            "vision_radius": TILE_SIZE * 4
        },
        "speed": 2
    },
    "rat": {
        "ammo": None,
        "attack": {
            "cooldown": 1500,
            "damage": 2,
            "type": "ranged"
        },
        "hp": 3,
        "i_frames": 500,
        "knockback_resistance": 7,
        "range": {
            "aggression_radius": TILE_SIZE * 4,
            "vision_radius": TILE_SIZE * 6
        },
        "speed": 4
    }
}
