# Druid Class Guide

**Versions:** every feature is tagged with the first game version it shipped in. *0.3.6+* means it was already in 0.3.6 or earlier.

The Druid is a Wisdom caster who speaks for the land. A druid's subclass is implied by the optional features it picks at each level-up: taking the storm spells makes a **Storm Druid**, who calls sand, sleet, lightning, locusts and blizzard down on the whole enemy line. A second path, the **Shape Druid** (animal shapes with their own action sets), is planned and not in the game yet.

Storms spend **any** affinity energy you own (Lust, Chaos or Heavenfire). Their save DC is 8 + your Wisdom modifier + a quarter of your level, plus Druidic Focus and Archdruid.

---

## Level Features

These are automatically granted at the listed level.

| Level | Icon | Feature | Since |
|-------|------|---------|-------|
| 1 | ![Druidic Focus](assets/druidic_focus_icon.webp) | Druidic Focus | 0.5.4+ |
| 10 | ![Nature's Ward](assets/natures_ward_icon.webp) | Nature's Ward | 0.5.4+ |
| 20 | ![Archdruid](assets/archdruid_icon.webp) | Archdruid | 0.5.4+ |

### ![](assets/druidic_focus_icon.webp) Druidic Focus *(L1 · 0.5.4+)*
Passive. The land answers you more readily: **+1 to your spell save DC**.

### ![](assets/natures_ward_icon.webp) Nature's Ward *(L10 · 0.5.4+)*
Passive. Rot and venom are part of the cycle you serve: **you cannot be Poisoned**.

### ![](assets/archdruid_icon.webp) Archdruid *(L20 · 0.5.4+)*
Passive. The weather is yours to call: a further **+2 to your spell save DC**.

---

## Storm Druid Spells (Level Options)

Each level-up you pick one option; already-learned spells are not offered again. Every storm hits **all living enemies**.

### Level 1

| Icon | Spell | Energy | Description | Since |
|------|-------|--------|-------------|-------|
| ![](assets/sand_storm_icon.webp) | Sand Storm | 3 | 1d6 physical to every enemy. A failed **Constitution** save leaves them **Sand-Blinded** for 2 turns: disadvantage on their attacks, advantage on attacks against them (Constitution 12 each turn to clear it). | 0.5.4+ |

### Level 3

| Icon | Spell | Energy | Description | Since |
|------|-------|--------|-------------|-------|
| ![](assets/sleet_storm_icon.webp) | Sleet Storm | 5 | Every enemy makes a **Wisdom** save: Icy and Wet for 5 turns on a fail, 2 on a success. Icy: 30% chance to slip and lose a turn. Wet: double cold and lightning damage. | 0.5.4+ |

### Level 5

| Icon | Spell | Energy | Description | Since |
|------|-------|--------|-------------|-------|
| ![](assets/lightning_storm_icon.webp) | Lightning Storm | 5 | 4d8 electric to every enemy, **Dexterity** save for half. Wet targets take double. | 0.5.4+ |

### Level 7

| Icon | Spell | Energy | Description | Since |
|------|-------|--------|-------------|-------|
| ![](assets/plague_storm_icon.webp) | Plague Storm | 6 | A locust swarm: 3d6 poison to every enemy, and a failed **Constitution** save leaves them **Poisoned** for 3 turns (1d4 poison per turn). | 0.5.4+ |

### Level 9

| Icon | Spell | Energy | Description | Since |
|------|-------|--------|-------------|-------|
| ![](assets/blizzard_icon.webp) | Blizzard | 8 | 8d8 cold to every enemy (+1d8 for every 3 levels past 9), **Constitution** save for half; Icy for 3 turns on a fail. | 0.5.4+ |

## Harvest Druid Spells (Level Options) *(0.6.1+)*

Growth rather than weather: offered beside the storm spells, and like them a druid becomes a Harvest Druid by picking them.

| Unlocks | Icon | Spell | Energy | Description | Since |
|---------|------|-------|--------|-------------|-------|
| L1 | ![](assets/renewal_icon.webp) | Renewal | 4 | Plant new growth in an ally's wounds: they heal **1d6 per four levels** (at least 1d6) **+ Wisdom** at the start of each of their next **3 turns**. | 0.6.1+ |
| L3 | ![](assets/grasping_rice_icon.webp) | Grasping Rice | 5 | The field rises around every enemy: on a failed **Strength** save each is held fast for 2 turns (**Netted**: cannot move, attacks at disadvantage) until it tears free or an ally cuts it loose. | 0.6.1+ |

---

## Feat Levels

At levels 4, 8, 12 and 16 you also choose one general feat, as every class does.

---

## Tips

- **Sleet, then Lightning.** Sleet Storm soaks the line; Lightning Storm on Wet enemies deals double.
- **Open with Sand Storm.** Blinding the whole enemy line at level 1 swings an early fight: your party hits more and gets hit less.
- **Plague Storm keeps working.** The poison ticks for three turns after the swarm passes.
- **Wisdom is everything.** Every storm's DC runs off it.
