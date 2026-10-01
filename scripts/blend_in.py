"""Hide H3's first-frame pop: fade from the exact start still into the clip.
usage: blend_in.py clip.webm start_still.png out.webm [N=4] [--loop]
--loop also eases the last N frames back to the still so the wrap is exact.
Streams frames through ffmpeg (raw rgb48), writes AV1 crf 8 10-bit."""
import sys, subprocess, numpy as np
from PIL import Image
clip, still, out = sys.argv[1:4]
N = int(sys.argv[4]) if len(sys.argv) > 4 and not sys.argv[4].startswith("--") else 4
loop = "--loop" in sys.argv
probe = subprocess.check_output(["ffprobe","-v","error","-select_streams","v","-count_frames","-show_entries","stream=width,height,nb_read_frames,r_frame_rate","-of","csv=p=0",clip]).decode().strip().split(",")
W, H, fps, n = int(probe[0]), int(probe[1]), probe[2], int(probe[3])
S = np.asarray(Image.open(still).convert("RGB").resize((W, H), Image.LANCZOS), np.float32) * 257.0
dec = subprocess.Popen(["ffmpeg","-loglevel","error","-i",clip,"-f","rawvideo","-pix_fmt","rgb48le","-"], stdout=subprocess.PIPE)
enc = subprocess.Popen(["ffmpeg","-loglevel","error","-y","-f","rawvideo","-pix_fmt","rgb48le","-s",f"{W}x{H}","-r",fps,"-i","-",
                        "-c:v","libsvtav1","-crf","8","-preset","6","-pix_fmt","yuv420p10le",out], stdin=subprocess.PIPE)
fsz = W * H * 3 * 2
for i in range(n):
    buf = dec.stdout.read(fsz)
    if len(buf) < fsz: break
    f = np.frombuffer(buf, np.uint16).reshape(H, W, 3).astype(np.float32)
    w = 1.0
    if i < N: w = i / N                      # frame 0 = exact still
    if loop and i >= n - N: w = min(w, (n - 1 - i) / N)   # last frame = exact still
    o = S * (1 - w) + f * w
    enc.stdin.write(np.clip(o, 0, 65535).astype(np.uint16).tobytes())
enc.stdin.close(); enc.wait(); dec.wait()
print("wrote", out, n, "frames, N =", N, "loop" if loop else "")
