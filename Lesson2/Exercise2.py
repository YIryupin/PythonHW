#Damage calculator
def calc_damage(base_damage: float, multiplier: float, critical: bool) -> float | str:
    if type(base_damage) not in [float, int]:
        return 'wrong types'
    if base_damage < 0 or multiplier < 0:
        return 'damage cannot be negative'
    damage = base_damage*multiplier
    if critical:
        damage = damage*2
    return damage

print(calc_damage(10, 1.5, False))
print(calc_damage(10, 1.5, True))
print(calc_damage(-1, 1.5, False))
print(calc_damage('10', 2, False))