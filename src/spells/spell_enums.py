class Aspect:
    EARTH = '^'
    WATER = '~'
    SHOCK = '!'
    FIRE = '*'
    DARK = 'G'
    LIGHT = 'A'
    MYSTIC = '%'

class Range:
    SELF = '@'
    TARGET = 'X'
    ROOM = 'O'
    WORLD = '_'

class Effect:
    FIRST = '.'
    SECOND = ':'
    THIRD = ','
    FOURTH = ';'
    FIFTH = ']'

class Duration:
    # OPTIONAL, DEFAULTS TO SHORT
    INSTANT = '1'
    SHORT = '`'
    MEDIUM = '3'
    LONG = 'M'

class Intensity:
    # OPTIONAL, DEFAULTS TO LOW
    LOW = '-'
    MEDIUM = '='
    HIGH = '+'
    INSANE = '#'

aspects = {
    '^': Aspect.EARTH,
    '~': Aspect.WATER,
    '!': Aspect.SHOCK,
    '*': Aspect.FIRE,
    'G': Aspect.DARK,
    'A': Aspect.LIGHT,
    '%': Aspect.MYSTIC
}

ranges = {
    '@': Range.SELF,
    'X': Range.TARGET,
    'O': Range.ROOM,
    '_': Range.WORLD
}

effects = {
    '.': Effect.FIRST,
    ':': Effect.SECOND,
    ',': Effect.THIRD,
    ';': Effect.FOURTH,
    ']': Effect.FIFTH
}

durations = {
    '1': Duration.INSTANT,
    '`': Duration.SHORT,
    '3': Duration.MEDIUM,
    'M': Duration.LONG
}

intensities = {
    '-': Intensity.LOW,
    '=': Intensity.MEDIUM,
    '+': Intensity.HIGH,
    '#': Intensity.INSANE,
}
# sets you on fire for a little bit just a lil
# *@.`-

# sets someone else on fire a lot for a medium amount of time
# *X.3+