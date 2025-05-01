enum Aspect
{
    ^ = Earth
    ~ = Water
    ! = Shock/Lightning
    * = Fire
    % = Mystic
}

enum Range
{
    S = Self
    T = Target
    R = Room
    W = World
}

enum Effect
{
    1 = effect 1
    2 = effect 2
}

enum EffectModifiers

enum EarthEffect
{
    1 = Earthquake
}

class Spell
{
    Aspect aspect;
    Range range;
    Effect primaryEffect;
    Effect secondaryEffect;
}

{
    "name1": {
        "name": "name1",
        "description": "blah blah blah",
        "runes": "abcdefg"
    }
}
Name|Description|Runes
Name|Description|Runes
Name|Description|Runes
Name|Description|Runes
Name|Description|Runes