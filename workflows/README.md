# Example ComfyUI workflows

Working pipelines for the LOTF character models — see
[`../modding.md`](../modding.md#8-art-models--lotf-character-loras--merges) for
the trigger contract and where to download the models themselves.

These are **API-format** workflows (the numbered-node JSON that ComfyUI's
`/prompt` endpoint accepts), exported from the tooling that generates the game's
own art, so they match a known-good configuration rather than being written by
hand. They use **only core ComfyUI nodes** — no custom node packs.

Every workflow here has been executed against ComfyUI and verified to run to a
saved image.

| Workflow | What it does |
|---|---|
| `illustrious_lotf_txt2img.json` | Illustrious merge → image. Simplest starting point. |
| `klein_lotf_txt2img.json` | Klein merge → image. |
| `klein_lotf_inpaint.json` | Klein merge → **masked inpaint**. Needs an uploaded `input.png` + `mask.png`. |
| `illustrious_base_plus_lotf_lora.json` | Stock Illustrious + the LoRA, for stacking with other concept LoRAs. |
| `klein_base_plus_lotf_lora.json` | Stock Klein + the LoRA, same idea. |
| `qwen_lotf_txt2img.json` | Qwen-Image 2.1 (GGUF) + `lotf_qwen_v3` → image. **Prompt is a JSON object** (see below). Needs the ComfyUI-GGUF node pack. |
| `flux3_klein_lotf_txt2img.json` | FLUX 3 Image Klein (step-distilled) + `lotf_flux3_klein_v3` → image. Core nodes only; needs ComfyUI ≥ 0.41. |

## Where files go

```
ComfyUI/models/
  checkpoints/      illustrious_lotf_v1.safetensors
  diffusion_models/ klein_lotf_v1_fp8.safetensors
  diffusion_models/ qwen-image-2.1-Q8_0.gguf      <- Qwen only
  diffusion_models/ flux3_image_klein_sd_bf16.safetensors   <- FLUX 3 Klein only
  loras/            lotf_sdxl_v1.safetensors
                    lotf_v2_klein.safetensors
                    lotf_qwen_v3.safetensors
                    lotf_flux3_klein_v3.safetensors
  vae/              flux2-vae.safetensors        <- Klein and FLUX 3 Klein
                    qwen_image_2.1_vae_bf16.safetensors  <- Qwen only
  text_encoders/    <a Klein 9B Qwen3 encoder>   <- Klein only
                    qwen3vl_8b_bf16.safetensors  <- Qwen only
                    qwen3vl_4b_bf16.safetensors  <- FLUX 3 Klein only
```

The workflows reference models by **bare filename**, assuming they sit in the
root of each folder. If you keep models in subfolders, edit the `ckpt_name` /
`unet_name` / `lora_name` strings to match (e.g. `mystuff/illustrious_lotf_v1.safetensors`).

The **Illustrious** workflows are self-contained — that checkpoint carries its
own VAE and text encoder, so the one file is all you need.

## Klein needs two extra files

The Klein workflows load the diffusion model, VAE, and text encoder separately.
Two of those come from elsewhere:

**VAE** (~336 MB), exact filename match:

```
https://huggingface.co/Comfy-Org/flux2-dev/resolve/main/split_files/vae/flux2-vae.safetensors
```
→ `ComfyUI/models/vae/flux2-vae.safetensors`

**Text encoder** — Klein 9B uses a **Qwen3** encoder. The official weights are at
[`black-forest-labs/FLUX.2-klein-9B`](https://huggingface.co/black-forest-labs/FLUX.2-klein-9B)
under `text_encoder/`, but they ship in multi-shard *diffusers* layout, which
ComfyUI's `CLIPLoader` cannot read — you need a single-file build. Several
community repackages exist in different precisions; search HuggingFace for
`flux2-klein-9b text encoder` and pick one that fits your VRAM.

The workflows name it as:

```json
"clip_name": "qwen38BFluxKlein9BTE_38b.safetensors"
```

That is just the filename this project happens to use — **edit it to match
whatever you downloaded.**

## Qwen needs three extra files and one node pack

The Qwen workflow is the project's own generation graph (the Comfy-Org
`image_qwen_image_2_1_image_edit` template with the refs removed) and needs
**ComfyUI 0.37 or newer** (`TextEncodeQwenImage21` / `QwenImage21Cache`) plus the
[ComfyUI-GGUF](https://github.com/city96/ComfyUI-GGUF) node pack for
`UnetLoaderGGUF` — the one non-core node in this collection.

- **Diffusion model** — `qwen-image-2.1-Q8_0.gguf` from
  [`abenzerps/Qwen-Image-2.1-GGUF`](https://huggingface.co/abenzerps/Qwen-Image-2.1-GGUF)
  → `ComfyUI/models/diffusion_models/` (a smaller quant works too; edit `unet_name`).
- **VAE** — `qwen_image_2.1_vae_bf16.safetensors` (same repo, or the Comfy-Org
  Qwen-Image 2.1 split files) → `ComfyUI/models/vae/`.
- **Text encoder** — a single-file **Qwen3-VL 8B** build (`qwen3vl_8b_bf16.safetensors`;
  ~16 GB, loaded with `CLIPLoader` type `qwen_image`) → `ComfyUI/models/text_encoders/`.
  A w4a8 quant also works on 24 GB cards; edit `clip_name` to match what you have.

Sampling is 25 steps, euler/simple, **cfg 1.0** (no negative prompt), at 832×1216.
The LoRA goes through `LoraLoaderModelOnly` at strength 1.0.

**Prompt format.** `lotf_qwen_v3` was trained on JSON captions, so the `prompt`
string in the workflow is a JSON object, not prose:

```json
{"scene": "lotf, ceraphina. A sunlit stone library ...",
 "subjects": [{"description": "ceraphina, an adult woman with fair ivory skin, ...",
               "position": "standing at a reading lectern, facing the viewer",
               "action": "turning a page, a calm half-smile"}],
 "style": "high quality 3d render like elden ring, cinematic, photoreal skin and materials",
 "lighting": "warm afternoon sunlight through the windows", "mood": "quiet, studious",
 "composition": "three-quarter portrait, eye level"}
```

Keep `lotf, <character>` at the start of `scene` and the character token at the
start of each `description`. Prose prompts only half-trigger the likeness.

## FLUX 3 Klein needs three files and a recent ComfyUI

`flux3_klein_lotf_txt2img.json` uses only core nodes but needs **ComfyUI 0.41 or
newer** (native FLUX 3 support: `CLIPLoader` type `flux3`). All three base files
are in BFL's own ComfyUI repack,
[`black-forest-labs/flux-3-image-klein-comfy`](https://huggingface.co/black-forest-labs/flux-3-image-klein-comfy)
(gated; accept the FLUX Kommunity license):

- **Diffusion model** — `diffusion_models/flux3_image_klein_sd_bf16.safetensors`
  (11 GB, the step-distilled model) → `ComfyUI/models/diffusion_models/`. The
  `int8_convrot` (5.8 GB) and `nvfp4` builds also work on 8-16 GB cards; edit
  `unet_name`.
- **Text encoder** — `text_encoders/qwen3vl_4b_bf16.safetensors` (8.9 GB; the
  `fp8_scaled` build from `Comfy-Org/Qwen3-VL` also works) →
  `ComfyUI/models/text_encoders/`.
- **VAE** — `vae/flux2-vae.safetensors`, the same Flux2 VAE the Klein workflows use.

Sampling is 16 steps, euler/simple, **cfg 1.0** (no negative prompt), at 832×1216.
The LoRA goes through a plain `LoraLoader` (model + clip) at strength 1.0. The
example prompt is the same JSON object shape as the Qwen workflow; plain
`lotf, <character>, <description>` prose also works on this model. If you load
the undistilled `flux3_image_klein_bf16` instead, use 30 steps and cfg 3.5.

## Running one

**Web UI:** *Workflow → Open* and pick the `.json`. (Recent ComfyUI frontends
import API-format graphs; if yours refuses, use the API route.)

**API:**

```bash
curl -X POST http://127.0.0.1:8188/prompt \
  -H 'Content-Type: application/json' \
  -d "{\"prompt\": $(cat illustrious_lotf_txt2img.json)}"
```

The inpaint workflow additionally expects `input.png` and `mask.png` to already
be uploaded to ComfyUI's input folder (in the mask, **white = repaint**,
black = keep).

## Prompts

Each workflow ships with a working example prompt using the
`lotf, <character>, <description>` trigger form. Per-character tokens, canonical
looks, and the base-model priors worth prompting around are documented in
[`../modding.md`](../modding.md#8-art-models--lotf-character-loras--merges).
