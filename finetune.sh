output_dir='lora/Mistral'
mkdir -p ${output_dir}
CUDA_VISIBLE_DEVICES="0" python finetune/finetune.py \
    --do_train --do_eval \
    --overwrite_output_dir \
    --stage 'sft' \
    --model_name_or_path 'mistralai/Mistral-7B-v0.1' \
    --model_name 'mistral' \
    --template 'default' \
    --train_file 'sample_data/DDI/composite_data/all_data.json' \
    --val_set_size 1 \
    --output_dir=${output_dir} \
    --per_device_train_batch_size 2 \
    --per_device_eval_batch_size 2 \
    --gradient_accumulation_steps 8 \
    --preprocessing_num_workers 16 \
    --num_train_epochs 3 \
    --learning_rate 1e-4 \
    --max_grad_norm 0.5 \
    --optim "adamw_torch" \
    --max_source_length 400 \
    --cutoff_len 1024 \
    --max_target_length 500 \
    --evaluation_strategy "epoch" \
    --save_strategy "epoch" \
    --save_total_limit 10 \
    --lora_r 64 \
    --lora_alpha 128 \
    --lora_dropout 0.1

