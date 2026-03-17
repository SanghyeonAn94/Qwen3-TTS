"""Quick inference test for a fine-tuned character model."""
import argparse

import soundfile as sf
import torch
from qwen_tts import Qwen3TTSModel


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--model_path", type=str, required=True, help="Path to fine-tuned checkpoint")
    parser.add_argument("--speaker", type=str, required=True, help="Speaker name used during fine-tuning")
    parser.add_argument("--text", type=str, required=True, help="Text to synthesize")
    parser.add_argument("--output", type=str, default="output.wav", help="Output wav path")
    parser.add_argument("--device", type=str, default="cuda:0")
    args = parser.parse_args()

    tts = Qwen3TTSModel.from_pretrained(
        args.model_path,
        device_map=args.device,
        dtype=torch.bfloat16,
        attn_implementation="sdpa",
    )

    wavs, sr = tts.generate_custom_voice(
        text=args.text,
        speaker=args.speaker,
    )
    sf.write(args.output, wavs[0], sr)
    print(f"Saved: {args.output} (sr={sr})")


if __name__ == "__main__":
    main()
