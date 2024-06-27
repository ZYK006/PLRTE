import json
import random

def load_json_data(file_paths, output_file):
    combined_data = []
    for file_path in file_paths:
        with open(file_path, 'r') as file:
            data = json.load(file)
            combined_data.extend(data)
    random.seed(42)
    random.shuffle(combined_data)

    with open(output_file, 'w') as file:
        json.dump(combined_data, file, indent=4, ensure_ascii=False)  # Save the combined list of JSON objects


if __name__ == '__main__':

    input_file_paths = [
        'sample_data/DDI/composite_data/train_abstract_composite_ep.json', 
        'sample_data/DDI/composite_data/train_abstract_ep.json', 
        'sample_data/DDI/composite_data/train_abstract_composite_rte.json',
        'sample_data/DDI/composite_data/train_abstract_rte.json'
    ]

    output_file_path = 'sample_data/DDI/composite_data/all_data.json'

    load_json_data(input_file_paths, output_file_path)
