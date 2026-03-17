#!/bin/bash
# Usage: ./prepare_and_finetune.sh <CHARACTER_NAME> <RAW_JSONL>
# Example: ./prepare_and_finetune.sh EVA /workspace/samples/SB2/EVA/train_raw.jsonl
set -e

CHARACTER=${1:?"Usage: $0 <CHARACTER_NAME> <RAW_JSONL>"}
RAW_JSONL=${2:?"Usage: $0 <CHARACTER_NAME> <RAW_JSONL>"}

DEVICE="${DEVICE:-cuda:0}"
TOKENIZER_MODEL_PATH="${TOKENIZER_MODEL_PATH:-Qwen/Qwen3-TTS-Tokenizer-12Hz}"
INIT_MODEL_PATH="${INIT_MODEL_PATH:-Qwen/Qwen3-TTS-12Hz-1.7B-Base}"

TRAIN_JSONL="/workspace/output/${CHARACTER}/train_with_codes.jsonl"
OUTPUT_DIR="/workspace/output/${CHARACTER}/model"

BATCH_SIZE="${BATCH_SIZE:-2}"
LR="${LR:-2e-5}"
EPOCHS="${EPOCHS:-10}"

mkdir -p "/workspace/output/${CHARACTER}"

echo "=== [1/2] Preparing data for ${CHARACTER} ==="
python /workspace/finetuning/prepare_data.py \
  --device "${DEVICE}" \
  --tokenizer_model_path "${TOKENIZER_MODEL_PATH}" \
  --input_jsonl "${RAW_JSONL}" \
  --output_jsonl "${TRAIN_JSONL}"

echo "=== [2/2] Fine-tuning ${CHARACTER} ==="
python /workspace/finetuning/sft_12hz.py \
  --init_model_path "${INIT_MODEL_PATH}" \
  --output_model_path "${OUTPUT_DIR}" \
  --train_jsonl "${TRAIN_JSONL}" \
  --batch_size "${BATCH_SIZE}" \
  --lr "${LR}" \
  --num_epochs "${EPOCHS}" \
  --speaker_name "${CHARACTER}"

echo "=== Done! Checkpoints saved to ${OUTPUT_DIR} ==="
