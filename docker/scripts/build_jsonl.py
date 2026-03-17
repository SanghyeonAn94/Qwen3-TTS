"""Generate train_raw.jsonl from WAV+txt pairs in a character directory."""
import argparse
import json
import os


def build_jsonl(char_dir, output_path, ref_audio=None):
    wavs = sorted(
        f for f in os.listdir(char_dir)
        if f.lower().endswith(".wav")
    )
    if not wavs:
        print(f"No WAV files found in {char_dir}")
        return

    # Default ref_audio: first WAV in the directory
    if ref_audio is None:
        ref_audio = os.path.join(char_dir, wavs[0])

    entries = []
    skipped = []
    for wav in wavs:
        txt_name = os.path.splitext(wav)[0] + ".txt"
        txt_path = os.path.join(char_dir, txt_name)
        wav_path = os.path.join(char_dir, wav)

        if not os.path.isfile(txt_path):
            skipped.append(wav)
            continue

        with open(txt_path, "r", encoding="utf-8") as f:
            text = f.read().strip()

        if not text:
            skipped.append(wav)
            continue

        entries.append({
            "audio": wav_path,
            "text": text,
            "ref_audio": ref_audio,
        })

    os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        for e in entries:
            f.write(json.dumps(e, ensure_ascii=False) + "\n")

    print(f"{os.path.basename(char_dir)}: {len(entries)} entries written -> {output_path}")
    if skipped:
        print(f"  Skipped (empty/missing txt): {skipped}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--samples_dir", type=str, required=True, help="Parent dir containing character subdirs")
    parser.add_argument("--output_dir", type=str, required=True, help="Where to write jsonl files")
    parser.add_argument("--ref_audio", type=str, default=None, help="Override ref_audio path (default: first WAV per character)")
    args = parser.parse_args()

    for name in sorted(os.listdir(args.samples_dir)):
        char_dir = os.path.join(args.samples_dir, name)
        if not os.path.isdir(char_dir):
            continue
        output_path = os.path.join(args.output_dir, name, "train_raw.jsonl")
        build_jsonl(char_dir, output_path, args.ref_audio)


if __name__ == "__main__":
    main()
