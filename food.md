# Food & Consumables

Food items are consumable resources that provide recovery during camp rest. They are tracked by calorie content and used to enhance rest recovery outside of safe zones.

---

## Food System Overview

Food serves two purposes in Legacy of the Fallen:

1. **Camp Rest Scaling:** Food increases the `calorie_ratio` passed to `rest_at_camp()`, boosting resource recovery
2. **Consumable Items:** Can be used directly in combat or exploration for immediate effects

### Calorie Values

Food is measured in **calories (kcal)**:
- **1 kcal of food** = 0.001 calorie ratio
- **1000 kcal of food** = 1.0 calorie ratio (full meal, maximum recovery)

---

## Using Food During Camp Rest

When resting at camp, the total calories of food consumed are divided by 1000 to calculate the recovery ratio:

```
calorie_ratio = total_calories / 1000
character.rest_at_camp(calorie_ratio)
```

### Example:
- **Consume 500 kcal of food:** `rest_at_camp(0.5)` → 25% HP + 12.5% each energy
- **Consume 1000 kcal of food:** `rest_at_camp(1.0)` → 50% HP + 25% each energy
- **Consume 250 kcal of food:** `rest_at_camp(0.25)` → 12.5% HP + 6.25% each energy

---

## Consumable Items

Consumable items can be used directly during combat or exploration. Common consumables include:

### Potions
- **Minor Health Potion** — Restores **2d4+2** HP
  - Common rarity, 50 gold price
  - Icon: `minor_healing_potion_icon`

- **Minor Rejuvenation Potion** — Restores **2d4+2** HP and **2d4+2** to all energy types
  - Common rarity, 50 gold price
  - Icon: `minor_rejuvenation_potion_icon`

---

## Food Sources

Food is typically found through:
- **Hunting** in hunting areas (generates fresh meat/game)
- **Merchant purchases** (buy prepared rations)
- **Gathering** during exploration
- **Looting** from defeated enemies or locations

---

## Food Management Tips

- **Stack consumables early.** Gather food during exploration to have options during camp rest.
- **High-calorie meals are precious.** Save 1000 kcal meals for critical recovery moments.
- **Partial rations are viable.** Even 500 kcal provides meaningful recovery (25% HP + energy).
- **Know your recovery needs.** Calculate total calories needed before settling camp: `(resources_needed × 1000) / recovery_percent`.
- **Balance risk and reward.** Camp rest with food lets you press onward without returning to a safe zone — but you're exposed.

---

## Consumable Effects

All consumable items override the `consume()` method to provide custom effects:

```python
item = MinorHealthPotion()
effects = item.consume(target)
# Returns: {"heal": rolled_amount}
```

Supported effect keys:
- `heal` — Direct HP restoration
- `energy` — Energy restoration (divided equally among available pools)
- Custom effects based on item type

---

## Summary

Food is a strategic resource that:
- **Scales camp rest recovery** based on calorie consumption
- **Provides risk/reward gameplay** (rest safely vs. camp with food)
- **Encourages exploration** (hunting and gathering)
- **Enables resource management** (ration decisions during long expeditions)

Use food strategically to extend your exploration window and manage resources efficiently.
