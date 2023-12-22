import subprocess
import os
import traceback


def create_dir_if_not_exist(path: str):
    if not os.path.isdir(path):
        os.mkdir(path)


MODEL_NAME="dreamlike-art/dreamlike-photoreal-2.0"
INSTANCE_DIR="./images"
OUTPUT_DIR="./photo_realism/"
CLASS_DIR="Stable-Diffusion-Regularization-Images-person_ddim/person_ddim/"

try:
    create_dir_if_not_exist(OUTPUT_DIR)
except Exception as e:
    print(f"Failed to create {OUTPUT_DIR} :- \n\n\n\nException:{traceback.format_exc()}")

command = f"""
accelerate launch diffusers/examples/dreambooth/train_dreambooth.py \
    --read_prompts_from_txts \
    --train_text_encoder \
    --pretrained_model_name_or_path={MODEL_NAME} \
    --instance_data_dir={INSTANCE_DIR} \
    --output_dir={OUTPUT_DIR} \
    --class_data_dir={CLASS_DIR} \
    --with_prior_preservation --prior_loss_weight=1.0 \
    --instance_prompt="photo of [v] person" \
    --class_prompt="photo of person" \
    --resolution=768 \
    --train_batch_size=1 \
    --gradient_accumulation_steps=1 --gradient_checkpointing \
    --use_8bit_adam \
    --mixed_precision="fp16" \
    --learning_rate=1e-6 \
    --lr_scheduler="constant" \
    --lr_warmup_steps=0 \
    --num_class_images=50 \
    --max_train_steps=1200 \
    --pretrained_vae_name_or_path="stabilityai/sd-vae-ft-mse"
"""

# Run the command using subprocess
ret = subprocess.run(command, shell=True, check=True,stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
if ret.returncode == 0:
    print(f"Training completed successfully")
else:
    print(f"Trained model saved at :- {OUTPUT_DIR}")
