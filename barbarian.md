# Barbarian Class Guide

**Versions:** every feature is tagged with the first game version it shipped in. *0.3.6+* means it was already in 0.3.6 or earlier.

The Barbarian is a Strength/Constitution-based melee class built around Rage. While raging they hit harder, resist physical damage, and can layer elemental damage through Storm Herald abilities. They have strong survivability tools and snowball significantly in the late game.

---

## Level Features

These are automatically granted at the listed level.

| Level | Icon | Feature | Since |
|-------|------|---------|-------|
| 1 | ![Rage](assets/rage_icon.webp) | Rage | 0.3.6+ |
| 2 | ![Reckless Attack](assets/reckless_icon.webp) ![Always Ready](assets/danger_sense_icon.webp) | Reckless Attack + Always Ready | 0.3.6+ |
| 5 | ![Extra Attack](assets/extra_attack_icon.webp) | Extra Attack | 0.3.6+ |
| 7 | ![Primal Instinct](assets/feral_instinct_icon.webp) | Primal Instinct | 0.3.6+ |
| 9 | ![Enhanced Critical](assets/brutal_critical_icon.webp) | Enhanced Critical | 0.3.6+ |
| 11 | ![Death Warding Rage](assets/relentless_rage_icon.webp) | Death Warding Rage | 0.3.6+ |
| 18 | ![Indomitable Might](assets/indomitable_might_icon.webp) | Indomitable Might | 0.3.6+ |
| 20 | ![Unrivaled Ability](assets/primal_champion_icon.webp) | Unrivaled Ability | 0.3.6+ |

### ![](assets/rage_icon.webp) Rage *(L1 — No energy, self-target · 0.3.6+)*
Enter a barbarian rage for **10 turns**, gaining:
- **+2 bonus damage** on all attacks
- **Resistance to bludgeoning, piercing, and slashing damage**
- **Advantage on Strength checks and saving throws**

### ![](assets/reckless_icon.webp) Reckless Attack *(L2 — Melee · 0.3.6+)*
Attack with abandon. Gain advantage on melee attack rolls this turn but **grant advantage to all attackers against you** until your next turn. Deals weapon damage + Strength modifier. **Melee weapon only** *(0.6.1+)*: greyed out while a bow or firearm is equipped.

### ![](assets/danger_sense_icon.webp) Always Ready *(L2 — Passive · 0.3.6+)*
Permanent **advantage on Dexterity saving throws** against traps, spells, and visible effects.

### ![](assets/extra_attack_icon.webp) Extra Attack *(L5 · 0.3.6+)*
Passive. Grants **1 extra attack** per turn.

### ![](assets/feral_instinct_icon.webp) Primal Instinct *(L7 — Passive · 0.3.6+)*
Permanent **advantage on initiative rolls**. You almost always act first.

### ![](assets/brutal_critical_icon.webp) Enhanced Critical *(L9 — Passive · 0.3.6+)*
Critical strikes deal extra damage dice:
- Levels 9–12: **+1 extra damage die**
- Levels 13–16: **+2 extra damage dice**
- Level 17+: **+3 extra damage dice**

### ![](assets/relentless_rage_icon.webp) Death Warding Rage *(L11 — Passive · 0.3.6+)*
Once per rage, when you would drop to 0 HP, you drop to **1 HP instead** (requires at least 1 HP remaining).

### ![](assets/indomitable_might_icon.webp) Indomitable Might *(L18 — Passive · 0.3.6+)*
When making a Strength check, you may use your **Strength score itself** instead of the dice roll if it's higher.

### ![](assets/primal_champion_icon.webp) Unrivaled Ability *(L20 — Passive · 0.3.6+)*
Permanently increases **Strength and Constitution by 4**, with an ability score cap of 24.

---

## Level Options

### ![](assets/taunting_icon.webp) Taunt *(L2+, No energy · 0.3.6+)*
Challenge all enemies, forcing them to target you for **3 turns**. Use this to protect squishier allies or to set up defensive plays while raging.

---

## Storm Herald — Affinity Options *(L6+, Affinity-Gated)*

Unlocked at level 6 if you have the matching affinity. Active only **while raging**.

| Affinity | Icon | Ability | Effect | Since |
|----------|------|---------|--------|-------|
| Heavenfire | ![](assets/storm_melee_heat_icon.webp) | Storm Melee: Heat | Melee attacks deal extra **1d6 heat** damage (2d6 at L14+). | 0.3.6+ |
| Lust | ![](assets/storm_melee_cold_icon.webp) | Storm Melee: Cold | Melee attacks deal extra **1d6 cold** damage (2d6 at L14+) and may **Slow** target (Con save). | 0.3.6+ |
| Chaos | ![](assets/storm_melee_poison_icon.webp) | Storm Melee: Poison | Melee attacks deal extra **1d6 poison** damage (2d6 at L14+) and may **Poison** target (Con save). | 0.3.6+ |

---

## Storm Herald — Aura Options *(L14+, Affinity-Gated)*

Unlocked at level 14 if you have the matching affinity. Active only **while raging**.

| Affinity | Icon | Ability | Effect | Since |
|----------|------|---------|--------|-------|
| Heavenfire | ![](assets/storm_aura_heat_icon.webp) | Storm Aura: Heat | Enemies with highest initiative take **1d6 heat** damage per turn (2d6 at L17+); all allies gain heat resistance. | 0.3.6+ |
| Lust | ![](assets/storm_aura_cold_icon.webp) | Storm Aura: Cold | Enemies with highest initiative take **1d6 cold** damage per turn (2d6 at L17+), may Slow; all allies gain cold resistance. | 0.3.6+ |
| Chaos | ![](assets/storm_aura_poison_icon.webp) | Storm Aura: Poison | Enemies with highest initiative take **1d6 poison** damage per turn (2d6 at L17+), may Poison; all allies gain poison resistance. | 0.3.6+ |

---

## Storm Herald Feats *(Feat Levels 4, 8, 12, 16)*

Barbarian-specific feats available at feat levels, in addition to generic feats.

| Level | Icon | Feat | Description | Since |
|-------|------|------|-------------|-------|
| L4 | ![](assets/storm_herald_melee_heat_icon.webp) ![](assets/storm_herald_melee_cold_icon.webp) ![](assets/storm_herald_melee_poison_icon.webp) | Storm Herald Melee | Affinity-gated. Scales 1d6 → 2d6 → 3d6 → 4d6 at levels 8, 12, 16. | 0.3.6+ |
| L8 | ![](assets/storm_herald_aura_heat_icon.webp) ![](assets/storm_herald_aura_cold_icon.webp) ![](assets/storm_herald_aura_poison_icon.webp) | Storm Herald Aura | Affinity-gated. Scales 1d6 → 2d6 → 3d6 at levels 12, 16. | 0.3.6+ |
| L12/L16 | — | Re-offer | Any Storm Herald feat not yet taken is offered again. | 0.3.6+ |

The Storm Herald Feat versions scale higher than the standard level options above — if you can take them via feats, they're stronger.

---

## Tips

- **Rage before you attack.** Most of your offensive and defensive bonuses require you to be raging. Make Rage your first action.
- **Reckless Attack** is high-risk, high-reward. Use it when you have Death Warding Rage (L11) active or when you need to eliminate a target fast.
- **Taunt + Rage** is a strong combo — you draw all attacks while also resisting physical damage. Very effective for protecting party members.
- **Primal Instinct** (L7) nearly guarantees you act first. Use this to pop Rage before enemies can act.
- **Storm Herald Melee** is your primary source of elemental damage. The Chaos (poison) and Lust (cold/slow) variants add crowd control on top of damage.
- **Storm Aura** (L14+) passively damages the most dangerous enemies every turn while raging — it rewards staying in melee and prolonging fights.
- **Unrivaled Ability** (L20) caps at +4 Str/Con. Combined with the Storm Herald scaling, late-game Barbarians hit extremely hard with every swing.
- Unlike Fighters, Barbarians have more survivability tools (Death Warding Rage, passive damage resistance). You can afford to play more aggressively.
