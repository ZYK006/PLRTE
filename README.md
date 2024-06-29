# PLRTE: Progressive Learning for Biomedical Relation Triplet Extraction Using Large Language Models

## Data Augmentation

### Compositional Instruction Construct and Semantic Relation Augmentation

This repository is structured to facilitate the transformation and integration of raw data into structured formats specifically designed for Entity Pair Extraction (EP) and Relation Triple Extraction (RTE) tasks. Below is an overview of the main components:

- `preprocess/`: Contains all preprocessing scripts that convert raw data into structured formats for various NLP tasks.
  - `rte_to_ner_and_rf.py`: Converts relation triplet extraction data into NER and RF tasks.
  - `transform_data.py`: Handles transformation for NER, RF, SOA, RTE, and EP tasks.
  -  `mti_instruct.py`: Merges outputs from individual tasks into compositional instructions.
- `sample_data/`: Sample data and schema files used for processing.

#### Running the `transform_data.sh` Script

The `transform_data.sh` script is responsible for transforming data for specific NLP tasks such as NER, RF, SOA, RTE, and EP.  This script should be run with the following parameters:

```bash
bash ./transform_data.sh <input_base_path> <output_base_path> <schema_ep_path> <schema_ner_path> <schema_rte_path> <neg_schema>
```

##### Parameters

- **`<input_base_path>`**: The path to the input JSON file containing the data to be processed.

- **`<output_base_path>`**: The path where the transformed data should be saved.

- **`<schema_ep_path>`**: Path to the schema JSON file for the Entity Pair (EP) extraction task.  This schema defines the coarse-grained types within the dataset

- **`<schema_ner_path>`**: Path to the schema JSON file for the Named Entity Recognition (NER) task.  This schema outlines the entity types present in the dataset

- **`<schema_rte_path>`**: Path to the schema JSON file for the Relation Triplet Extraction (RTE) task.  This schema contains definitions for fine-grained relation types between entities in the dataset

- **`<neg_schema>`**: A floating-point value between 0 and 1 indicating the proportion of the schema to be considered for negative sampling. <=0 means no negative samples.


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
