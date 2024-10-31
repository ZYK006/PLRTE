#!/bin/bash


# Set default paths
default_schema_path_ep="/workspace/dataset/en_dataset/DDI/schema/schema_ep.json"
default_schema_path_ner="/workspace/dataset/en_dataset/DDI/schema/schema_ner.json"
default_schema_path_rte="/workspace/dataset/en_dataset/util/data_format/RE/schema.json"
input_base_path="/workspace/dataset/en_dataset/DDI/format/filtered_train_abstract"
output_base_path="/workspace/dataset/en_dataset/new_re2/ddi/train"

# Accept parameters
input_base_path=${1:-$input_base_path}
output_base_path=${2:-$output_base_path}
schema_path_ep=${3:-$default_schema_path_ep}
schema_path_ner=${4:-$default_schema_path_ner}
schema_path_rte=${5:-$default_schema_path_rte}
neg_schema=${6:-1}

# First, convert relation triple extraction tasks to entity extraction and relationship filtering tasks.
python preprocess/rte_to_ner_and_rf.py --input_json_file_path "${input_base_path}.json"


#Execute NER data conversion command
python preprocess/transform_data.py \
  --src_path "${input_base_path}_ner.json" \
  --tgt_path "${output_base_path}_ner.json" \
  --schema_path1 "$schema_path_ner" \
  --schema_path2 $schema_path_rte \
  --task NER \
  --neg_schema 1

# # Execute RF data conversion command
python preprocess/transform_data.py \
  --src_path ${input_base_path}_rf.json \
  --tgt_path ${output_base_path}_rf.json \
  --schema_path1 "$schema_path_ner" \
  --schema_path2 $schema_path_rte \
  --task RF \
  --neg_schema $neg_schema

# Execute SOA data conversion command
python preprocess/transform_data.py \
  --src_path ${input_base_path}.json \
  --tgt_path ${output_base_path}_soa.json \
  --schema_path1 "$schema_path_ner" \
  --schema_path2 $schema_path_rte \
  --task SOA \
  --neg_schema $neg_schema

# Execute RTE data conversion command
python preprocess/transform_data.py \
  --src_path ${input_base_path}.json \
  --tgt_path ${output_base_path}_rte.json \
  --schema_path1 "$schema_path_ner" \
  --schema_path2 $schema_path_rte \
  --task RTE \
  --neg_schema $neg_schema

# Execute EP data conversion command
python preprocess/transform_data.py \
  --src_path ${input_base_path}.json \
  --tgt_path ${output_base_path}_ep.json \
  --schema_path1 "$schema_path_ner" \
  --schema_path2 $schema_path_ep \
  --task EP \
  --neg_schema $neg_schema


# # Merge into relation triple extraction compositional instructions
python preprocess/mti_instruct.py --json_files ${output_base_path}_ner.json ${output_base_path}_rf.json ${output_base_path}_soa.json --output ${output_base_path}_composite_rte.json

# # Merge into entity-pair extraction compositional instructions
python preprocess/mti_instruct.py --json_files ${output_base_path}_ner.json ${output_base_path}_ep.json --output ${output_base_path}_composite_ep.json

