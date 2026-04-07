# Rest & Camp System

The rest system in Legacy of the Fallen provides two types of recovery: **full rest** (complete recovery) and **camp rest** (scaled recovery based on food).

---

## Full Rest

A full rest completely restores all resources and clears all temporary effects.

### Effects of Full Rest:
- **HP:** Fully restored to max HP
- **Energy:** All energy types (Lust, Chaos, Heavenfire) fully restored to maximum
- **Conditions:** All transient conditions removed (buffs and debuffs)
- **Temporary HP:** Removed
- **Available Actions:** Reset (abilities with "once per rest" become usable again)

### When to Use:
Full rest is used after combat or in safe locations where complete recovery is available. It's the baseline recovery for the game.

```
character.rest()  # Triggers a full rest
```

---

## Camp Rest

Camp rest is a partial recovery system that scales based on available food. It allows gradual resource recovery during exploration or in dangerous areas where full rest isn't possible.

### How Camp Rest Works:

Camp rest restores resources based on a **calorie ratio** (0.0 to 1.0), where 1.0 represents 1000 kcal of food:

- **Calorie Ratio 0.0** (no food): Only conditions/actions reset; no HP or energy recovery
- **Calorie Ratio 1.0** (full meal): Maximum recovery (50% HP, 25% energy per type)
- **Values in between** (0.0–1.0): Scaled recovery

### Recovery Formula:

| Resource | Maximum Restore | Calculation |
|----------|-----------------|-------------|
| HP | 50% of max | `old_hp + (max_hp × 0.50 × ratio)` |
| Lust Energy | 25% of max | `old_lust + (max_lust × 0.25 × ratio)` |
| Chaos Energy | 25% of max | `old_chaos + (max_chaos × 0.25 × ratio)` |
| Heavenfire Energy | 25% of max | `old_heavenfire + (max_heavenfire × 0.25 × ratio)` |

### Always Restored:
- All transient conditions cleared
- Temporary HP removed
- Available actions reset (once-per-rest abilities become usable)

### When to Use:
Camp rest is used during exploration, when resting in camps, or when you need partial recovery without a full safe rest.

```python
character.rest_at_camp(calorie_ratio)  # 0.0 = no food, 1.0 = full meal
```

### Examples:

**No food (0.0):**
```
character.rest_at_camp(0.0)
# Output: Rests at camp (0% ration): +0 HP restored.
# Conditions cleared, actions reset, but no resource recovery.
```

**Half ration (0.5):**
```
character.rest_at_camp(0.5)
# Output: Rests at camp (50% ration): +25 HP restored (example).
# Recovery scales: 25% of 50% = 12.5% max HP, 12.5% of 25% = 6.25% max energy, etc.
```

**Full meal (1.0):**
```
character.rest_at_camp(1.0)
# Output: Rests at camp (100% ration): +50 HP restored (example).
# Maximum recovery: 50% HP, 25% of each energy type.
```

---

## Rest Mechanics in Combat

After leveling up, your character must call `rest()` to recalculate derived stats:
- Hit points (HP)
- Energy pools

Failing to rest after a level-up will result in stale stat calculations. Always rest after leveling!

```python
character.level_up()
character.rest()  # Recalculate HP and energy
```

---

## Summary

| Type | Usage | HP Restore | Energy Restore | Clears Conditions |
|------|-------|-----------|----------------|--------------------|
| **Full Rest** | Safe location | 100% | 100% | ✓ |
| **Camp Rest** | Exploration | 0–50% | 0–25% each | ✓ |

Choose the right rest type based on your situation: use full rest in safe zones and camp rest with food during exploration for resource management and risk/reward gameplay.
