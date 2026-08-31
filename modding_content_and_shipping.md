# Modding: Content Types & Shipping

A companion to [`modding.md`](modding.md), which covers the framework
mechanics — how mods load, the registration hooks, custom items/enemies/areas.
This guide covers what comes *after* that:

- authoring a **wardrobe outfit** mod, a content type with its own registry and
  art contract;
- the **asset-production traps** that reliably cost time when generating
  character art for a mod;
- how to **package and distribute** a finished mod.

The advice here is drawn from building two full-size mods against this
framework — a 100-floor roguelike and a multi-character wardrobe pack — and is
written for anyone building their own.

---

## 1. `mods.in/` vs `game/mods/`

Ren'Py only compiles files under `game/`, so a mod must end up in
`game/mods/<mod_id>/` to run. But that is **not** where you author it.

```
mods.in/<mod_id>/          <- source of truth, committed to git
    <mod>.rpy              <- registration + image declarations
    images/                <- art that ships to players
    refs/                  <- identity anchors, NOT shipped
    prompts/               <- generation prompts, NOT shipped
    README.md

game/mods/<mod_id>/        <- installed copy, gitignored, built by `make mods`
```

`make mods` does `rsync -a --delete mods.in/<mod>/ game/mods/<mod>/` for every
mod folder. Two consequences worth internalising:

- **Never edit `game/mods/` directly.** It is a build artifact; the next
  `make mods` overwrites it.
- **Do not symlink `mods.in/<mod>` into `game/mods/`.** It is tempting (edits
  go live instantly) but `renpy distribute` *follows symlinks*, so the entire
  mod — including reference art and any dev-only material — silently ships
  inside every package. Use a real directory and re-run `make mods` after edits.

---

## 2. Outfit mods

Outfits are a distinct content type with their own registry, gating, and art
contract. A mod adds one by calling `register_outfit()` — it edits no base-game
file, and Vespera's Atelier picks it up automatically because the vendor
iterates the shared `OUTFITS` registry.

### The `Outfit` object

```python
from outfits import Outfit, register_outfit
from item import ItemRarity

register_outfit(Outfit(
    id="pegasus_academy",            # stable, unique
    character="pegasus",             # must match pegasus / pegasus_ss / pegasus_dc globals
    name="Succubus Academy Uniform",
    description="...",               # vendor tooltip
    price=180,
    icon="pegasus_academy_icon",     # bare image name, 96x96
    rarity=ItemRarity.UNCOMMON,
    combat_image="pegasus_academy_combat",       # healthy
    combat_image_mid="pegasus_academy_combat2",  # damaged
    combat_image_low="pegasus_academy_combat3",  # heavily damaged
    portrait_image="pegasus_academy_combat",
    has_emote_sprites=True,
    poses={
        "plain":   ["ch2_pegasus_academy_plain_1", ...],
        "topless": [...],
        "nude":    [...],
    },
    flavor={ "intro": "...", "plain": ["...", "...", "..."], ... },
))
```

`character` is load-bearing: the posing engine resolves `<character>`,
`<character>_ss` and `<character>_dc` from that string. Get it wrong and the
outfit registers but crashes when worn.

### Tier gating — two independent locks

Pose galleries are tiered `plain` → `topless` → `nude`, and a tier opens only
when **both** locks clear:

1. **Relationship** — `OUTFIT_TIER_THRESHOLDS` in `outfits.py`:
   `plain: 0`, `topless: 3`, `nude: 6`.
2. **Story gate** — `OUTFIT_TIER_STORY_GATES` maps `(character, tier)` to a
   store flag that must be `True`.

The second lock is the one that surprises people. **It is keyed on
`(character, tier)`, not on outfit id**, so *your* mod's outfits inherit
whatever gates the base game already defines for that character — you don't opt
in, and you can't opt out from mod code without touching the shared dict.

Gate flags for unreleased story content are declared `default False` and never
set, so a gated tier can be **unreachable in play no matter how high the
relationship is**. Before generating art for a tier, check that it actually
opens:

```python
unlocked_tiers(relationship, character, outfit_gate_check)
```

If the tier you're arting isn't in that list for any reachable game state, the
art will sit unused until the gating story ships.

### Art contract per outfit

| Asset | Count | Naming | Size |
|---|---|---|---|
| Item icon | 1 | `<char>_<outfit>_icon` | 96×96, background removed |
| Pose gallery | 3 per tier | `ch2_<char>_<outfit>_<tier>_<n>` | 2560×1080 |
| Combat sprites | 3 | `<char>_<outfit>_combat`, `_combat2`, `_combat3` | 2560×1080 transparent |
| Emote sprites | 6–12 | `<outfit_id>_<emotion>` | 2560×1080 transparent |

Emotions come from the mod's own list, e.g. `MOD_OUTFIT_EMOTIONS =
["normal", "blush", "angry", "sad", "surprised", "thinking", ...]`.

**Some characters have a form prefix.** A character whose `<char>_emote()`
translator prepends a form name (Nashoba's prepends `wolfgirl_`) needs her
outfit emote sprites named `<outfit_id>_<form>_<emotion>` instead of the plain
pattern. Check the character's `*_dialog.rpy` before arting her emotes. The safe
approach is to declare *both* patterns and let the missing one fall through:

```python
if outfit.has_emote_sprites:
    for emo in MOD_OUTFIT_EMOTIONS:
        _modout_defimg("%s_%s" % (outfit.id, emo))
        _modout_defimg("%s_wolfgirl_%s" % (outfit.id, emo))
```

### Degrade gracefully, don't crash

Declare every image through a `renpy.loadable()`-guarded helper, then **prune
pose entries whose art is missing** so the wardrobe only offers tiers it can
actually show:

```python
def _modout_defimg(name):
    path = "mods/mod_outfits/images/" + name + ".webp"
    if renpy.loadable(path):
        renpy.image(name, path)
        return True
    _MODOUT_MISSING.append(name)
    return False
```

This is why a half-arted outfit is playable and lint-clean. The flip side:
**missing art fails silently.** Audit against the table above rather than
trusting "the game didn't crash" — a whole tier can be absent with no error.

### Selling it in more than one shop

The base game only stocks outfits at Vespera. To appear everywhere, teach the
framework about each vendor and inject stock:

```python
MOD_OUTFIT_VENDORS = {
    "vespera":     ("setup_outfit_vendor",         "vespera_dc"),
    "thalassa":    ("setup_pirate_vendor",         "thalassa_dc"),
    "melitta":     ("ch2_athens_vendor_menu",      "melitta_dc"),
    "twins":       ("ch1_townsville_vendor_menu",  "ch1_vendor_twins_dc"),
    "hunt_market": ("ch2_vrykolakas_market",       "ch2_hunt_market_dc"),
}
for vid, (setup, var) in MOD_OUTFIT_VENDORS.items():
    register_mod_vendor(vid, setup, var)
```

The second tuple element is the vendor's **setup label**, which the framework
re-runs to top the shelf up. Point it at the wrong label and the vendor silently
never restocks, so verify each one against the vendor's own file.

### Enable/disable without breaking saves

Keep outfits **registered** when the mod is toggled off, and add their ids to
`outfits.DISABLED_OUTFITS` instead. The vendor, wardrobe, and worn-outfit
cleanup all respect that set, so the outfits vanish from play — but a save that
already pickled an `OutfitItem` still unpickles instead of raising `KeyError`.

---

## 3. Asset production traps

These are the failure modes that cost the most time in practice. All are avoidable once known.

### Get the whole silhouette in frame at generation time

The single highest-leverage rule. `rmbg` background removal **deletes wings,
tails, and other detached appendages when they run off the edge of the frame** —
it keeps only what it recognises as "person". Newer/crisper segmentation models
tend to be *worse* at this, not better, because they segment people more
aggressively.

Prompt for the full body inside the frame, wings folded or tucked. That is far
cheaper than any repair. If wings must be spread, render on **flat chroma green**
and key on colour with `tools/chroma_key.py` instead of `rmbg`.

Always verify a cutout by compositing over magenta — a deleted wing is invisible
against a white page and obvious against `(255,0,255)`.

### Folding beats outpainting

When a winged or tailed sprite comes back hard-clipped mid-span, there are two
possible fixes:

- **Outpaint the missing wingtips** — needed canvas padding, chroma fills,
  colour correction, and seam blending, and still produced AI-invented wing
  geometry.
- **Re-render with the wings folded behind the back** — the silhouette shrinks
  dramatically (roughly 29% of the canvas to 9% in one measured case), sits well
  clear of both edges, and clipping becomes *structurally impossible*.

The second is strictly better and much cheaper. Prefer changing the pose over
repairing the crop.

### Pipeline order matters: identity pass **before** the fold

If you run a `dev_lotf` identity pass over a chroma-green render, it replaces
the flat background with a *lit studio backdrop*. Measured greenness collapses
from 243 to 22, and the background range (−81…55) then **overlaps the subject's**
(−90…58) — no threshold can separate them, and chroma-keying becomes impossible.

```
✗ original → fold (grok) → identity (dev) → key      key impossible
✓ original → identity (dev) → fold (grok) → key      works
```

Put whichever step restores flat chroma **last**. Grok reliably returns clean
chroma green; Dev does not.

Related: run the identity pass at **cfg 1.0**. At higher cfg the character
LoRA's own prior overrides the source image — a LoRA trained on spread wings
will re-spread wings you just folded.

### Whole-frame edits drift everything

Flux2 edit models VAE-encode the *entire* frame, so "change only X" prompts
still shift untouched pixels — verified by measuring colour drift in a region
the prompt never mentioned. Consequences:

- For a **localized** change, use a true masked inpaint (`gin.py --provider
  klein --inpaint --box X,Y,W,H`). The binary mask preserves everything outside
  it mathematically, not just by request.
- Post-hoc "paste the original back over the result" compositing is a poor
  substitute: it reintroduces the hard seam you were trying to remove, and a
  global colour correction can't fix drift that varies across the frame.

Deriving one damage stage from another is a good use of masked inpaint — a
heavily-damaged `combat3` sprite can be built from an already-finished `combat2`
with two masked fills, guaranteeing the stages share identical pose, wings, and
framing so they swap without visible drift mid-fight.

### Provider moderation

Hosted providers moderate their output, and for adult content you will hit it.
The failure is often **stochastic rather than a hard block** — an identical
retry frequently succeeds — so retry 2–3× before concluding a prompt is refused.
For reliably explicit content use a local provider with no moderation layer.

### Resolution defaults

Check each provider's default resolution against your target canvas. A `1k`
default can be well under half a 2560×1080 sprite, forcing an upscale from a
soft source; asking for a higher tier lets you *downscale* into the canvas
instead, which is always cleaner.

---

## 4. Where art actually lives

Two different destinations, and putting art in the wrong one means it silently
disappears:

| Art for | Goes in | Notes |
|---|---|---|
| **A mod** | `mods.in/<mod>/images/` | Shipped as-is. `make mods` copies it. |
| **The base game** | `src_assets/` | **Never `game/images/`** |

`legacy_of_the_fallen/game/images/` is **gitignored and pipeline-generated** —
`make images` regenerates it from `src_assets/` via `resize_border.py`. Anything
written there directly is wiped by the next build.

This matters if your mod also improves *existing* character art rather than only
adding new art. Base-game sprites must be replaced in `src_assets/`, and they
reach players through a game build — not through your mod folder.

---

## 5. Packaging and distribution

### Shipping inside the game

Ship the folder. `make mods` installs it and it goes out inside the normal game
build. Nothing else needed.

### Dev-only mods

A mod present in `game/mods/` ships in **every** package — desktop and Android —
and the Mod Manager auto-discovers it. To keep one in-tree without shipping it,
exclude it from every package with `build.classify` in `options.rpy`:

```python
build.classify('game/mods/mod_decent_to_hell/**', None)
```

### Standalone download

To distribute a mod on its own, build both `.tar.gz` and `.zip` (Windows users
expect zip), with the mod folder at the **archive root** so extracting drops
`<mod_id>/` straight into `game/mods/`. Include an `INSTALL.md` at the root
written for players, not developers — where the game folder lives, where to put
the folder, how to enable it in the Mods menu.

Ship compiled `.rpyc` alongside `.rpy`. A standalone mod lands in an *installed*
game; without the compiled form Ren'Py has to write into the install directory
at first launch, which may be read-only.

### Resolution variants

If the base game has resolution variants, the mod needs them too: full-frame art
built for a 2560×1080 canvas overflows an FHD build's 1920×1080 virtual canvas
(set via `gui.init` in a generated `resolution.rpy`). Produce a cropped variant
with `resize_border.py --crop`.

**Exclude small assets from that pass.** `resize_border.py` unconditionally
resizes to the target dimensions after cropping, so a 96×96 icon run through it
is stretched to 1920×1080. Pull icons out, crop the full-frame art, put the icons
back untouched.

## 6. Checklist for a content mod

1. Author in `mods.in/<mod_id>/`; real directory in `game/mods/`, never a symlink.
2. Prefix every name; use `default` for anything that must persist in a save.
3. Guard every `renpy.image` with `renpy.loadable()`; prune dead entries.
4. Audit art against the asset table — missing art fails **silently**.
5. Verify cutouts over magenta; confirm no clipping at canvas edges.
6. Base-game art → `src_assets/`. Mod art → `mods.in/<mod>/images/`.
7. Decide bundled / dev-only / standalone; add the `build.classify` line if the
   mod should not ship.
8. For a standalone download: ship `.rpyc` alongside `.rpy`, mod folder at the
   archive root, `.tar.gz` + `.zip`, and a player-facing `INSTALL.md`.
9. `renpy <project> lint` before playtesting.
