# Outfit striptease clips (MiniMax H3 + guide frames)

A repeatable recipe for a ~15 s striptease video of any character in any
registered outfit, driven by the outfit's own pose art. Validated 2026-09-24 on
Cera's corset (worked example at the end), reworked 2026-09-26 on Pegasus's
futa corset and swimwear.

The idea in one line: **the outfit's own tier art pins identity and wardrobe,
the prompt carries the choreography, H3 animates between two or three guide
frames, and H3 refines its own output at 1.9x in chunked windows.** No
reference-to-video, no cloud upscalers.

```
<char>_<outfit>_plain_<n>   ──► frame 0
one close-up guide (Qwen)   ──► mid                  ─┐
<char>_<outfit>_nude_<n>    ──► last frame            │
                                                      ▼
prompt (hand-led camera, one take) ───► H3 SparseRef15, 20 steps, 362 frames
                                                      │
                                                      ▼
        --h3-upscale 1.9 --h3-attention kitchen (split refine) → 2560x1088
                                                      │
                                                      ▼
                     crop → 2560x1080, AV1 webm → mods.in/mod_outfits/video/
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

## 2. Guide frames

### The default: three guides

**Use as few guides as the clip will tolerate.** A dense storyboard was the
first-generation recipe and it costs more than it buys: every generated guide is
another chance to contradict the art, and the clip visibly settles onto each one.
The prompt already carries the choreography. Since 2026-09-26 the default set is
three frames:

| Frame | Guide | Source |
|---|---|---|
| 0 | full body, outfit on | `ch2_<char>_<outfit>_plain_<n>.webp`, untouched |
| ~216 | the reveal close-up | crop of the nude tier, Qwen super-rez (below) |
| 361 | full body, nude | `ch2_<char>_<outfit>_nude_<n>.webp`, untouched |

The first and last frames come straight from shipped art, so identity, wardrobe
and setting are pinned for free and cannot drift. The single interior guide goes
where the camera dwells longest and where the model is weakest on its own — for
a female clip that is the hips-and-vulva beat.

**For a futa character, do not put the interior guide on a head-on penis
reveal.** That beat cannot be guided; it has to be choreographed around. See
"Futanari clips" below before building the guide set.

Everything else — the unfastening, the top coming off, the breast close-up, the
upward sweep — the prompt handles. Validated on Pegasus's corset
(`sparse20_guided216`, the user's pick out of a field that included unguided and
densely-guided takes) and reused unchanged for her swimwear.

### Futanari clips: choreograph around the reveal

**Everything in this subsection is a futa problem.** H3's base model has
effectively no nudity in its training data and no prior at all for a penis
emerging from a garment, so a frontal futa reveal is the one beat in the whole
recipe the model cannot improvise. Female clips do not need any of this — the
hips-and-vulva beat behaves, one guide is enough, and the rest of the doc
applies unchanged. Read this only when the character is futa.

Four takes were spent trying to *guide* the head-on reveal and all four failed
the same way: for ~25 frames before the guide the model invents a pale
featureless tube, then snaps to the guide for two frames, then decays again. A
guide only reaches a few frames either side of itself; it cannot repair the
stretch in front of it.

**The fix is choreography, not guidance: turn her around.**

Rewrite the lower-garment beat so she rotates until her back is to the lens,
takes the garment off from behind (bare buttocks, which the model renders well),
then rotates back to face camera. The penis then only ever appears *after* she
is already turning square, with the final frame right there pinning it. On
Pegasus's swimwear this removed the problem in a single run after four takes of
patching it.

Three things this needs:

1. **Pin the rotation direction in frame-relative terms.** "She turns to her
   left" is ambiguous once her back is to the camera. Write what the frame
   shows: *"rotating so that her buttocks come round toward the right-hand side
   of the frame and her front swings away to the left"*, and describe the
   turn-back the same way. If it still comes out mirrored, flipping the guide
   horizontally is lossless and cheaper than re-rolling the clip.

2. **One guide at the turn-back, and give it runway.** See the next subsection —
   this is where guide placement matters most.

3. **Do not reach for a penis LoRA.** `H3/PLORA_H3_V2` at 1.0 fixes the malformed
   tip and ruins everything else: the penis inflates and reads semi-erect through
   the whole clip. 1.2 is worse. The LoRA is treating "penis" as the subject
   rather than a detail. If the profile still looks wrong after the turn, fix the
   *art* — see the last point below.

### Guide placement: a guide needs runway

**The single most useful thing learned on this clip.** The same guide, same
seed, same prompt, placed at two different frames:

| Guide frame | Result |
|---|---|
| 258 | hard cut — rear view through f257, three-quarter front at f260, background jumps. She teleports. |
| 300 | smooth animated rotation across f240-330. No cut. |

A guide ~100 frames after the previous one, asking for a 135-degree change of
body orientation, cannot be reached in three frames. Give a large pose change
**50-60 frames of runway** and place the guide where the motion is already
finishing, not where you want it to start. The same rule explains the dense
route's failures: guides every 50 frames leave no room to move *between* them,
so the clip visibly settles onto each one.

### Editing a guide with Qwen: one instruction at a time

Qwen's edit path treats the prompt as a single instruction and a second clause
displaces the first rather than adding to it. Measured on this clip:

| Prompt | Result |
|---|---|
| `Turn her 90 degrees to the left` | rotates correctly, identity and pose preserved |
| `...left. Her penis is smaller.` | **no rotation** |
| `...left. Her penis is soft and hangs down against her thigh.` | **no rotation** |
| `...left. Her penis is small, soft and flaccid...` | no rotation, anatomy nearly erased |

So: **turn in one pass, adjust anatomy in a second pass on the result** — or
better, fix the anatomy on the source art while she is still front-on, because
the last frame of the clip uses that art anyway and the whole clip will then
agree with it.

**Never pass a pose reference that contains the thing you are trying to fix.**
Feeding `nude_1` as identity plus a video frame as a pose ref copied the
malformed penis straight across, overrode her pose, and cropped her head out of
frame. One identity reference plus plain text was dramatically better. Run three
seeds: rotation lands about one time in three.

### The reveal close-up (crop → Qwen super-rez)

Do not generate this frame. **Cut it out of the nude tier art** so the anatomy
is the anatomy that actually ships, then rez it up:

1. Grid-overlay the nude tier image and read off the crotch box — never guess
   coordinates (see `feedback_klein_box_verify_large_images`).
2. Crop at the clip's aspect (2.333:1 for a 1344x576 canvas), framed like a
   held close-up: thighs filling the sides, the penis or vulva top-centre,
   nothing of the face. On a 2560x1080 source a box around 532x228 lands right.
3. Qwen super-rez the raw crop to the full canvas — feed the small crop and ask
   for the output size; the rescale is the upscale:

```bash
uv run python tools/gin.py --provider qwen --url http://192.168.69.44:8188   --size 1344x576 --seed <N> --image <crop>.png   --prompt "Reproduce image 1 exactly at higher resolution: identical framing, composition, pose, anatomy, proportions, colors, lighting and background. Do not change, add or remove anything. Only render it sharper, with finer skin texture and crisper anatomical detail. <lora:Qwen/lotf_qwen_v3.safetensors:1.0>"   --output final/216_penis.png
```

Run three seeds and pick in ivp. **Qwen shifts the grade** — expect the skin to
come back warmer than the source. It usually does not matter enough to fix, but
check it against frames 0 and 361 before committing, because H3 interpolates
toward this frame and a tone step mid-clip reads as a colour pop. If it is off,
match per-channel mean and std back to the lanczos crop rather than re-rolling.

### The dense route (first-generation recipe)

Kept for reference. Use it only when a clip genuinely needs a beat the prompt
cannot hold — an unusual garment order, a prop that must leave frame at a
specific moment. Six interior guides plus a last frame is ~50 frames apart:

| Frame | Beat | Guide source |
|---|---|---|
| 0 | full body, outfit on | plain tier, untouched |
| ~60 | hands at the first fastening, chin-to-waist | generate (plain + icon) |
| ~110 | top garment off, breasts revealed / cupped | generate from a **chest crop** of the topless tier |
| ~160 | breast close-up | generate from the chest crop + icon |
| ~215 | lower garment being pushed down | generate (all three tiers + icon) |
| ~265 | hips / vulva close-up | **re-extract** hip crop of nude tier → lanczos → SDXL vulva inpaint, box pasted back (see Fixing a guide) |
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

- **Vulva.** Qwen draws the mound smooth, or oversized when pushed. **Always
  double-check the vulva guide frames at 1:1 before rendering** (crop the box
  region, do not judge from the full frame) and refine if necessary; the H3
  render dwells on this beat and the guide is what it will reproduce. Two
  routes, both validated on the Halloween set (2026-09-25):
  - *Hips beat:* lanczos-upscale the raw hip crop to the canvas (no Qwen
    rescale), SDXL Illustrious inpaint with a small box over the crotch and
    booru tags, two seeds, then paste back ONLY the box through a feathered
    mask: `gin.py --provider sdxl --inpaint --image <lanczos crop> --box X,Y,W,H --denoise 0.9 --prompt "lotf <char>, 1girl, solo, nude, pussy, bald pussy, labia, cleft of venus, ..."`.
    The Qwen rescale + Qwen refine around the inpaint shifts skin tan and the
    background blue on every pass, so the guide no longer matches the tier
    art; the lanczos route keeps the tier's colours exactly.
  - *Legs beat (re-extracted, vulva missing or soft):* Qwen with TWO refs, the
    legs guide as image 1 and a ~160 px crop of the approved hips vulva as
    image 2: "Keep image 1 exactly as it is ... The only change: at the top of
    her thighs where they meet, add her bare vulva exactly like the one shown
    in image 2 ..." — adds a matching cleft without touching anything else.
  Verify the box coordinates with a grid crop first: a box placed from a
  coarse grid missed the crotch entirely on three of five characters.
  Futa characters: see the futa recipe in the create-outfit skill instead.
- **Small slips** (a nipple under a hand, a finger): paint a green blob in ivp
  and run `gin.py --provider dev --image <guide> --prompt "Replace ONLY the solid bright green block in this image with <content>. ... Do NOT alter anything outside the block. No green should remain."`.
- **Hair.** Describe it exactly as the tier art shows it (side, high/low, band,
  loose strands). A generic description flips or deletes ponytails and invents
  headbands.
- **Footwear and straps.** Generated legs invent garters and boots. Re-extract
  from the tier whose footwear should appear at that beat. If the strip ends
  fully nude (boots off), take the legs crop from the NUDE tier and put the
  boot removal in the prompt.
- **Props.** A prop carried in the plain tier (lantern, pumpkin) has to go
  somewhere: either write it into the opening beat (tossed, set down) and drop
  it from every later guide, or keep it throughout. A Qwen edit on the final
  torso guide removes it cleanly ("remove the X from her hand: her raised hand
  now rests open against her collarbone").
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

**Non-futa — the default.** 4-step turbo GGUF, ~7 minutes:

```bash
uv run tools/gen_video.py --engine h3_turbo \
  -i <plain tier> <nude tier> \
  -p <prompt>.txt -o <name>_base.mp4 --seed <seed> --length 360
```

**Futa only.** SparseRef15 at 20 steps, ~28 minutes:

```bash
export H3_UNET_FULL=minimaxH3Sparseref15_prunedPartialINT8V10.safetensors
uv run tools/gen_video.py --engine h3 --h3-steps 20 \
  -i <plain tier> <turn guide>.png:300 <nude tier> \
  -p <prompt>.txt -o <name>_base.mp4 --seed <seed> --length 360
```

- First `-i` is frame 0, last is the final frame, everything between is a
  waypoint with an explicit `:frame`. The canvas is derived from the first
  image's aspect (768 short edge, 1344 max long edge; 2560x1080 art → 1344x576).
  Generate guides at that canvas size.
- **Base model: turbo unless the character is futa.** The 4-step turbo GGUF is
  what every shipped non-futa clip was rendered with, Cera's corset included,
  and its anatomy is fine on female bodies. **SparseRef15 at 20 steps is a futa
  measure only** — it was adopted because turbo renders futa anatomy poorly at
  the reveal, and that is the only place it has been shown to help. It costs 4x
  the base time (~28 min vs ~7), so do not pay for it on a non-futa clip. Set it
  via `H3_UNET_FULL`; `--engine h3` picks the full-checkpoint path.
- Iterate at the base: the refine keeps the seed, so the motion you approve is
  the motion you ship.
- Contact-sheet it (`ffmpeg -ss T -frames:v 1` at each guide time, `xstack`)
  and open sheet + mp4 in ivp. Check that each sampled frame matches its guide,
  that garments stay off once removed, and that hair, footwear and markings do
  not flicker between beats.

## 5. Refine to 1.9x (chunked)

```bash
... same command ... -o <name>_19.mp4 --h3-upscale 1.9 --h3-attention kitchen
```

- Same seed, same guides. 1.9x takes a 1344x576 canvas to **2560x1088**, which
  is the game canvas plus 8 rows to crop — no lanczos fill, no bars.
- The refine is a **split schedule**: the tail of the same sigma ladder the base
  pass used, re-run at the upscaled size (`--h3-upscale-refine-steps` to change).
  `--h3-upscale-denoise 0` decodes the raw upscaled latent, which is softer than
  a lanczos resize — never ship that.
- `--h3-attention kitchen` (comfy-kitchen INT8 attention) is required at this size.
- Since 2026-09-26 the refine sample is **chunked in time** through the upstream
  `MMH3SplitUpscale` node: overlapping windows of 73 pixel frames with 22 frames
  of overlap, each window's conditioning re-anchored, then crossfaded. This is
  what makes 1.9x survive a 15 s clip; a single sampler pass over 362 frames
  aborts server-side at any scale above ~1.5x. Verified no seam or pose jump at
  the window boundaries (73 / 146 / 219 / 292).
- Chunk lengths must sit on H3's **17k+5 pixel-frame grid** (73, 90, 107, 136…)
  with overlap 17 or 22. The conv3d upscaler's own chunking knobs are *latent*
  frames — a different axis, and a no-op at these lengths (latent T ≈ 22).
- Budget ~40 min for 15 s on .51 with turbo (~7 min base, ~32 min refine), or
  ~60 min on SparseRef15. Peak ~56 GB either way. **Turbo plus the chunked 1.9x
  refine is not yet validated** — the pre-split 1.9x failures were all on turbo,
  and every success since the split node landed has been on SparseRef15. Confirm
  it on one clip before batching a set.
- Guides re-anchor at the refine resolution, so identity holds; poses can shift
  a touch as the tail steps re-author detail. `--h3-upscale-refine-steps 2` if
  that matters for a shot.
- Knobs, should a run need them: `H3_REFINE_CHUNK_FRAMES` (73),
  `H3_REFINE_OVERLAP_FRAMES` (22), `H3_REFINE_IDENTITY_ANCHOR` (0),
  `H3_REFINE_MOTION_ANCHOR` (22), `H3_REFINE_SEAM_POLISH` (auto). Setting
  `H3_REFINE_CHUNK_FRAMES=0` restores the old single-pass behaviour.

### History: why 1.5x used to be the ceiling

Until the chunked refine landed, anything above 1.5x aborted on a 362-frame
clip — 2.0, 1.9, 1.875 and 1.833 all died server-side, the queue emptied, and
`gen_video.py` hung forever on a 0-byte log. It was never VRAM (~52 of 95 GB at
peak) and never the base model. It was length, not scale: the same 1.875 refine
succeeded on a 243-frame clip, which is how the Pegasus wedding pose clip got
rendered at 2528x1088. Full diagnosis in `tmp/h3_upscale_symptoms.md`.

## 6. Deliver

```bash
mkdir -p mods.in/mod_outfits/video
ffmpeg -i <name>_19.mp4 -vf "crop=2560:1080:0:4" \
  -c:v libsvtav1 -crf 28 -preset 6 -pix_fmt yuv420p -g 40 -an \
  mods.in/mod_outfits/video/<char>_<outfit>_striptease.webm
```

At 1.9x the refine lands on 2560x1088, so **crop** 8 rows rather than scaling —
no resample at all on the delivered pixels. The encode matches
`tools/create_videos.sh` (AV1, GOP 40, silent). Keep the 2560x1088 mp4 master in
the scratch folder, **not** in `video/` — the DLC packagers walk that folder and
a 23 MB master rides along for nothing. Register the webm the same way as any
other mod video.

Naming is by convention, no registration code needed:
`<char>_<outfit>_striptease.webm`, `<char>_<outfit>_poses.webm`, and the futa
variants `<char>_<outfit>_futa_striptease.webm` /
`<char>_<outfit>_futa_poses.webm`. Bump `modout_version` and add a CHANGELOG
entry in the same commit.

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
- **Dense guide sets** (six interior beats): each one is a chance to contradict
  the art, and the clip visibly settles onto every guide instead of moving
  through it. Three guides beat seven in a side-by-side on Pegasus's corset.
- **Starting the clip from the clothed art and letting H3 invent the strip**
  unguided: the garment comes back mid-clip and limbs duplicate. The nude tier
  as the last frame is what stops that.
- **Fixing bad video anatomy with LoRAs** (penis LoRAs, reveal LoRAs, higher
  weights, more steps): the ceiling is the *source art* H3 interpolates toward,
  not the model. If the clip's anatomy is wrong, repaint the guide frame.
  `H3/PLORA_H3_V2` at 1.0 does fix a malformed tip, but inflates the penis and
  makes it read semi-erect for the whole clip; 1.2 is worse.
- **A pose reference that contains the defect.** Qwen copies it verbatim, and
  the pose ref also overrode the subject's pose and cropped her head off. One
  identity ref plus text.
- **Stacking two instructions in a Qwen edit.** The second silently replaces the
  first.
- **Feather-pasting the original anatomy back over an edit.** The surrounding
  pixels no longer match, so it leaves a patch; auto-alignment keyed on the
  background rather than the body and hit its search bounds. Compositing the
  *edit's* hands onto the *original* worked; the reverse did not.
- **There is no penis-physics LoRA for H3.** Checked the public catalogue
  2026-09-28: the nearest is a generic secondary-motion booster
  (`ref2VA_Motion_v2`, trigger `dynv2`, 0.6-0.8), trained on two-person scenes.
  `Worship It` explicitly converts a flaccid penis to erect — avoid for these
  clips.

## Server notes (.51)

The refine depends on local state on phoenix that a ComfyUI or comfy-kitchen
update would silently remove: the Triton backend flag in `deep_start.sh`, an
int32 guard in comfy-kitchen's Triton `int8_linear`, and the
`Comfyui_Minimax_h3_latent_Upscaler` pack being current enough to provide
`MMH3SplitUpscale` / `MMH3TemporalSplitParamsV10`. Our old local temporal-chunk
patch on the upscaler node is superseded by upstream's own
`enable_temporal_chunking` and should not be re-applied. Details and the restart
recipe are in the memory note `feedback_h3_latent_upscale`. If a render goes
quiet, check `systemctl show comfyui -p NRestarts`: a crashed server leaves
`gen_video.py` waiting forever.

Updating that pack broke three call sites once, so if the refine suddenly throws
on a fresh checkout: the node is named `MinimaxH3LatentUpscaler3D` (not
`...UpscalerNode3D`), it needs `"mode": "target dimensions"`, and its nested
inputs must be **dot-prefixed** (`mode.width`, `mode.height`) — siblings give
`float(None)` and a nested dict gives "missing required argument 'mode'".

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
## Worked example: Pegasus, corset, futa (three guides)

Folder `mods.in/mod_outfits/tmp/pegasus_corset_futa_strip/`. Canvas 1344x576,
seed 20260924, SparseRef15 at 20 steps.

| Frame | Guide | Source |
|---|---|---|
| 0 | `ch2_pegasus_corset_futa_plain_1.webp` | plain tier, untouched |
| 216 | `final/216_penis.png` | hip crop of the futa nude tier → Qwen super-rez |
| 361 | `ch2_pegasus_corset_futa_nude_1.webp` | nude tier, untouched |

Base `sparse20_guided216.mp4` (1344x576, ~28 min), refined to `split19.mp4`
(2560x1088, ~32 min), delivered as
`mods.in/mod_outfits/video/pegasus_corset_futa_striptease.webm` (2560x1080 AV1,
11 MB) in mod 1.2.

This take was picked over an unguided run, a densely-guided run, and variants
with the H3 penis and "reveals" LoRAs at several weights. The lesson that came
out of it: none of the LoRA work moved the needle, because the limit was the
guide frame's own anatomy. Fix the art, not the sampler.

## Worked example: Pegasus, swimwear, futa (turn-around)

Folder `mods.in/mod_outfits/tmp/pegasus_swimwear_futa_strip/`. Canvas 1344x576,
seed 20260924, SparseRef15 at 20 steps, no LoRAs.

Eleven takes. The first four tried to guide a head-on reveal of the penis as the
bikini bottoms come off, with one guide, two bracketing guides, Qwen-edited
hands-at-hips guides, and Dev-edited variants of those. All four produced the
same failure: the model improvises a malformed penis for ~25 frames, snaps to
the guide, then decays. Two more takes tried `H3/PLORA_H3_V2` at 1.0 and 1.2,
which fixed the tip and inflated everything else.

What shipped, take K:

| Frame | Guide | Source |
|---|---|---|
| 0 | `ch2_pegasus_swimwear_futa_plain_1.webp` | plain tier, untouched |
| 300 | `final/258_turn.webp` | `nude_1` rotated by Qwen (`"Turn her 90 degrees to the left"`, seed 303) |
| 361 | `ch2_pegasus_swimwear_futa_nude_1.webp` | nude tier, untouched |

Prompt: `pegasus_swimwear_futa_strip_turn_dir.txt` — she turns her back to the
lens, slips the side-ties and pushes the bottoms down from behind, holds on her
bare ass, then rotates back to square, with the direction pinned frame-relative.

Delivered as `mods.in/mod_outfits/video/pegasus_swimwear_futa_striptease.webm`
(2560x1080 AV1, 7.0 MB) in mod 1.4.

The lesson, and it inverts the note on the corset example above: when a beat is
outside the model's prior, more guides do not help. Change what the camera is
asked to watch.

