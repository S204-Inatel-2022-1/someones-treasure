# Settings
FPS = 60
RESOLUTION = WIDTH, HEIGHT = 1280, 720
TILE_SIZE = 64

# Entity Stats
STATS = {
    "player": {
        "ammo": 16,
        "attack": {
            "cooldown": 500,
            "damage": 1,
            "type": "ranged"
        },
        "hp": 6,
        "i_frames": 1000,
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
        "i_frames": 1000,
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
        "i_frames": 1000,
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
        "i_frames": 1000,
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
            "damage": 2,
            "type": "ranged"
        },
        "hp": 3,
        "i_frames": 1000,
        "knockback_resistance": 7,
        "range": {
            "aggression_radius": TILE_SIZE * 4,
            "vision_radius": TILE_SIZE * 6
        },
        "speed": 4
    }
}

# Music
MUSIC = {
    "game_over": "audio/music/evretro_8-bit-game-over-sound-tune.wav",
    "main_loop": "audio/music/evretro_8-bit-brisk-music-loop.wav"
}

# Sound Effects
SFX = {
    "attack": {
        "player": "audio/sounds/tissman_gun1.wav",
        "rat": "audio/sounds/tissman_gun1.wav",
        "ghost": "audio/sounds/japanyoshithegamer_8-bit-hi-hat-soft.wav",
        "skeleton": "audio/sounds/japanyoshithegamer_8-bit-hi-hat-soft.wav",
        "slime": "audio/sounds/jeckkech_collision.wav"
    },
    "death": {
        "player": "audio/sounds/mentoslat_8-bit-death-sound.wav",
        "rat": "audio/sounds/mentoslat_8-bit-death-sound.wav",
        "ghost": "audio/sounds/mentoslat_8-bit-death-sound.wav",
        "skeleton": "audio/sounds/mentoslat_8-bit-death-sound.wav",
        "slime": "audio/sounds/mentoslat_8-bit-death-sound.wav"
    },
    "misc": {
        "break": "audio/sounds/japanyoshithegamer_8-bit-hi-hat-soft.wav"
    }
}
