# PLRTE: Progressive Learning for Biomedical Relation Triplet Extraction Using Large Language Models

## Data Augmentation

### Compositional Instruction Construct and Semantic Relation Augmentation

This repository is structured to facilitate the transformation and integration of raw data into structured formats specifically designed for Entity Pair Extraction (EP) and Relation Triple Extraction (RTE) tasks. Below is an overview of the main components:

- `preprocess/`: Contains all preprocessing scripts that convert raw data into structured formats for various NLP tasks.
  - `rte_to_ner_and_rf.py`: Converts relation triplet extraction data into NER and RF tasks.
  - `transform_data.py`: Handles transformation for NER, RF, SOA, RTE, and EP tasks.
  -  `mti_instruct.py`: Merges outputs from individual tasks into compositional instructions.
- `sample_data/`: Sample data and schema files used for processing.


### Combine Data
```bash
python preprocess/combine_data.py
```
#### Parameters:
- `input_file_paths` (list): A list containing paths to JSON files. These files may include both compositional and single instructions for relation triplet tasks, as well as compositional and single instructions for entity-pair extraction.
- `output_file` (str): The path to the output file.

## Training
### Environments Install
```bash
conda create -n PLRTE python=3.10
conda activate PLRTE
pip install -r requirements.txt
```

### Finetuning with data
```bash
bash finetune.sh
```
