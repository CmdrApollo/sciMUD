from spell_enums import *

complexity = {
    # Aspect complexities
    Aspect.EARTH: 1,
    Aspect.WATER: 1,
    Aspect.SHOCK: 1,
    Aspect.FIRE: 1,
    Aspect.DARK: 2,
    Aspect.LIGHT: 2,
    Aspect.MYSTIC: 3,

    # Range complexity
    Range.SELF: 1,
    Range.TARGET: 2,
    Range.ROOM: 4,
    Range.WORLD: 8,

    # Effect complexity
    Effect.FIRST: 1,
    Effect.SECOND: 1,
    Effect.THIRD: 2,
    Effect.FOURTH: 2,
    Effect.FIFTH: 3,

    # Duration complexity
    Duration.INSTANT: 1,
    Duration.SHORT: 1,
    Duration.MEDIUM: 2,
    Duration.LONG: 5,
    
    # Intensity complexity
    Intensity.LOW: 1,
    Intensity.MEDIUM: 2,
    Intensity.HIGH: 4,
    Intensity.INSANE: 8,
}