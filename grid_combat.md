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

### Dash *(0.6.1+)*

**Dash** is on every character's action bar during grid fights. It costs no energy and uses one of your actions for the turn. In exchange you get your full move again on top of whatever you have left, so a turn's movement doubles. Squares you walked before dashing still count.

- If Dash was your last action, you then walk the extra squares (blue) and press **End Turn** when you're done.
- With actions left, the turn carries on as normal, and the move hint shows the new total.
- It isn't a disengage. Breaking away from an enemy still draws its free attack.
- A Netted or Pinned character can't dash.
- Enemies (and allies on Auto Battle) dash only when nothing they have can reach anyone this turn, the extra squares get them closer, and they haven't moved yet.

### Knock-back *(0.6.1+)*

Some attacks **push** the target straight away from the attacker: the fighter's **Pushing Shot** (one square on a failed Strength save) and the **Windforce** bow (one square on every hit, two with Pushing Shot).

- The push goes in the 8-way direction closest to a straight line from attacker to target.
- It stops at the edge of the field or at an occupied square, and nobody is hurt by the stop.
- Being pushed is forced movement: it draws **no free attacks** and doesn't use the target's move.
- Netted or Pinned targets are held in place and can't be pushed.
- The combat log says how far ("pushed back 1 square") or that the target held its ground, and the token slides to its new square on the map.

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
| River Surge (Kallirhoe) | a line 1 column wide and 4 rows tall, aimed anywhere *(0.6.1+)* |
| Semi-Automatic Shot (AR15, Euryale's rifle) | a line 1 column wide and 5 rows tall, aimed anywhere *(0.6.1+)* |
| Volley, Suppressing Fire (Fighter) | 3 x 3, aimed anywhere in range *(0.6.1+)* |

Exact values live in `combat_attacks.py` and `cold_movesets.py` (`splash_size`, `splash_self`, `reach`).
