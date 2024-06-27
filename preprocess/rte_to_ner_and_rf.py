import json,os
import argparse

parser = argparse.ArgumentParser(description='Transform JSON data.')
parser.add_argument('--input_json_file_path', type=str, help='Path to the input JSON file')
args = parser.parse_args()
input_json_file_path = args.input_json_file_path


def transform_json_entities(json_file_path):
    transformed_entities = []

    with open(json_file_path, 'r', encoding='utf-8') as file:
        for line in file:
            obj = json.loads(line)
            new_obj = {"input": obj["input"], "entity": []}
            entities = []

            for relation in obj.get("relation", []):
                if relation["head"] not in [e["entity"] for e in entities]:
                    entities.append({"entity": relation["head"]})
                if relation["tail"] not in [e["entity"] for e in entities]:
                    entities.append({"entity": relation["tail"]})

            new_obj["entity"] = entities
            transformed_entities.append(new_obj)

    return transformed_entities


def transform_json_relations(json_file_path):
    transformed_relations = []

    with open(json_file_path, 'r', encoding='utf-8') as file:
        for line in file:
            obj = json.loads(line)
            new_obj = {"input": obj["input"], "relation": []}
            seen_relations = set()
            ordered_relations = []

            for relation in obj.get("relation", []):
                if relation["relation"] not in seen_relations:
                    seen_relations.add(relation["relation"])
                    ordered_relations.append({"relation": relation["relation"]})

            new_obj["relation"] = ordered_relations
            transformed_relations.append(new_obj)

    return transformed_relations


def save_transformed_objects(transformed_objects, output_file_path):
    with open(output_file_path, 'w', encoding='utf-8') as file:
        for obj in transformed_objects:
            file.write(json.dumps(obj) + '\n')


def main():
    base_file_path = os.path.splitext(input_json_file_path)[0]
    
    output_json_file_path_entities = f"{base_file_path}_ner.json"
    output_json_file_path_relations = f"{base_file_path}_rf.json"
    
    transformed_json_entities = transform_json_entities(input_json_file_path)
    save_transformed_objects(transformed_json_entities, output_json_file_path_entities)
    
    transformed_json_relations = transform_json_relations(input_json_file_path)
    save_transformed_objects(transformed_json_relations, output_json_file_path_relations)
    
    print(f"Transformed JSON objects with entities have been saved to {output_json_file_path_entities}")
    print(f"Transformed JSON objects with relations have been saved to {output_json_file_path_relations}")

if __name__ == '__main__':
    main()
