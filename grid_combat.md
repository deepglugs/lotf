# Battle Grid

From 0.6, fights play out on an **isometric grid** over the battle map, with every combatant standing on a square as a chibi token. Initiative still sets the turn order; the grid decides who can reach whom.

## Grid size

The grid grows with the fight, using the smallest size that leaves room to move (each side deploys in two columns, and the field allows about five squares per combatant):

| Grid | Columns x rows |
|------|----------------|
| Small | 8 x 5 |
| Medium | 10 x 6 |
| Large | 12 x 7 |
| Largest | 14 x 8 |

## Movement

Each turn a character can move **1 + (DEX − 10) ÷ 4** squares (rounded down), **at least 2**, in any of the 8 directions, never through an occupied square:

| Dexterity | Squares per turn |
|-----------|------------------|
| up to 17 | 2 |
| 18–21 | 3 |
| 22+ | 4 |

Some effects add bonus movement on top.

## Reach

- **Melee** attacks reach the 8 squares around you (reach 1).
- **Touch spells and weapon-delivered spells** are reach 1 too: Heal, Greater Heal, Lay on Hands, Divine Bitch Slap and the smites (Divine Smite, Water Smite and the like).
- **Ranged weapons and most spells** reach any square. Equipping a bow or firearm turns your basic attack into a ranged attack.
- **Close-in weapon moves need a melee weapon** *(0.6.1+)*: the fighter's maneuvers, the smites, Heavenfire Blade, Glacial Strike and Reckless Attack are greyed out while a bow or firearm is equipped. Execute Strike and Sneak Attack follow the weapon instead and shoot with a bow or gun.
- A few breath attacks reach 2 squares.

## Engagement

- **Leaving** a square next to an enemy gives that enemy one free melee attack against you (once per enemy per move).
- A **ranged or spell attack** made while an enemy stands next to you rolls with **disadvantage**.

## Area spells

Area spells hit a square area centred on the square you aim at; a few are centred on the caster instead.

| Spell | Area |
|-------|------|
| Fireball | 2 x 2 |
| Web Barrage, Black Hole, Spore Cloud, Blizzard, Sand Storm | 3 x 3 |
| Sleet Storm, Divine Wrath | 5 x 5 |
| Heavenfire Nova | 5 x 5 around the caster |
| Leg Sweep (Fighter) | 3 x 3 around the caster |
| Cleave (Fighter) | a line of 3 squares in front of or behind the caster |
| River Surge (Kallirhoe) | a line 4 columns long and 1 row tall (sideways), aimed anywhere *(0.6.1+)* |
| Semi-Automatic Shot (AR15, Euryale's rifle) | a line 5 columns long and 1 row tall (sideways), aimed anywhere *(0.6.1+)* |
| Volley, Suppressing Fire (Fighter) | 3 x 3, aimed anywhere in range *(0.6.1+)* |

Exact values live in `combat_attacks.py` and `cold_movesets.py` (`splash_size`, `splash_self`, `reach`).
