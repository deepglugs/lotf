"""RIFE-interpolate an existing clip on ComfyUI: python rife.py in.mp4 out.mp4 [mult] [--loop]
--loop drops the final frame (FL2VA loops end on the start frame, so the
wrap would otherwise show it twice)."""
import json, sys, time, uuid, urllib.request, subprocess, os
URL = "http://192.168.69.51:8188"
src, dst = sys.argv[1], sys.argv[2]
mult = int(sys.argv[3]) if len(sys.argv) > 3 and not sys.argv[3].startswith("--") else 2
loop = "--loop" in sys.argv
name = f"rife_{uuid.uuid4().hex[:8]}{os.path.splitext(src)[1]}"
subprocess.run(["curl", "-s", "-F", f"image=@{src};filename={name}", "-F", "type=input", f"{URL}/upload/image"], check=True, stdout=subprocess.DEVNULL)
fps = float(subprocess.check_output(["ffprobe", "-v", "error", "-select_streams", "v", "-show_entries", "stream=r_frame_rate", "-of", "csv=p=0", src]).decode().strip().split("/")[0])
wf = {
 "1": {"class_type": "VHS_LoadVideoFFmpeg", "inputs": {"video": name, "force_rate": 0, "custom_width": 0, "custom_height": 0,
       "frame_load_cap": 0, "start_time": 0}},
 "2": {"class_type": "RIFE VFI", "inputs": {"ckpt_name": "rife49.pth", "clear_cache_after_n_frames": 5, "ensemble": True,
       "fast_mode": False, "frames": ["1", 0], "multiplier": mult, "scale_factor": 1}},
 "3": {"class_type": "VHS_VideoCombine", "inputs": {"images": ["2", 0], "frame_rate": fps * mult, "loop_count": 0,
       "filename_prefix": "rife_out", "format": "video/av1-webm", "pingpong": False, "save_output": True,
       "pix_fmt": "yuv420p10le", "crf": 8, "input_color_depth": "8bit", "save_metadata": False}},
}
req = urllib.request.Request(f"{URL}/prompt", data=json.dumps({"prompt": wf}).encode(), headers={"Content-Type": "application/json"})
pid = json.load(urllib.request.urlopen(req))["prompt_id"]
print("queued", pid, flush=True)
while True:
    h = json.load(urllib.request.urlopen(f"{URL}/history/{pid}"))
    if pid in h and h[pid].get("status", {}).get("completed"):
        break
    if pid in h and h[pid].get("status", {}).get("status_str") == "error":
        sys.exit("error: " + json.dumps(h[pid]["status"])[:2000])
    time.sleep(5)
g = h[pid]["outputs"]["3"]["gifs"][0]
tmp = dst + ".raw.webm"
urllib.request.urlretrieve(f"{URL}/view?filename={g['filename']}&subfolder={g['subfolder']}&type={g['type']}", tmp)
n = int(subprocess.check_output(["ffprobe", "-v", "error", "-count_frames", "-select_streams", "v", "-show_entries", "stream=nb_read_frames", "-of", "csv=p=0", tmp]).decode())
if loop:
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", tmp, "-frames:v", str(n - 1), "-c:v", "libsvtav1", "-crf", "8", "-preset", "6", "-pix_fmt", "yuv420p10le", dst], check=True)
    os.remove(tmp)
else:
    os.replace(tmp, dst)
print("wrote", dst, "frames", n - 1 if loop else n, "fps", fps * mult)
