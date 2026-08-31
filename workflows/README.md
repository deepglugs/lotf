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

## Where files go

```
ComfyUI/models/
  checkpoints/      illustrious_lotf_v1.safetensors
  diffusion_models/ klein_lotf_v1_fp8.safetensors
  loras/            lotf_sdxl_v1.safetensors
                    lotf_v2_klein.safetensors
  vae/              flux2-vae.safetensors        <- Klein only
  text_encoders/    <a Klein 9B Qwen3 encoder>   <- Klein only
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
