"""One side at a time: 1024x1024 crop around one character, inpaint inside that
side's green stroke, 3 seeds. usage: crop_inpaint.py base marked side(peg|chr) variant(m|futa) x0 y0 seeds"""
import sys, subprocess, numpy as np, cv2, threading
from PIL import Image, ImageFilter
base_p, marked_p, side, variant = sys.argv[1:5]; x0, y0 = int(sys.argv[5]), int(sys.argv[6]); seeds = [int(s) for s in sys.argv[7].split(",")]
B = np.asarray(Image.open(base_p).convert("RGB")); M = np.asarray(Image.open(marked_p).convert("RGB")).astype(int)
g = ((M[...,1] > 110) & (M[...,1]-M[...,0] > 40) & (M[...,1]-M[...,2] > 40)).astype(np.uint8)
if np.array_equal(B.astype(int), M): B = cv2.inpaint(B, cv2.dilate(g, np.ones((9,9),np.uint8))*255, 7, cv2.INPAINT_TELEA)
n, lab, st, _ = cv2.connectedComponentsWithStats(cv2.dilate(g, np.ones((9,9),np.uint8)))
comps = sorted([i for i in range(1, n) if st[i,4] > 2000], key=lambda i: st[i,0])
# pick the groin stroke of this side (leftmost low stroke = pegasus, rightmost = chrys)
low = [i for i in comps if st[i,1] + st[i,3] >= 700]
ci = low[0] if side == "peg" else low[-1]
import os
crop = Image.fromarray(B[y0:y0+1024, x0:x0+1024]); W = os.path.join(os.path.dirname(base_p) or ".", "crops") + "/"; os.makedirs(W, exist_ok=True)
tag = f"{W}{variant}_{side}"
crop.save(tag + "_crop.png")
mk = Image.fromarray(((lab[y0:y0+1024, x0:x0+1024] == ci) * 255).astype(np.uint8)).filter(ImageFilter.MaxFilter(11))
mk.convert("RGB").save(tag + "_mask.png")
L = "<lora:SDXL/nyl2-guy-PONYv2.safetensors:0.8>"
if side == "peg":
    subj, skin = "futanari, 1girl", "fair skin, pale skin, pink natural skin-toned penis"
else:
    subj = "futanari, 1girl" if variant == "futa" else "1boy, male"
    skin = "light tan skin, natural skin-toned penis matching the skin of the body, light brown penis"
P = (f"nyl2 guy, {subj}, nude, erection, erect penis, testicles, side view, from side, uncircumcised, {skin}, kneeling, crotch, "
     f"dark background, close-up, detailed skin, high quality 3d render, masterpiece, best quality {L}")
NEG = ("lowres, bad anatomy, worst quality, low quality, watermark, text, multiple penises, deformed penis, flaccid, soft penis, circumcised, "
       "dark skin, black skin, dark brown penis, very dark penis, lamp, lantern, fire, candle, object, hand, fingers, pussy, vagina, gigantic penis, huge testicles")
def run(seed, port):
    out = f"{tag}_{seed}.png"
    subprocess.run(["uv","run","tools/gin.py","--provider","sdxl","--inpaint","--url",f"http://192.168.69.44:{port}","--image",tag+"_crop.png",
                    "--mask",tag+"_mask.png","--denoise","0.95","--mask-blur","12","--seed",str(seed),"--prompt",P,"--negative",NEG,"--output",out+".raw.png"],
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
    res = Image.open(out+".raw.png").convert("RGB").resize((1024,1024), Image.LANCZOS)
    pm = mk.filter(ImageFilter.MaxFilter(9)).filter(ImageFilter.GaussianBlur(6))
    Image.composite(res, crop, pm).save(out); print("wrote", out, flush=True)
ts = [threading.Thread(target=run, args=(s, p)) for s, p in zip(seeds, (8188, 8189, 8190))]
[t.start() for t in ts]; [t.join() for t in ts]
