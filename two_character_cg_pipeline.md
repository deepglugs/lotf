# Two-character explicit CGs and their animation

A recipe for a two-character explicit CG (two figures, both with genitals in
frame) and the chain of H3 clips that animate it. Worked out 2026-09-29 to
2026-10-01 on Pegasus's futa arc (`game/pegasus_futa_arc.rpy`): the anatomy
comparison and the tent "experiment", each in a male-Chrys and a futa-Chrys
variant.

In one line: **Qwen composes the scene, the genitals are repaired one
character at a time inside hand-painted strokes, Qwen refines the whole frame,
and H3 (full model + PLORA) animates a chain of clips that each start on the
still the previous one ends on.**

```
Qwen compose (2 char refs)  ──►  pick base  ──►  user paints strokes in ivp
        │                                              │
        │                         remove wrong anatomy (base Klein / Qwen crop edit)
        │                                              │
        │                 add genitals ONE SIDE AT A TIME (Illustrious + nyl2,
        │                 1024 crop, stroke-shaped mask, 3 seeds, user picks)
        │                                              │
        ▼                                              ▼
                   Qwen refine (same size, "keep image 1 exactly")  ──►  base still
                                                       │
            H3 full model + PLORA, direct --h3-upscale 1.9, per beat:
            I2V transition ─► last frame = next still ─► FL2VA loop on that still
                                                       │
            AV1 masters (src_videos/.../h3_final) ─► same file in src_elite ─► ELITE clips
```

Drafts, seeds, logs and intermediates go in `tmp/<work>/`. Only approved
finals and their prompt files go into `src_assets/`, `src_videos/` and
`src_elite/`.

## 1. Compose on Qwen

```bash
uv run tools/gin.py --provider qwen --url http://192.168.69.44:8188 \
  --image char_refs/pegasus_ref.png char_refs/chrys/chrys_16.webp \
  --size 2560x1088 --seed N --output tmp/<work>/m_qN.webp \
  --prompt "$(cat prompt.json) <lora:Qwen/lotf_qwen_v3.safetensors:1.0>"
```

- **References are characters only** (no earlier scene renders). For Pegasus,
  use `pegasus_ref.png`. For male Chrys, use `chrys_16` (frontal nude). For
  female and futa Chrys, use `chrys_f_02`.
- **JSON prompt** with `scene`, `subjects[]` (description / position / action),
  `style`, `lighting`, `composition`. Start the scene with the triggers
  (`lotf, pegasus, chrys.`) and the line *"Only the two people's appearances
  come from the images — the backgrounds of image 1 and image 2 are gone."*
- **Spell out canonical outfits.** Qwen invents clothes otherwise. Female
  Chrys: strapless olive-green leather corset, gold gauntlet, brown belt, dark
  brown shorts, knee boots. Add "no tail" for Pegasus.
- **Strict profile, close together.** "medium side-on shot, the camera
  perpendicular to them, both figures in exact profile… an arm's length apart"
  keeps both genitals readable in silhouette.
- Render 4-6 seeds and let the user pick. Expect the genitals to be wrong on
  every seed: oversized, pink, merged into one shape, or placed at chest
  height. That's what steps 2-3 are for.
- When `.51` is training, use the three `.44` ports.

## 2. Mark and remove the wrong anatomy

The user paints the problem areas in ivp's paint tool (green strokes, roughly
the shape the genital should have).

- **ivp paint-save overwrites the image as lossy WebP.** Copy the marked file
  aside (`*_marked.*`) for the mask, and get the clean original back by
  re-rendering the same seed on the same server. Qwen is deterministic, so
  the mask lines up (diff about 1-2 outside the strokes).
- **Remove** misplaced or merged anatomy with **base Klein** masked inpaint.
  It only removes, so it doesn't break the futa rule. Mask = green pixels,
  dilated (`MaxFilter(15)`):
  ```bash
  uv run tools/gin.py --provider klein --inpaint \
    --model Flux2/klein/fluxKleinFP8_flux2KleinBase9bFp8.safetensors \
    --mask mask.png --cfg 3.5 --steps 20 --image clean.webp \
    --prompt "the bare groins … nothing between them … the dark shadowed canvas of a tent behind"
  ```
- **When Klein rebuilds the thing you asked it to remove** (it did with the
  chest-height penises), do a **Qwen edit of a 1024 crop** instead ("Keep
  everything exactly … change only one thing: remove the two penises they
  are holding … their hands reach toward each other holding nothing"). Qwen
  redraws the whole crop slightly, so paste back the whole crop with a 24 px
  feathered edge, not just the blob.

## 3. Add the genitals, one character at a time

Futa anatomy is **Illustrious + nyl2 guy only, never Klein** (user rule).
Script: `docs/scripts/crop_inpaint.py` (writes to `<base dir>/crops/`).

```bash
uv run python docs/scripts/crop_inpaint.py <base> <marked> chr|peg m|futa <x0> <y0> 10011,10012,10013
```

- **1024×1024 crop centred on one character** (native size for Illustrious,
  no rescale). The mask is **that character's own green stroke**, slightly
  grown. The stroke sets the genital's size, angle and position. A plain
  rectangle box instead makes the model fill the box: oversized penises, or
  one floating in mid-air when the groin is hidden behind an arm.
- **Prompt per side**, booru tags: `nyl2 guy, futanari, 1girl` (or
  `1boy, male`), `nude, erection, erect penis, testicles, side view, from side,
  uncircumcised, kneeling, crotch, dark background`, plus the skin tone, then
  `<lora:SDXL/nyl2-guy-PONYv2.safetensors:0.8>`. Run 3 seeds at denoise 0.95
  and mask blur 12, and paste back through the feathered stroke mask.
- **Skin tone:** "tan skin, dark skin" turned Chrys's penis chocolate brown.
  Use "light tan skin, natural skin-toned penis matching the skin of the body",
  and put "dark skin, dark brown penis" in the negative. For Pegasus, use
  "fair skin, pale skin, pink natural skin-toned penis".
- **Don't put scene words in the prompt.** "warm lantern light" painted
  lanterns into the gap between them. Keep `lamp, lantern, fire, candle,
  object` in the negative.
- Do **Chrys first, paste the pick into the full frame, then Pegasus.** The
  script only scrubs the user's green paint (OpenCV TELEA fill) when the base
  *is* the marked image (`np.array_equal`). A looser "nearly equal" test
  re-scrubbed both strokes and smudged the first side's finished penis.

## 4. Refine

Qwen at full size, on the inpainted frame, two seeds:

> Keep image 1 exactly as it is — the same pose, composition, bodies, anatomy,
> genitals, hands, wings, lighting and background, nothing added or removed.
> *(one-line scene description)*; their penises and testicles stay exactly as
> in image 1. Only refine it: re-render it sharp and clean with fine natural
> skin texture, crisp feathers, fur and canvas, as a high quality 3d render
> like elden ring. `<lora:Qwen/lotf_qwen_v3.safetensors:1.0>`

This blends the inpaint patches into the frame without moving anything.

**Crops vs. outpaint:** if the user hands back a hand-repaired *crop*, don't
outpaint it back to 2560 (rejected as "bad"). Template-match the crop against
the original wide render (`cv2.matchTemplate`, score about 0.97), refine the
crop, resize it back to the crop's size, and feather-paste it (40 px Gaussian
side feather) onto the original background.

## 5. Animate with H3

**Use the full model** (`--engine h3`, `h3ErosMax_beta2_Q8_0.gguf`) with
`<lora:H3/PLORA_H3_V2-step00006300.safetensors:1.0>`. **`h3_turbo` silently
ignores every LoRA:** its checkpoint is ComfyUI-GGUF's Q8_CR int8 format,
whose native int8 layers never apply LoRA patches. The log still prints
`LoRAs: [...]`. See `memory/video_loras.md`. Budget about 25 minutes per
4.5 s clip at full resolution on `.51`.

**Render direct:** `--h3-upscale 1.9 --h3-attention kitchen`, which outputs
2560×1088, about 107 frames, as an AV1 master. The user picked the direct
renders over every alternative.

### Chain the beats through stills

Each beat starts on the still the previous one ends on, so the game can
hand over between clips and fall back to stills without ELITE:

| beat | engine input | output |
|---|---|---|
| transition (harden, gaze down, lean in) | I2V: `-i start_still` | clip; **its last frame becomes the next still** (`ffmpeg -sseof -0.2 … -update 1`) |
| loop (admire, rub) | FL2VA: `-i still still` | loop; ease the last 4 frames back to the start (`docs/scripts/blend_in.py N=4 --loop`, wrap jump 5 → about 1) |
| climax / touch | I2V from the loop's still | clip that holds its last frame |

### Prompt lessons

- **Closed tips:** add *"The smooth rounded head of each penis stays closed
  and intact, with only a tiny slit at its tip."* Without it, H3 turns
  head-on glans into gaping holes.
- **Angles:** say *"…jutting straight out almost horizontally, level with
  each other … neither erection rises steeply upward; both end nearly
  parallel to the ground"*. Otherwise they rise to 45-60°.
- **Order** ("she hardens first, then him"): write the halves as one shot
  with "during the first half… then, in the second half…". It's only
  partially honoured; a mid-clip guide frame forces it.
- **Living actors:** never write "their bodies stay still". It freezes
  them. Give them small motion: breathing, weight shifts, blinks, fingers
  adjusting a grip, a glance down and back up.
- **Loops that should hold still:** *"the two erections stay rigid and almost
  perfectly still"*. "Throb gently and bob" made them wiggle. (The user
  still preferred the original loops, so treat this as a per-scene call.)
- **Precum thread at the tip:** *"attached exactly at the small slit at the
  very tip of each penis head"*.

### The first-frames distortion (known, unsolved cleanly)

Every `--h3-upscale` clip warps for about 3 frames at the start (feathers,
hair and foliage reshape, then settle). The latent upscale and refine cause
it; the base render is clean. Options we tried:

- **Accept it.** This is what the user chose for the shipped clips.
- **Held start:** `H3_GUIDES_ONLY=1 … -i still still:4 still:8`, render 8
  extra frames, cut them. This keeps direct-render detail and removes the
  warp. (`H3_GUIDES_ONLY` makes every image after the first a guide, with no
  end frame.)
- **Padded upscale-video** (render base, prepend 8 clones, `--h3-upscale-video`,
  cut). This removes the warp but is **rejected**: about 18% less detail
  ("plastic"), and its refine re-paints prompt content into early frames
  (a precum thread before the tips touched).
- **NVIDIA SoL-Refiner (H3 variant): rejected.** It rewrote identities and
  erased genital anatomy.

**RIFE is a per-clip call** (`docs/scripts/rife.py` / `rife_blend.sh`): RIFE 2x plus a 1:2:1 blend back to 24 fps suited
the slow stroke loop, but the user vetoed it for fast motion.

### Motion transfer: when an approved clip has the right motion but the wrong cast

Futa-on-futa humping failed every other way:
- **Prompting:** H3 can't tell which of two women is thrusting.
- **Pasting the male clip's pixels:** the reference's wings and hair bled in.
- **Optical-flow warping:** the penises moved like snakes.
- **2D rig:** the body looked unnatural.

What worked was H3 **Ref2VA with a reference video**:
- **Inputs:** the futa still as `<Picture 1>` (identity and scene) and the approved male clip as `<Video 1>` (motion).
- **Anchors:** the still is pinned at frame 0, and at -1 too for a loop, through `MiniMaxH3AddGuide`.
- **Code:** `h3_workflows.build_ref2va(..., ref_videos=[...], anchors=[...])`. The driver is `tmp/pegasus_futa/experiment/comp/ref2va_motion.py` (`still refvideo out seed [full] [prompt_file] [start_only]`).
- **Prompt:** *"Keep their faces, bodies, wings, hair and the tent exactly as in <Picture 1>; only the motion comes from <Video 1>. Reproduce the motion of <Video 1>: ..."*
- **Upscale:** turbo outputs 1344×576, so finish with `--h3-upscale-video 1.9 --h3-upscale-refine-steps 8` and `blend_in.py ... 4 --loop`. That loader is `VHS_LoadVideoFFmpeg` now, so the AV1 masters load directly.
- **Climaxes:** pin only frame 0, so the ending can differ from the still.

### Loops that won't move: chain I2V clips

FL2VA with the same still at both ends often renders a frozen clip (motion around 0.4). I2V from the still moves. For a long loop:
1. Render two I2V clips from the still.
2. Render two short FL2VA transitions (39 frames): from the end of clip A to the start of clip B, and from the end of B back to the start of A.
3. Concatenate A → T1 → B → T2. Drop each transition's repeated first frame and crossfade 3 frames at every join and at the wrap.

The result is about 11.7 s with no snap back to the still.

### Prompt traps found here

- **"Mouth falls open in a gasp" plus semen wording** makes semen run from that open mouth. Give the receiver a closed-mouth reaction, and name the target mouth whenever liquid is mentioned.
- **Semen has to be spelled out** ("a string of white semen stretches from her lower lip to the tip...") or it renders none.
- **Stillness words** ("holds still", "keeps its size") freeze the whole clip. Say what moves, never what doesn't.

## 6. Ship

- Base stills: `src_assets/<name>.webp` (lossless), promoted with
  `tools/resize_border.py --replace --width=2560 --height=1080 --format WEBP`.
- Clip masters: `src_videos/<work>/h3_final/<name>.webm` (AV1, crf 8,
  10-bit). Game copies: `src_elite/<name>.webm`, the same AV1 file (git
  stores identical blobs once). Don't re-encode to VP9: `tools/create_videos.sh`
  transcodes `src_elite` to AV1 for `game/videos` anyway, so a VP9 copy only
  adds a lossy generation.
- `assets_gen.yml` → `interp_videos`: `images: [start_still, end_still]`
  (`repeat: false`) or `[still]` (`repeat: true`), with `condition: ELITE`.
- Script: one `<scene>_cg(stage)` label per scene that plays the clip when
  `renpy.has_image(name, exact=True)`, otherwise shows the matching still
  `with dissolve`. Loops use `scene expression`. Gate every CG on
  `lewd_enabled()`.
- Prompt records: `prompts/<name>.json` (compose prompt, seeds, inpaint
  method, user picks) and the H3 prompt files beside the masters.
- Test with the play-vn bridge: call the scene for each Chrys sex and
  screenshot every beat. Save the user's slot first if it's their session.
