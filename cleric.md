# Cleric Class Guide

**Versions:** every feature is tagged with the first game version it shipped in. *0.3.6+* means it was already in 0.3.6 or earlier.

The Cleric is a Wisdom-based divine caster focused on healing, radiation damage, and sustain. They excel in longer fights where their passive regeneration and party healing can turn the tide.

---

## Level Features

These are automatically granted at the listed level.

| Level | Icon | Feature | Since |
|-------|------|---------|-------|
| 1 | ![Heal](assets/heal_icon.webp) | Heal | 0.3.6+ |
| 2 | ![Divine Grace](assets/divine_grace_icon.webp) | Divine Grace | 0.3.6+ |
| 3 | ![Channel Divinity](assets/channel_divinity_icon.webp) | Channel Divinity | 0.3.6+ |
| 5 | ![Sacred Aura](assets/sacred_aura_icon.webp) | Sacred Aura | 0.3.6+ |
| 7 | ![Divine Ward](assets/divine_ward_icon.webp) | Divine Ward | 0.3.6+ |
| 9 | ![Blessed Resilience](assets/blessed_resilience_icon.webp) | Blessed Resilience | 0.3.6+ |
| 11 | ![Holy Aura](assets/holy_aura_icon.webp) | Holy Aura | 0.3.6+ |
| 14 | ![Extra Attack](assets/extra_attack_icon.webp) | Extra Attack | 0.3.6+ |
| 18 | ![Divine Ascension](assets/divine_ascension_icon.webp) | Divine Ascension | 0.3.6+ |
| 20 | ![Avatar of Light](assets/avatar_of_light_icon.webp) | Avatar of Light | 0.3.6+ |

### ![](assets/heal_icon.webp) Heal *(L1 — Auto · 0.3.6+)*
A baseline healing ability granted at level 1. Since 0.6.1, on the battle grid it is a touch: the ally must be on a square **next to you** (reach 1).

### ![](assets/divine_grace_icon.webp) Divine Grace *(L2 · 0.3.6+)*
Passive. Adds your **Wisdom modifier** to all saving throws.

### ![](assets/channel_divinity_icon.webp) Channel Divinity *(L3 — 5 Heavenfire energy, once per rest · 0.3.6+)*
Heal all allies for **2d8 + Wisdom modifier** HP, and deal **2d8 radiation damage** to all enemies simultaneously. Resets on rest.

### ![](assets/sacred_aura_icon.webp) Sacred Aura *(L5 · 0.3.6+)*
Passive. Regenerates **1d4 HP per turn**.

### ![](assets/divine_ward_icon.webp) Divine Ward *(L7 · 0.3.6+)*
Passive. Grants permanent **resistance to radiation damage**.

### ![](assets/blessed_resilience_icon.webp) Blessed Resilience *(L9 · 0.3.6+)*
Passive. Regenerates **1d6 HP per turn** (stacks with Sacred Aura for up to 1d4+1d6 per turn).

### ![](assets/holy_aura_icon.webp) Holy Aura *(L11 · 0.3.6+)*
Passive. Grants **+2 to spell saving throws** and **+2 Wisdom**.

### ![](assets/extra_attack_icon.webp) Extra Attack *(L14 · 0.3.6+)*
Passive. Grants one additional attack per turn.

### ![](assets/divine_ascension_icon.webp) Divine Ascension *(L18 · 0.3.6+)*
Passive. Permanently increases **Wisdom by 4**, with an ability score cap of 24.

### ![](assets/avatar_of_light_icon.webp) Avatar of Light *(L20 · 0.3.6+)*
Passive. Reduces all spell costs by **25%** and adds your **Wisdom modifier as bonus radiation damage** to all spells.

---

## Spells (Level Options)

Spells are chosen on level up and added to your action list.

### Level 1
| Icon | Spell | Energy | Description | Since |
|------|-------|--------|-------------|-------|
| ![](assets/aid_icon.webp) | Aid | 3 (Heavenfire) | Since 0.6.1 no target: grants **every living ally and yourself** temporary HP equal to **1d6 + Wisdom modifier + 1 per spell level**, lasting until rest. | 0.3.6+ |
| ![](assets/firebolt_icon.webp) | Firebolt | 1 | Standard fire damage spell. | 0.3.6+ |
| ![](assets/slap_icon.webp) | Divine Bitch Slap | 4 (Heavenfire) | **2d8 radiant** + 1d4 per four levels (max 5d4 more) + Strength modifier. Reach 1 (adjacent enemy) since 0.6.1. | 0.3.6+ |

### Level 2
| Icon | Spell | Energy | Description | Since |
|------|-------|--------|-------------|-------|
| ![](assets/sacred_flame_icon.webp) | Sacred Flame | 3 (Heavenfire) | Calls down sacred flame on a target. Deals **Nd8 + Wisdom modifier** radiation damage (N scales as `1 + level/3`). Dexterity save for half. | 0.3.6+ |
| ![](assets/heat_icon.webp) | Heat | 2 | Kindles magical warmth in a target. Constitution save or become **Hot**: 1d5 heat damage per turn for 5 turns. | 0.3.6+ |

### Level 3
| Icon | Spell | Energy | Description | Since |
|------|-------|--------|-------------|-------|
| ![](assets/smite_icon.webp) | Divine Smite | 8 (Heavenfire) | Weapon damage plus **2d8** radiation damage, +1d8 per four levels (max 5d8 more). Extra 1d8 vs. undead/demons. Radiant dice double on a crit. | 0.3.6+ |
| ![](assets/glacial_strike_icon.webp) | Glacial Strike | 2 | Channel cold through your weapon: weapon + scaling cold damage (1d10, +1d10 at L5/11/17). Failed enemy Con save grants you **Glacial Shield**. | 0.3.6+ |

### Level 5
| Icon | Spell | Energy | Description | Since |
|------|-------|--------|-------------|-------|
| ![](assets/fireball_icon.webp) | Fireball | — | Large area fire damage. | 0.3.6+ |
| ![](assets/greater_heal_icon.webp) | Greater Heal | 6 (Heavenfire) | Heals target for **4d8 + Wisdom modifier x2**. Scaling with level. Reach 1 (adjacent ally) since 0.6.1. | 0.3.6+ |
| ![](assets/blessed_strike_icon.webp) | Blessed Strike | 2 (Heavenfire) | Melee weapon hit + self-heal for **1d6 + Wisdom modifier**. | 0.3.6+ |
| ![](assets/sleet_storm_icon.webp) | Sleet Storm | 4 | AoE control: all enemies gain **Icy** + **Wet** for 5 turns. Icy = 30% chance to slip and lose a turn; Wet doubles Cold/Lightning damage taken. | 0.3.6+ |

### Level 7
| Icon | Spell | Energy | Description | Since |
|------|-------|--------|-------------|-------|
| ![](assets/holy_word_icon.webp) | Holy Word | 6 (Heavenfire) | All enemies take **Nd8 + Wisdom modifier** radiation damage (N scales as `2 + level/5`). Enemies who fail a Wisdom save are **Stunned for 1 turn**. | 0.3.6+ |

### Level 9
| Icon | Spell | Energy | Description | Since |
|------|-------|--------|-------------|-------|
| ![](assets/greater_heal_icon.webp) | Mass Heal | 8 (Heavenfire) | Heals all allies (including self) for **3d6 + Wisdom modifier**. | 0.3.6+ |
| ![](assets/blizzard_icon.webp) | Blizzard | 8 | AoE nuke: **8d8** cold damage to all enemies (Constitution save for half; scales +1d8 per 3 levels past 9). Those who fail are left **Icy** for 3 turns. Devastating after Sleet Storm's Wet. | 0.3.12+ |

---

## Affinity Spell Options *(L6+ — Affinity-Gated)*

| Affinity | Icon | Spell | Energy | Description | Since |
|----------|------|-------|--------|-------------|-------|
| Heavenfire | ![](assets/sacred_temptation_icon.webp) | Sacred Temptation | 0 (Lust) | Divine temptation that inflicts Horny. Charisma save to resist. | 0.3.6+ |

---

## Feat Levels

Generic feats are available at levels **4, 8, 12, and 16**.

---

## Tips

- **Wisdom is your primary stat.** It drives Divine Grace (saving throws), Sacred Flame damage, Blessed Strike heals, Holy Word damage, and Avatar of Light. Stack it.
- **Sacred Aura + Blessed Resilience** stack, giving up to **1d4 + 1d6 HP regen per turn** by level 9 — you become very hard to kill in extended fights.
- **Channel Divinity** is a swing ability: heals your whole party while damaging all enemies at once. Use it when the fight is balanced — it can flip the momentum entirely.
- **Holy Word** (L7) is your best crowd-control nuke. It hits every enemy and has a stun chance. Use it when you need to buy a turn.
- **Avatar of Light** (L20) combined with high Wisdom turns all your radiation spells into massive damage. Prioritize Wisdom investment heading into late game.
- The Cleric rewards a patient, reactive playstyle — let passive regen work for you and save high-cost spells like Channel Divinity and Holy Word for pivotal moments.
