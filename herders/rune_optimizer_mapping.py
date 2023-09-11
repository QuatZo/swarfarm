from bestiary.models import Monster
from herders.models import base, RuneInstance, RuneCraftInstance, ArtifactInstance, ArtifactCraftInstance

type_encode_dict = {
    RuneInstance.TYPE_ENERGY: 'Energy',
    RuneInstance.TYPE_FATAL: 'Fatal',
    RuneInstance.TYPE_BLADE: 'Blade',
    RuneInstance.TYPE_RAGE: 'Rage',
    RuneInstance.TYPE_SWIFT: 'Swift',
    RuneInstance.TYPE_FOCUS: 'Focus',
    RuneInstance.TYPE_GUARD: 'Guard',
    RuneInstance.TYPE_ENDURE: 'Endure',
    RuneInstance.TYPE_VIOLENT: 'Violent',
    RuneInstance.TYPE_WILL: 'Will',
    RuneInstance.TYPE_NEMESIS: 'Nemesis',
    RuneInstance.TYPE_SHIELD: 'Shield',
    RuneInstance.TYPE_REVENGE: 'Revenge',
    RuneInstance.TYPE_DESPAIR: 'Despair',
    RuneInstance.TYPE_VAMPIRE: 'Vampire',
    RuneInstance.TYPE_DESTROY: 'Destroy',
    RuneInstance.TYPE_FIGHT: 'Fight',
    RuneInstance.TYPE_DETERMINATION: 'Determination',
    RuneInstance.TYPE_ENHANCE: 'Enhance',
    RuneInstance.TYPE_ACCURACY: 'Accuracy',
    RuneInstance.TYPE_TOLERANCE: 'Tolerance',
}

stat_encode_dict = {
    RuneInstance.STAT_HP: 'HP flat',
    RuneInstance.STAT_HP_PCT: 'HP%',
    RuneInstance.STAT_DEF: 'DEF flat',
    RuneInstance.STAT_DEF_PCT: 'DEF%',
    RuneInstance.STAT_ATK: 'ATK flat',
    RuneInstance.STAT_ATK_PCT: 'ATK%',
    RuneInstance.STAT_SPD: 'SPD',
    RuneInstance.STAT_CRIT_RATE_PCT: 'CRate',
    RuneInstance.STAT_CRIT_DMG_PCT: 'CDmg',
    RuneInstance.STAT_RESIST_PCT: 'RES',
    RuneInstance.STAT_ACCURACY_PCT: 'ACC',
}

type_decode_dict = {
    'Energy': RuneInstance.TYPE_ENERGY,
    'Fatal': RuneInstance.TYPE_FATAL,
    'Blade': RuneInstance.TYPE_BLADE,
    'Rage': RuneInstance.TYPE_RAGE,
    'Swift': RuneInstance.TYPE_SWIFT,
    'Focus': RuneInstance.TYPE_FOCUS,
    'Guard': RuneInstance.TYPE_GUARD,
    'Endure': RuneInstance.TYPE_ENDURE,
    'Violent': RuneInstance.TYPE_VIOLENT,
    'Will': RuneInstance.TYPE_WILL,
    'Nemesis': RuneInstance.TYPE_NEMESIS,
    'Shield': RuneInstance.TYPE_SHIELD,
    'Revenge': RuneInstance.TYPE_REVENGE,
    'Despair': RuneInstance.TYPE_DESPAIR,
    'Vampire': RuneInstance.TYPE_VAMPIRE,
    'Destroy': RuneInstance.TYPE_DESTROY,
    'Fight': RuneInstance.TYPE_FIGHT,
    'Determination': RuneInstance.TYPE_DETERMINATION,
    'Enhance': RuneInstance.TYPE_ENHANCE,
    'Accuracy': RuneInstance.TYPE_ACCURACY,
    'Tolerance': RuneInstance.TYPE_TOLERANCE,
}

stat_decode_dict = {
    'HP flat': RuneInstance.STAT_HP,
    'HP%': RuneInstance.STAT_HP_PCT,
    'DEF flat': RuneInstance.STAT_DEF,
    'DEF%': RuneInstance.STAT_DEF_PCT,
    'ATK flat': RuneInstance.STAT_ATK,
    'ATK%': RuneInstance.STAT_ATK_PCT,
    'SPD': RuneInstance.STAT_SPD,
    'CRate': RuneInstance.STAT_CRIT_RATE_PCT,
    'CDmg': RuneInstance.STAT_CRIT_DMG_PCT,
    'RES': RuneInstance.STAT_RESIST_PCT,
    'ACC': RuneInstance.STAT_ACCURACY_PCT,
}

element_map = {
    Monster.ELEMENT_WATER: 1,
    Monster.ELEMENT_FIRE: 2,
    Monster.ELEMENT_WIND: 3,
    Monster.ELEMENT_LIGHT: 4,
    Monster.ELEMENT_DARK: 5,
}

rune_set_map = {
    RuneInstance.TYPE_ENERGY: 1,
    RuneInstance.TYPE_GUARD: 2,
    RuneInstance.TYPE_SWIFT: 3,
    RuneInstance.TYPE_BLADE: 4,
    RuneInstance.TYPE_RAGE: 5,
    RuneInstance.TYPE_FOCUS: 6,
    RuneInstance.TYPE_ENDURE: 7,
    RuneInstance.TYPE_FATAL: 8,
    RuneInstance.TYPE_DESPAIR: 10,
    RuneInstance.TYPE_VAMPIRE: 11,
    RuneInstance.TYPE_VIOLENT: 13,
    RuneInstance.TYPE_NEMESIS: 14,
    RuneInstance.TYPE_WILL: 15,
    RuneInstance.TYPE_SHIELD: 16,
    RuneInstance.TYPE_REVENGE: 17,
    RuneInstance.TYPE_DESTROY: 18,
    RuneInstance.TYPE_FIGHT: 19,
    RuneInstance.TYPE_DETERMINATION: 20,
    RuneInstance.TYPE_ENHANCE: 21,
    RuneInstance.TYPE_ACCURACY: 22,
    RuneInstance.TYPE_TOLERANCE: 23,
    RuneInstance.TYPE_SEAL: 24,
    RuneInstance.TYPE_INTANGIBLE: 25,
}

rune_stat_type_map = {
    RuneInstance.STAT_HP: 1,
    RuneInstance.STAT_HP_PCT: 2,
    RuneInstance.STAT_ATK: 3,
    RuneInstance.STAT_ATK_PCT: 4,
    RuneInstance.STAT_DEF: 5,
    RuneInstance.STAT_DEF_PCT: 6,
    RuneInstance.STAT_SPD: 8,
    RuneInstance.STAT_CRIT_RATE_PCT: 9,
    RuneInstance.STAT_CRIT_DMG_PCT: 10,
    RuneInstance.STAT_RESIST_PCT: 11,
    RuneInstance.STAT_ACCURACY_PCT: 12,
}

quality_map = {
    base.Quality.QUALITY_NORMAL: 1,
    base.Quality.QUALITY_MAGIC: 2,
    base.Quality.QUALITY_RARE: 3,
    base.Quality.QUALITY_HERO: 4,
    base.Quality.QUALITY_LEGEND: 5,
}

craft_type_map = {
    RuneCraftInstance.CRAFT_ENCHANT_GEM: 1,
    RuneCraftInstance.CRAFT_GRINDSTONE: 2,
    RuneCraftInstance.CRAFT_IMMEMORIAL_GEM: 3,
    RuneCraftInstance.CRAFT_IMMEMORIAL_GRINDSTONE: 4,
    RuneCraftInstance.CRAFT_ANCIENT_GEM: 5,
    RuneCraftInstance.CRAFT_ANCIENT_GRINDSTONE: 6,
}

artifact_type_map = {
    ArtifactInstance.SLOT_ELEMENTAL: 1,
    ArtifactInstance.SLOT_ARCHETYPE: 2,
}

artifact_main_stat_map = {
    ArtifactInstance.STAT_HP: 100,
    ArtifactInstance.STAT_ATK: 101,
    ArtifactInstance.STAT_DEF: 102,
}

artifact_effect_map = {
    ArtifactInstance.EFFECT_ATK_LOST_HP: 200,
    ArtifactInstance.EFFECT_DEF_LOST_HP: 201,
    ArtifactInstance.EFFECT_SPD_LOST_HP: 202,
    ArtifactInstance.EFFECT_SPD_INABILITY: 203,
    ArtifactInstance.EFFECT_ATK: 204,
    ArtifactInstance.EFFECT_DEF: 205,
    ArtifactInstance.EFFECT_SPD: 206,
    ArtifactInstance.EFFECT_CRIT_RATE: 207,
    ArtifactInstance.EFFECT_COUNTER_DMG: 208,
    ArtifactInstance.EFFECT_COOP_ATTACK_DMG: 209,
    ArtifactInstance.EFFECT_BOMB_DMG: 210,
    ArtifactInstance.EFFECT_REFLECT_DMG: 211,
    ArtifactInstance.EFFECT_CRUSHING_HIT_DMG: 212,
    ArtifactInstance.EFFECT_DMG_RECEIVED_INABILITY: 213,
    ArtifactInstance.EFFECT_CRIT_DMG_RECEIVED: 214,
    ArtifactInstance.EFFECT_LIFE_DRAIN: 215,
    ArtifactInstance.EFFECT_HP_REVIVE: 216,
    ArtifactInstance.EFFECT_ATB_REVIVE: 217,
    ArtifactInstance.EFFECT_DMG_PCT_OF_HP: 218,
    ArtifactInstance.EFFECT_DMG_PCT_OF_ATK: 219,
    ArtifactInstance.EFFECT_DMG_PCT_OF_DEF: 220,
    ArtifactInstance.EFFECT_DMG_PCT_OF_SPD: 221,
    ArtifactInstance.EFFECT_CRIT_DMG_UP_ENEMY_HP_GOOD: 222,
    ArtifactInstance.EFFECT_CRIT_DMG_UP_ENEMY_HP_BAD: 223,
    ArtifactInstance.EFFECT_CRIT_DMG_SINGLE_TARGET: 224,
    ArtifactInstance.EFFECT_DMG_TO_FIRE: 300,
    ArtifactInstance.EFFECT_DMG_TO_WATER: 301,
    ArtifactInstance.EFFECT_DMG_TO_WIND: 302,
    ArtifactInstance.EFFECT_DMG_TO_LIGHT: 303,
    ArtifactInstance.EFFECT_DMG_TO_DARK: 304,
    ArtifactInstance.EFFECT_DMG_FROM_FIRE: 305,
    ArtifactInstance.EFFECT_DMG_FROM_WATER: 306,
    ArtifactInstance.EFFECT_DMG_FROM_WIND: 307,
    ArtifactInstance.EFFECT_DMG_FROM_LIGHT: 308,
    ArtifactInstance.EFFECT_DMG_FROM_DARK: 309,
    ArtifactInstance.EFFECT_SK1_CRIT_DMG: 400,
    ArtifactInstance.EFFECT_SK2_CRIT_DMG: 401,
    ArtifactInstance.EFFECT_SK3_CRIT_DMG: 402,
    ArtifactInstance.EFFECT_SK4_CRIT_DMG: 403,
    ArtifactInstance.EFFECT_SK1_RECOVERY: 404,
    ArtifactInstance.EFFECT_SK2_RECOVERY: 405,
    ArtifactInstance.EFFECT_SK3_RECOVERY: 406,
    ArtifactInstance.EFFECT_SK1_ACCURACY: 407,
    ArtifactInstance.EFFECT_SK2_ACCURACY: 408,
    ArtifactInstance.EFFECT_SK3_ACCURACY: 409,
}

archetype_map = {
    base.Archetype.ARCHETYPE_ATTACK: 1,
    base.Archetype.ARCHETYPE_DEFENSE: 2,
    base.Archetype.ARCHETYPE_HP: 3,
    base.Archetype.ARCHETYPE_SUPPORT: 4,
    base.Archetype.ARCHETYPE_MATERIAL: 5,
}

