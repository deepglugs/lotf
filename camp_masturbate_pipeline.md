# Camp masturbation CGs and videos (Qwen stills + MiniMax H3)

The recipe behind the camp **Masturbate** action (`camp_actions.rpy`): one solo
CG per camp × Chrys shape (5 camps × male/female/futa = 15 stills), and two
ELITE videos per still — a seamless **masturbation loop** and a **climax** —
both animated on the full-body shot. Built 2026-09-30 → 10-03.

The idea in one line: **the approved full-body CG is the first frame of both
clips; the loop ends on it too, the climax ends on a still edited from it, and
any bad penis is redrawn on the still (qwen_penis_edit_v1) before H3 sees it.**

```
Qwen compose (bf16 encoder) ─► genital/hand fix ─► Qwen refine ─► still CG (src_assets/)
                                                                     │
                     qwen_penis_edit_v1 on the still if the penis is off
                                                                     │
                     climax end frame: Qwen edit of the still (cum / afterglow)
                                                                     │
  loop    still ──► still          static, turbo, 96 f, seamless     │
  climax  still ──► climax frame   static, turbo, 96–121 f           │
                                                                     ▼
        motion DRAFTS at base res (no --h3-upscale) → user approves motion
                                                                     ▼
        finals: same seeds + --h3-upscale 1.9 --h3-upscale-refine-steps 2
                                                                     │
                       AV1 CRF 18 → src_elite/ → ELITE=1 HW_QP=18 make videos
```

Scratch work lives in `tmp/camp_masturbate/` (stills) and
`tmp/camp_mast_video/` (videos); every approved still has a prompt record in
`prompts/camp_masturbate_<camp>_<sex>.json`.

## 1. The still CGs

### Compose (Qwen)

`tmp/camp_masturbate/compose.py` — `gin.py --provider qwen`, 2560x1088 native,
`lotf_qwen_v3` 1.0, JSON prompt (`scene` / `subjects[]` / `style` / `lighting`
/ `composition`), one character ref (`chrys_16.webp` male, `chrys_f_02.webp`
female/futa). Describe the camp in text — never feed a camp render as a ref.

- **Use the bf16 text encoder.** `.44` auto-picks the small
  `qwen3vl_8b_w4a8_heretic` encoder; it ignores "completely naked", boots-off and
  hand placement. Pass `--qwen-te qwen3vl_8b_bf16.safetensors` (compose.py
  `--te`). Slower (~73 s vs ~20 s on .44) but it is what made the Pegasus scene
  compose cleanly on .51.
- **Frontal seated poses.** "sitting … facing the camera, back against
  <prop>, knees raised and parted" plus "wide frontal shot … centred and
  symmetrical" fixed most tangled limbs.
- **Female Chrys keeps her corset.** `lotf_qwen_v3` bakes it into the `chrys`
  1girl identity; wording and no-ref renders do not remove it (see memory
  `feedback_qwen_chrys_f_corset_baked`).

### Fix the anatomy

| Problem | Fix that worked |
|---|---|
| **Penis (any shot)** | **`qwen_penis_edit_v1`** (Qwen edit LoRA, deployed 2026-10-02): `gin.py --provider qwen --image <still> --prompt "Redraw his penis as an erect circumcised penis with natural testicles, anatomically correct and matching his skin tone. Keep everything else in the image unchanged. <lora:Qwen/qwen_penis_edit_v1.safetensors:1.0>"` (futa: "Redraw her penis as …"; flaccid comes out long — try 0.8). Replaces the nyl2 route below. |
| Female corset | Klein inpaint box over the corset → "bare torso, full bare breasts, bare waist" (`corset_off.py`); keep the box top above the cups |
| Fingers on a vulva | Illustrious booru inpaint, no nyl2, dn 0.8 (`vulva_inpaint.py`) |
| Penis / grip (old route) | nyl2 (Illustrious + `nyl2-guy` 0.8) at dn 0.75 over Qwen's layout (`nyl_inpaint.py`) — or the user's hand repair in ComfyUI |
| User marks (green paint) | build the mask from the paint; pre-fill the paint with ringed-skin median before a partial-denoise inpaint (`nyl_mask_inpaint.py`), or Klein masked inpaint for fingers |
| Hollow bracer cuff / detached hand | Klein inpaint the bracer end + hand base ("wrist coming out of the end of the bracer and flowing into the back of her hand") |
| Patch seams / hands | Qwen "keep image 1 exactly … only refine it" pass (`refine.py`) |

- **Hand-edited crops go back with `paste_back.py`** (SIFT + RANSAC locates the
  crop, feathered paste). A raw `inpaint_target` output is a 0.8×-box context
  crop at ~1.8×: paste it at its known crop rectangle instead.
- **Sometimes the raw Qwen frame wins** — beach male and male shore shipped
  untouched.
- **i2k is not the refine** — it de-ages faces, plasticises skin and drops the
  grade. Use the Qwen refine.
- **Gate with /review-image** (≥90) before showing the user; show only those.

## 2. The two clips (current recipe)

All turbo: `--engine h3_turbo --h3-camera static --h3-attention kitchen`,
1344x576 base → `--h3-upscale 1.9` → 2560x1088, 24 fps. **H3 runs on .51 only.**
The full-body CG is 2560x1088 — the clip aspect — so no cropping or guides.

| Clip | Frames | In → out | Plays | Prompt core |
|---|---|---|---|---|
| **loop** | 96 (4.4 s) | still → **same still** | `repeat: true` under the body-beat narration | the stroking/rubbing, "static camera, locked framing" |
| **climax** | 96–121 | still → **climax still** | once, holds its last frame | build-up, the climax, then relaxing |

- **Loop:** first == last == the CG, so it repeats seamlessly. Male/futa: "He
  moves his hand rapidly up and down the shaft of his penis, pumping it hard and
  fast in full strokes … his hand never stops moving". Female: slow wording
  ("her fingers moving slowly and gently in small soft circles … her hand never
  moves quickly") — the user rejected fast rubbing.
- **Climax end frame:** a Qwen edit of the still. Male/futa: "Add thick ropes of
  white semen that have just squirted from the tip of his penis, dripping down
  over the head and onto his fist … Keep everything else in image 1 exactly the
  same" (Illustrious cum inpaint reshaped the glans). Female: an afterglow edit
  (head back, eyes closed, flushed, hand resting). Check the edit did not
  reframe the body — full-frame Qwen edits can drift; reroll if it moved.
- **Climax prompt:** "The smooth rounded head of his penis stays closed and
  intact, with only a tiny slit at its tip … thick ropes of white semen squirt
  from the small slit in three short pulses, landing low …, then his body goes
  slack". Female: the orgasm LoRA's trigger phrases ("strong orgasmic
  contractions visibly tightening and releasing rhythmically", "falls back
  into a relaxed state, audibly catching her breath") with the slow wording.
- **Name the accessories** in both prompts (bracers, corset, boots) — between
  pinned frames H3 invents ornate gold filigree and laced corsets.
- **Approve motion on base-res drafts first.** Drop `--h3-upscale` (1344x576,
  minutes), post, get approval; only then render finals with the same seed +
  `--h3-upscale 1.9 --h3-upscale-refine-steps 2`. Same seed → same base sample;
  check final-vs-draft mean diff (≈2 good; ≈5 → look, the refine moved
  something). Don't use `--h3-upscale-video` on a draft (~18% less detail, it
  re-paints content).
- **Tip deformation:** add "his glans stays smooth, round and firmly closed
  with only a tiny slit … it never opens, stretches or deforms" and roll seeds.
- **Check every frame for text.** Turbo has invented glyphs / a watermark logo
  over a hand. Turbo takes no `--negative`; reroll the seed and add "A clean,
  unmarked frame showing only …".

## 3. Deliver

1. Masters: AV1 CRF 10 10-bit `.webm` in `tmp/camp_mast_video/`.
2. Game sources: AV1 CRF 18 →
   `src_elite/camp_masturbate_<camp>_<sex>_loop.webm` and `…_climax.webm`.
3. `assets_gen.yml` `interp_videos` (`condition: ELITE`): the loop with images
   `[still]`, `repeat: true`; the climax with `[still, …_climax_end.webp]`,
   `repeat: false` (the end still is extracted from the clip).
4. `ELITE=1 HW_QP=18 make videos` (default QP 28 is too lossy). Check first
   which `src_elite` clips are missing from `game/videos` — make encodes all of
   them.
5. Scene wiring: the loop under the body-beat lines, the climax on the climax
   line (`camp_actions.rpy`, `camp_masturbate_cg`). Falls back to the still.

## History: the close-up recipe (pilots, superseded)

The first three videos (beach female, beach male, shore futa, still installed
as `camp_masturbate_<camp>_<sex>_vid`) were one spliced clip: push-in to a
cropped close-up guide → 3 s cum/orgasm clip → rise past a torso guide to a face
guide. It worked but cost a lot of guide fixing. What it taught:

- **The close-up guide decides the penis.** A guide with the hand beside the
  shaft produced a bad penis in every engine, base model and LoRA tried.
- **Crop wide enough to keep limbs attached** — a tight crop cut the wrist off
  and the bracer read as an empty cuff with the hand beside it.
- **Torso guides pin accessories** (`-i start torso.png:96 face.png`); add
  matching cum to them if the clip starts on the cum frame.
- **The crotch shot stays ≤ 5 s** (user rule) — the first build spent ~13 s
  there. Shorten a pinned clip by rendering fewer frames, never by trimming.
- **Stroke motion comes from the wording on turbo** (static turbo loop: local
  motion 5–8; full H3 + LoRAs: 1.1).
- **The optical-flow "local motion" number is only valid for close-ups.** On a
  full-body frame the hand is a few percent of the pixels and the metric reads
  ~0.1 for a loop the user saw stroking fine. Judge full-body motion by eye (or
  crop to the hand before measuring); never call a clip frozen from the number.

## Things that did not work

- **LoRAs on turbo** — silent no-op (`minimaxH3TurboGGUF` is int8 convrot).
- **Full H3 + HMPenis v2 + Handjob Helper** — near-frozen hand (local motion
  1.1). Handjob Helper does apply on ErosMax (A/B diff 2.6–3.2) but the user
  preferred turbo loops.
- **Base-model swap** (ErosMax / SparseRef15 / stock FP8 / PinkCherry, same
  seed + LoRAs): FP8 moved most (4.4) but swallowed the penis; PinkCherry
  cleanest but stiffest (1.7). None fixed a bad guide.
- **Orgasm LoRA 0.6 + slow wording on the full engine** — froze (0.03).
- **nyl2 over Qwen's oversized penis** (box sets size) and **Klein removal →
  nyl2** — 22 attempts on one frame, none kept.
- **qwen21_vagina_v1** LoRA — no usable female frame; corset stayed on.

## Server notes

- `.51`: H3 (turbo, ErosMax Q8, SparseRef15 Partial-INT8, stock FP8, PinkCherry
  Q8 in `SwarmUI/Models/unet`), Qwen bf16 encoder. Don't use while training.
- `.44`: Qwen (3 ports, incl. `qwen_penis_edit_v1`), Klein, Illustrious. Run
  all stills work here.
- Civitai downloads: `CIVITAI_TOKEN` is in `~/.bashrc` but not exported; resume
  dropped transfers with `curl -C -`, and size-check before installing (a 404
  body once landed under a model filename).
- Never `pkill -f` a pattern that also appears in your own shell command;
  remove only your own ComfyUI jobs (`POST /queue {"delete":[id]}`).
