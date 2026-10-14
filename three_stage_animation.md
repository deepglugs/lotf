# Three-stage animations (intro → loop → climax)

The house pattern for animating an explicit scene: three ELITE clips built around one approved
still. The base build ships the stills only; ELITE builds play the clips over the same lines.

| Stage | Plays | First frame → last frame | Holds on |
|---|---|---|---|
| **intro** | once (non-looping) | intro start still → **the scene still** | the scene still |
| **loop** | repeats seamlessly until the line advances | **the scene still** → **the scene still** | — |
| **climax** | once (non-looping) | **the scene still** → climax end still | the climax end still |

**Only the loop loops.** The intro and the climax are one-shots that hold their last frame.

Every clip joins the next on the same frame. That keeps the hand-offs invisible whenever the player
clicks, even if a one-shot has already finished and is holding.

Used by:
- the camp Masturbate action (`camp_actions.rpy`)
- Ceraphina's tent walk-in (`cera_melon_walkin_cg`)
- Pegasus's futa arc
- Nashoba's lessons
- the Ambrosia quest (planned, `TODO/chapter_3/ambrosia.md`)

## The stills

| File (`src_assets/`, lossless webp) | Role |
|---|---|
| `<name>.webp` | **The scene still.** The loop's first and last frame. It is also the base-build CG for the intro and loop beats. |
| `<name>_intro_start.webp` | The intro's first frame: the beat before the act (hands elsewhere, not yet touching, not yet hard). Make it as an edit of the scene still so the framing matches. |
| `<name>_climax_end.webp` | The climax's last frame: cum, afterglow. Make it as an edit of the scene still. **It sets the volume** (a heavy cum frame gives a jet whatever the prompt says). It is also the base-build CG for the climax beat. |

Older sets name the end still after its content (`_cum`, `_after`), and that's fine. `assets_gen.yml`
says which still is which. If a scene has a natural before/after pair (Ambrosia's stroke → facial),
the "after" still can serve as the climax end frame.

A scene with no separate "before" pose skips the intro. The loop and climax alone still work, and every
call is guarded (see below).

## The clips

All three are rendered with MiniMax H3 on `.51`, at 2560x1088 to match the CGs.

| Clip | Input frames | Notes |
|---|---|---|
| `<name>_intro` | `-i <intro_start> <still>` (first + last) | ~121 frames; it must land exactly on the still |
| `<name>_loop` | `-i <still> <still>` | first == last; ease the wrap (`docs/scripts/blend_in.py N=4 --loop`). If FL2VA freezes, chain I2V clips (two-character doc) |
| `<name>_climax` | `-i <still> <climax_end>` | full `h3` + `MH3_Cum_05b` for spurts (LoRAs are a no-op on turbo) |

Production rules (details in the pipeline docs below):
- Approve motion on **base-res drafts** (no `--h3-upscale`). Then render the finals with the same seed
  and upscale.
- **One render queue on `.51`.** Concurrent `gen_video.py` jobs cross-wire their uploaded frames.
- Drafts go in `tmp/<work>/`. Masters are AV1 lossless (CRF ≤ 10, 10-bit `.webm`).
- Game copies go in `src_elite/<name>_{intro,loop,climax}.webm`. Never top-level `src_videos`.
- Fix anatomy on the **still** before H3 sees it, because every clip copies the still faithfully. If
  you fix the still later, re-render all three clips.

## Shipping

`assets_gen.yml` → `interp_videos`. Each clip is ELITE-only. `repeat` is `false` for intro and climax,
and `true` only for the loop:

```yaml
    <name>_intro.webm:
        images:
            - legacy_of_the_fallen/game/images/<name>_intro_start.webp
            - legacy_of_the_fallen/game/images/<name>.webp
        repeat: false
        condition: ELITE
    <name>_loop.webm:
        images:
            - legacy_of_the_fallen/game/images/<name>.webp
        repeat: true
        condition: ELITE
    <name>_climax.webm:
        images:
            - legacy_of_the_fallen/game/images/<name>.webp
            - legacy_of_the_fallen/game/images/<name>_climax_end.webp
        repeat: false
        condition: ELITE
```

`tools/gen_video_rpy.py` turns each entry into
`image <name>_<stage> = Movie(start_image=<first>, play=..., image=<last>, loop=<repeat>)`. A
non-looping Movie shows `image` (the last still) once it ends, which gives the hold.

- Encode with `ELITE=1 HW_QP=18 make videos` (the default QP 28 is too lossy).
- Stills you have **replaced** need `tools/resize_border.py ... --replace`. Otherwise `game/images`
  keeps the old file and the Movie `start_image` shows stale art.

## Scene wiring

One `<scene>_cg(stage)` label per scene. Inside it, `renpy.has_image(name, exact=True)` is the ELITE
check, and the matching still is the fallback. Switch clips on narration lines: the intro on the
opening line, the loop under the body beat, the climax on the climax line.

```renpy
label <scene>_cg(stage="loop"):
    if stage == "intro":
        if renpy.has_image("<name>_intro", exact=True):
            scene expression "<name>_intro"
        else:
            scene expression "<name>" with dissolve
    elif stage == "loop":
        if renpy.has_image("<name>_loop", exact=True):
            scene expression "<name>_loop"
        # base build: the still from the intro beat stays up
    elif renpy.has_image("<name>_climax", exact=True):
        scene expression "<name>_climax"
    else:
        scene expression "<name>_climax_end" with dissolve
    return
```

- **Dissolve only into the first CG.** Clip-to-clip switches need no transition because the frames
  already match.
- Gate every CG on `lewd_enabled()` (plus the scene's own content flags).
- Test both builds. In ELITE, every hand-off should be seamless. In the base build, the stills should
  change on the same lines.

## Checklist per scene

- [ ] Scene still approved (`src_assets/<name>.webp` + `prompts/<name>.json`)
- [ ] Intro start still (edit of the scene still), unless the scene skips its intro
- [ ] Climax end still (edit of the scene still; keep the cum light)
- [ ] Intro, loop and climax drafts at base res: user approves the motion
- [ ] Finals (same seeds, upscaled), AV1 masters, `src_elite/` copies
- [ ] `assets_gen.yml` entries (`repeat: true` on the loop only, `condition: ELITE`)
- [ ] `<scene>_cg(stage)` label wired to the narration, still fallbacks
- [ ] Tested in the base and ELITE builds

## See also

- [Camp Masturbation CGs & Videos](camp_masturbate_pipeline.md): the solo recipe, with loop and climax
  prompts, glans-sway screening, pinned stills and the optional intro clip
- [Two-Character CGs & Animation](two_character_cg_pipeline.md): two-figure scenes, full H3 + PLORA,
  chained I2V loops and prompt traps
