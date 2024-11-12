# Feature toggles
FEATURES = {
    "enable_spin": True,
    "enable_stake": True,
    "enable_combo": True
}

# Mining upgrade configurations
MINING_CONFIG = {
    "farmer": {
        "enabled": True, #no 4
        "max_level": 10
    },
    "beehive": {
        "enabled": True, #no 3
        "max_level": 10
    },
    "bee": {
        "enabled": True, #no 2
        "max_level": 20
    },
    "honey": {
        "enabled": True, #no 1 (cheap one)
        "max_level": 50
    }
}

UPGRADE_SEQUENCE = ["farmer", "beehive", "bee", "honey"]