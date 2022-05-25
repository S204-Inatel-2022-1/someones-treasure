# Settings
FPS = 60
RESOLUTION = WIDTH, HEIGHT = 960, 540
TILE_SIZE = 64

# Entities
STATS = {
    "player": {
        "ammo": 999,
        "attack": {
            "cooldown": 500,
            "damage": 1
        },
        "hp": 6,
        "i_frames": 500,
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
            "cooldown": 1000,
            "damage": 2
        },
        "hp": 2,
        "i_frames": 500,
        "knockback_resistance": 7,
        "range": {
            "aggression_radius": TILE_SIZE * 1,
            "vision_radius": TILE_SIZE * 10
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
        "knockback_resistance": 7,
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
            "cooldown": 1000,
            "damage": 3
        },
        "hp": 4,
        "i_frames": 500,
        "knockback_resistance": 7,
        "range": {
            "aggression_radius": TILE_SIZE * 1,
            "vision_radius": TILE_SIZE * 6
        },
        "speed": 3
    }
}

MUSIC = {
    "game_over": "audio/music/evretro_8-bit-game-over-sound-tune.wav",
    "main_loop": "audio/music/evretro_8-bit-brisk-music-loop.wav"
}

SFX = {
    "attack": {
        "player": "audio/sounds/tissman_gun1.wav",
        "rat": "audio/sounds/tissman_gun1.wav",
        "skeleton": "audio/sounds/japanyoshithegamer_8-bit-hi-hat-soft.wav",
        "slime": "audio/sounds/jeckkech_collision.wav"
    },
    "death": {
        "player": "audio/sounds/mentoslat_8-bit-death-sound.wav",
        "rat": "audio/sounds/mentoslat_8-bit-death-sound.wav",
        "skeleton": "audio/sounds/mentoslat_8-bit-death-sound.wav",
        "slime": "audio/sounds/mentoslat_8-bit-death-sound.wav"
    }
}
