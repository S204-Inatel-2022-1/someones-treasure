# Settings
FPS = 60
RESOLUTION = WIDTH, HEIGHT = 960, 540
TILE_SIZE = 64

# Entities
STATS = {
    "player": {
        "ammo": 16,
        "attack": {
            "cooldown": 500,
            "damage": 1
        },
        "hp": 6,
        "i_frames": 500,
        "knockback_resistance:": 7,
        "range": {
            "aggression": None,
            "vision": None
        },
        "speed": 5
    },
    "ghost": {
        "ammo": None,
        "attack": {
            "cooldown": 1000,
            "damage": 2
        },
        "hp": 2,
        "i_frames": 500,
        "knockback_resistance:": 7,
        "range": {
            "aggression": TILE_SIZE * 1,
            "vision": TILE_SIZE * 10
        },
        "speed": 10
    },
    "skeleton": {
        "ammo": None,
        "attack": {
            "cooldown": 1000,
            "damage": 3
        },
        "hp": 4,
        "i_frames": 500,
        "knockback_resistance:": 7,
        "range": {
            "aggression_radius": TILE_SIZE * 1,
            "vision_radius": TILE_SIZE * 6
        },
        "speed": 7
    },
    "slime": {
        "ammo": None,
        "attack": {
            "cooldown": 500,
            "damage": 1
        },
        "hp": 6,
        "i_frames": 500,
        "knockback_resistance:": 7,
        "range": {
            "aggression": TILE_SIZE * 1,
            "vision": TILE_SIZE * 4
        },
        "speed": 2
    },
    "rat": {
        "ammo": None,
        "attack": {
            "cooldown": 1000,
            "damage": 3
        },
        "hp": 4,
        "i_frames": 500,
        "knockback_resistance:": 7,
        "range": {
            "aggression_radius": TILE_SIZE * 1,
            "vision_radius": TILE_SIZE * 6
        },
        "speed": 7
    },
}
