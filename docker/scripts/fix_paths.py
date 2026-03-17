"""Convert Windows paths in train_raw.jsonl to container paths."""
import json
import glob
import os

for path in glob.glob("output/SB2/*/train_raw.jsonl"):
    lines = open(path, encoding="utf-8").readlines()
    out = []
    for l in lines:
        d = json.loads(l)
        d["audio"] = d["audio"].replace("D:/Qwen3-TTS", "/workspace").replace("\\", "/")
        d["ref_audio"] = d["ref_audio"].replace("D:/Qwen3-TTS", "/workspace").replace("\\", "/")
        out.append(json.dumps(d, ensure_ascii=False))
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(out) + "\n")
    print(f"{os.path.dirname(path)}: done")
