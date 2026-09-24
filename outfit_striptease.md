# Outfit striptease clips (MiniMax H3 + guide frames)

A repeatable recipe for a ~15 s striptease video of any character in any
registered outfit, driven by the outfit's own pose art. Validated 2026-09-24 on
Cera's corset (worked example at the end).

The idea in one line: **the outfit's own tier art pins identity and wardrobe,
Qwen makes the in-between key poses, H3 animates between them, and H3 refines
its own output at 1.5x.** No reference-to-video, no cloud upscalers.

```
<char>_<outfit>_{plain,topless,nude}_<n>  ─┐
                                            ├─► guide frames (Qwen + crops)
<char> face icon                           ─┘        │
                                                      ▼
prompt (hand-led camera, one take) ───► H3 fl2v turbo, native canvas, 362 frames
                                                      │
                                                      ▼
                          --h3-upscale 1.5 --h3-attention kitchen  →  1.5x canvas
                                                      │
                                                      ▼
                     lanczos → 2560x1080, AV1 webm → mods.in/mod_outfits/video/
```

Conventions below: `<char>` is the character's lotf trigger (`ceraphina`,
`pegasus`, `nashoba`, `kallirhoe`, `danu`, `igret`, `chrys`), `<outfit>` the
outfit id, `<n>` the pose number. Work in a scratch folder such as
`mods.in/mod_outfits/tmp/<char>_<outfit>_strip/` with a `guides/` subfolder;
keep the prompt, run scripts and every guide's JSON prompt there.

## 1. Source art

Take all three tiers of **one pose number**, plus the character's face icon:

```
mods.in/mod_outfits/images/ch2_<char>_<outfit>_plain_<n>.webp    frame 0, verbatim
mods.in/mod_outfits/images/ch2_<char>_<outfit>_topless_<n>.webp  anatomy ref, topless beats
mods.in/mod_outfits/images/ch2_<char>_<outfit>_nude_<n>.webp     anatomy ref, nude beats
src_assets_no_resize/<char>_icon_0001.webp                        face ref
```

Before writing anything, **look at the tiers and list what is actually there**:
hair (style, band, side), jewellery, garments per tier, hosiery, footwear per
tier (the nude tier can have different shoes from the plain tier), harness or
straps, tattoos, wings, ears, horns. Every prompt and guide must describe these
exactly as drawn. Most guide failures were the prompt contradicting the art.

## 2. Storyboard → guide frames

A 15 s clip is 362 frames at 24 fps. Six interior guides plus a last frame is a
good density (~50 frames apart). The beats of a strip are always the same shape;
adapt the garments:

| Frame | Beat | Guide source |
|---|---|---|
| 0 | full body, outfit on | plain tier, untouched |
| ~60 | hands at the first fastening, chin-to-waist | generate (plain + icon) |
| ~110 | top garment off, breasts revealed / cupped | generate from a **chest crop** of the topless tier |
| ~160 | breast close-up | generate from the chest crop + icon |
| ~215 | lower garment being pushed down | generate (all three tiers + icon) |
| ~265 | hips / vulva close-up | **re-extract** hip crop of nude tier → Qwen rescale → SDXL vulva inpaint → Qwen refine |
| ~315 | low legs shot for the upward sweep | **re-extract** legs crop of the tier whose footwear you want → Qwen rescale |
| 361 | nude medium/close, final pose | generate from a nude torso crop + icon; fix slips with a Dev blob pass |

Drop or add beats for the outfit (a one-piece has one garment; a corset plus
skirt has two). Keep one guide per garment reveal and one per close-up the
camera should dwell on.

### Generating a guide (Qwen)

`gin.py --provider qwen`, `lotf_qwen_v3` LoRA (covers all eight characters),
**JSON prompt** (prose only half-triggers identity), canvas forced to the H3
canvas size (see §4 for how to get it; 21:9 art gives 1344x576):

```bash
uv run tools/gin.py --provider qwen --url http://192.168.69.51:8188 \
  --size <W>x<H> --seed <seed> \
  --image <ref1> [<ref2> ...] src_assets_no_resize/<char>_icon_0001.webp \
  --prompt "$(cat guides/<beat>.prompt.txt)" \
  --output guides/<beat>.png
```

Prompt skeleton:

```json
{
  "scene": "Keep the woman's face, hair (<hair exactly as in the art>), <markings/jewellery>, body and the room exactly as in image 1; image N is a close-up of her face. lotf, <char>, <identity line>, <what she wears at this beat>, <shot size and framing>, in <room from the art>",
  "subjects": [{"description": "<identity line>", "position": "centered", "action": "<the beat: hands, garment state, gaze>"}],
  "style": "high quality 3d render like elden ring, highly detailed skin and material textures, painterly fantasy visual-novel CG",
  "lighting": "<lighting from the art>",
  "background": "<room from the art>",
  "composition": "<shot size>, <framing from ... to ...>, front view, solo"
}
<lora:Qwen/lotf_qwen_v3.safetensors:1.0>
```

Run two seeds per beat and pick in ivp. Save the JSON beside the PNG.

**Framing rule: the first ref sets the framing.** On a wide canvas with a
full-scene ref, Qwen returns medium/full-body shots whatever the composition
field says. For a close-up beat, crop the tier image to the region at native
resolution, keeping the canvas aspect (896x384 for 21:9), and pass **that crop**
as image 1. It respects the tight framing and inherits the tier's anatomy.

### Re-extracting instead of generating

When the beat already exists in the tier art (hips, legs, a static torso), do
not generate it. Crop at native res, then let Qwen rescale to the canvas with a
"reproduce exactly" prompt: sharper than lanczos and faithful to the art.

```bash
uv run tools/gin.py --provider qwen --url http://192.168.69.51:8188 \
  --size <W>x<H> --seed <seed> --image guides/ref_<region>_crop.png \
  --prompt "Reproduce image 1 exactly at higher resolution: identical framing, composition, pose, anatomy, proportions, colors, lighting and background. Do not change, add or remove anything. Only render it sharper with finer skin, fabric and wood detail. <lora:Qwen/lotf_qwen_v3.safetensors:1.0>" \
  --output guides/<beat>.png
```

The same prompt doubles as the **Qwen refine pass**: run it on a guide after an
SDXL or Dev patch to pull the patch back into one style.

### Fixing a guide

- **Vulva.** Qwen draws the mound smooth, or oversized when pushed. Use the SDXL
  Illustrious inpaint on the rescaled hip crop with a small box over the crotch
  and booru tags, two seeds, then the Qwen refine pass:
  `gin.py --provider sdxl --inpaint --image <guide> --box X,Y,W,H --denoise 0.9 --prompt "1girl, solo, pussy, bald pussy, labia, cleft of venus, ..."`.
  Futa characters: see the futa recipe in the create-outfit skill instead.
- **Small slips** (a nipple under a hand, a finger): paint a green blob in ivp
  and run `gin.py --provider dev --image <guide> --prompt "Replace ONLY the solid bright green block in this image with <content>. ... Do NOT alter anything outside the block. No green should remain."`.
- **Hair.** Describe it exactly as the tier art shows it (side, high/low, band,
  loose strands). A generic description flips or deletes ponytails and invents
  headbands.
- **Footwear and straps.** Generated legs invent garters and boots. Re-extract
  from the tier whose footwear should appear at that beat.
- **Wings, ears, horns, tails.** Same rule: name them in every guide prompt and
  keep the icon as a ref, or they vanish on close-ups.

Review all guides in ivp in clip order before rendering
(`uv run tools/ivp.py <plain tier> guides/... --name <name>`). Notes left in the
viewer come back with `uv run tools/ivp.py --read-feedback <name>`.

## 3. The prompt

Four parts, in this order. `mods.in/mod_outfits/tmp/h3_vae_test/sensual/cera_corset_sensual_fl2v.txt`
is a filled example.

1. **Subject, wardrobe, style.** Hair and markings as in the art, the exact
   garments of the plain tier, the room, then the style sentence:
   "Painterly fantasy digital-illustration style: smooth painted shading, soft
   glowing rim light, an illustrated visual-novel CG look." State the lighting
   as steady and continuous.
2. **Camera contract.** "One uninterrupted take, slow and sensual throughout.
   Every camera move is small amplitude at slow speed, gliding rather than
   cutting. Her hands lead the framing: the camera goes where her hands go. She
   keeps soft eye contact with the lens whenever her face is in frame. No cuts,
   hidden edits, teleporting, digital zooms. Clothing comes off in a continuous
   visible motion, one garment at a time, and stays off."
3. **Choreography.** One paragraph per phase, in guide order. Each phase names
   the hand motion, the camera move as type + amplitude + speed, and the reveal,
   and ends on the pose of the next guide. Put the sweeps in explicitly, e.g.
   "the camera sinks smoothly down to her shoes and sweeps slowly upward along
   her legs ... and rises to her chest as both hands come to the laces".
4. **Sound line.** Fabric, ambience, breath. No dialogue.

Keep it I2VA-shaped: continuous development, no "then"-lists, no `[Shot N]`
timestamps. The guides carry the timing; the prose carries the motion between
them.

## 4. Base render

```bash
uv run tools/gen_video.py --engine h3_turbo \
  -i <plain tier> guides/<beat1>.png:60 guides/<beat2>.png:110 ... guides/<last>.png \
  -p <prompt>.txt -o <name>_base.mp4 --seed <seed> --length 360
```

- First `-i` is frame 0, last is the final frame, everything between is a
  waypoint with an explicit `:frame`. The canvas is derived from the first
  image's aspect (768 short edge, 1344 max long edge; 2560x1080 art → 1344x576).
  Generate guides at that canvas size.
- About 7 minutes on .51. Iterate here: it is cheap, and the refine keeps the
  seed, so the motion you approve is the motion you ship.
- Contact-sheet it (`ffmpeg -ss T -frames:v 1` at each guide time, `xstack`)
  and open sheet + mp4 in ivp. Check that each sampled frame matches its guide,
  that garments stay off once removed, and that hair, footwear and markings do
  not flicker between beats.

## 5. Refine to 1.5x

```bash
... same command ... -o <name>_up15.mp4 --h3-upscale 1.5 --h3-attention kitchen
```

- Same seed, same guides. The default refine is the **split schedule**: the last
  3 of the 4 turbo steps re-run at the upscaled size (`--h3-upscale-refine-steps`
  to change). `--h3-upscale-denoise 0` decodes the raw upscaled latent, which is
  softer than a lanczos resize, so never ship that.
- `--h3-attention kitchen` (comfy-kitchen INT8 attention) is required at this
  size on .51.
- About 15 minutes and ~56 GB peak for 15 s. Guides re-anchor at the refine
  resolution, so identity holds; poses can shift a touch as the last steps
  re-author detail. `--h3-upscale-refine-steps 2` if that matters for a shot.
- **2x does not work** for a 15 s clip: ComfyUI aborts on the first refine step
  every time. 1.5x is the ceiling until the refine can be chunked in time.

## 6. Deliver

```bash
mkdir -p mods.in/mod_outfits/video
cp <name>_up15.mp4 mods.in/mod_outfits/video/<char>_<outfit>_striptease_<W>x<H>.mp4   # master
ffmpeg -i mods.in/mod_outfits/video/<char>_<outfit>_striptease_<W>x<H>.mp4 \
  -vf "scale=2560:1080:flags=lanczos" -c:v libsvtav1 -crf 28 -preset 6 -pix_fmt yuv420p -g 40 -an \
  mods.in/mod_outfits/video/<char>_<outfit>_striptease.webm
```

Lanczos, not swin2sr: the final step is under 1.6x and SR smears this render
style. The encode matches `tools/create_videos.sh` (AV1, GOP 40, silent). A
21:9 refine is 2.33:1 against the 2.37:1 game canvas; the scale stretches about
1.5 % horizontally rather than cropping. Register the webm the same way as any
other mod video.

## Things that did not work

- **Ref2VA** (`--engine ref2va`, tier images and icon as refs at max size):
  identity drifted to a generic anime face and the room was reinterpreted.
  Guide frames from the real art beat it on identity, style and speed.
- **BFL FLUX video upscale**: refuses nude content even at the most permissive
  tolerance.
- **Qwen close-ups from a full-scene ref**: come back as medium shots. Crop first.
- **Generated vulva and legs guides**: inflated anatomy, invented straps.
  Re-extract from the art.
- **Raw 2x latent upscale without refine**: softer than lanczos.

## Server notes (.51)

The 1.5x refine depends on local patches on phoenix that a ComfyUI or
comfy-kitchen update would silently remove: the Triton backend flag in
`deep_start.sh`, temporal chunking in the H3 latent-upscaler node, and an int32
guard in comfy-kitchen's Triton `int8_linear`. Details and the restart recipe
are in the memory note `feedback_h3_latent_upscale`. If a render goes quiet,
check `systemctl show comfyui -p NRestarts`: a crashed server leaves
`gen_video.py` waiting forever.

## Worked example: Cera, corset, pose 1

Folder `mods.in/mod_outfits/tmp/h3_vae_test/sensual/`. Canvas 1344x576, seed
20260924, guides at 60/110/160/215/265/315 + last:

| Frame | Guide | Source |
|---|---|---|
| 0 | `ch2_cera_corset_plain_1.webp` | plain tier |
| 60 | `s1_unlacing_v2_0` | Qwen, plain + icon |
| 110 | `s2_cupping_v2` | Qwen, topless chest crop |
| 160 | `s3_breasts_v4_1` | Qwen, chest crop + icon |
| 215 | `s4_skirt_down` | Qwen, all tiers + icon |
| 265 | `s5_vulva_final` | nude hip crop → Qwen → SDXL inpaint (seed picked in ivp) → Qwen refine |
| 315 | `s55_legs_plain_qwen` | plain legs crop → Qwen (low-cut shoes, not the nude tier's boots) |
| 361 | `s6_nude_medium_v3_0_fix` | Qwen, nude torso crop + icon, Dev blob fix on the nipple |

Outputs: `cera_corset_sensual_base_v5.mp4` (1344x576, 7 min),
`cera_corset_sensual_up15.mp4` (2016x864, 15 min), delivered as
`mods.in/mod_outfits/video/cera_corset_striptease.webm` (2560x1080 AV1) with the
2016x864 mp4 kept beside it as the master.

Lessons that came out of this run and are folded into the rules above: write
the hair as drawn (three guides lost or flipped the ponytail on "high
ponytail"), re-extract legs and hips rather than generate them, crop before
asking Qwen for a close-up, and review the guide set in ivp with notes before
spending a render.
