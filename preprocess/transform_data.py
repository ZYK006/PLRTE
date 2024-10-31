import sys
sys.path.append("./")
import argparse
import json
import os
import hashlib
from collections import defaultdict
import random, copy
from typing import Dict
random.seed(42)

from convert.sampler import Sampler, get_positive_type_role
from convert.random_sort import rel_sort, ent_sort, rf_sort
from convert.converter.ner_converter import NERConverter
from convert.converter.rte_converter import RTEConverter
from convert.converter.rf_converter import RFConverter
from convert.converter.soa_converter import SOAConverter
from convert.converter.ep_converter import EPConverter


def stable_hash(input_str):
    sha256 = hashlib.sha256()
    sha256.update(input_str.encode('utf-8'))
    return sha256.hexdigest()


def process_ft_file(input_file_path, output_file_path):
    processed_data = []
    with open(input_file_path, 'r') as file:
        for line in file:
            try:
                obj = json.loads(line.strip())
                processed_obj = {
                    "instruction": obj.get("instruction", ""),
                    "input": obj.get("input", ""),
                    "output": obj.get("output", ""),
                    "history": []
                }
                processed_data.append(processed_obj)
            except json.JSONDecodeError as e:
                print(f"Error decoding JSON object: {e}, Content: {line}")

    with open(output_file_path, 'w', encoding='utf-8') as file:
        json.dump(processed_data, file, indent=4, ensure_ascii=False)


def convert_ie(
        record:Dict, 
        sample:int, 
        task:str, 
        neg_sampler1,
        neg_sampler2,
        converter,
        neg_ratio:0.1,
        input_text='input',
        random_sort=True,
    ):
    if sample == -1:
        if task == "EP":
            rand1 = random.randint(0,9)
        else:
            rand1 = random.randint(0,19)

        if task == "RTE" or task == "SOA":
            rand2 = random.randint(0,1)
        else:
            rand2 = 0
    else:
        rand1 = sample
        rand2 = sample

    neg = False
    if neg_ratio > 0:
        rand3 = random.random() 
        if rand3 < neg_ratio:
            neg = True

    if task == 'EP':
        rels_type = neg_sampler2.role_list
        sinstruct, output_text = converter.convert(record['relation'], rand1, rand2, s_schema2=rels_type)
    elif task == 'RTE':
        if neg:
            record['relation'] = neg_sampler2.negative_sample(record['relation'], 'RTE')
        if random_sort:
            record['relation'], rels_type = rel_sort(record[input_text], record['relation']) 
        else:
            rels_type = list(get_positive_type_role(record['relation'], 'RTE')[1])
            rels_type = sorted(rels_type)
        sinstruct, output_text = converter.convert(record['relation'], rand1, rand2, s_schema1=list(neg_sampler1.type_list), s_schema2=rels_type)
    elif task == 'SOA':
        if neg:
            record['relation'] = neg_sampler2.negative_sample(record['relation'], 'RTE')
        if random_sort:
            record['relation'], rels_type = rel_sort(record[input_text], record['relation']) 
        else:
            rels_type = list(get_positive_type_role(record['relation'], 'RTE')[1])
            rels_type = sorted(rels_type)
        sinstruct, output_text = converter.convert(record['relation'], rand1, rand2, s_schema2=rels_type)
    elif task == 'NER':
        if neg:
            record['entity'] = neg_sampler1.negative_sample(record['entity'], 'NER')
        if random_sort:
            record['entity'] = ent_sort(record[input_text], record['entity']) 
        else:
            ents_type = list(get_positive_type_role(record['entity'], 'NER')[0])
            ents_type = sorted(ents_type)
        sinstruct, output_text = converter.convert(record['entity'], rand1, rand2, s_schema1=neg_sampler1.type_list)
    elif task == 'RF':
        negative_relations = []
        if neg:
            negative_relations = copy.deepcopy(record['relation'])
            record['relation'] = neg_sampler2.negative_sample(record['relation'], 'RF')
        if random_sort:
            rels_type = rf_sort(record['relation'])  
        else:
            rels_type = list(get_positive_type_role(record['relation'], 'RF')[1])
            rels_type = sorted(rels_type)
        sinstruct, output_text = converter.convert(negative_relations, rand1, rand2, s_schema2=rels_type)
    else:
        raise KeyError
    return sinstruct, output_text


def process(
        src_path, 
        tgt_path, 
        schema_path1,
        schema_path2,
        task='RTE', 
        sample=-1,
        neg_ratio=0.1,
        neg_schema=0.8,
        random_sort=True,
    ):
    # 加载第一个 schema 文件
    if os.path.exists(schema_path1):
        neg_sampler1 = Sampler.read_from_file(schema_path1, negative=-1)
    else:
        raise FileNotFoundError(f"The schema file '{schema_path1}' does not exist. Unable to proceed.")
    
    # 加载第二个 schema 文件
    if os.path.exists(schema_path2):
        neg_sampler2 = Sampler.read_from_file(schema_path2, negative=-1)
    else:
        raise FileNotFoundError(f"The schema file '{schema_path2}' does not exist. Unable to proceed.")


    if task == 'RTE':
        converter = RTEConverter(NAN='NAN')
        neg_sampler1.set_negative(max(1, round(neg_schema*len(neg_sampler1.type_list))))
        neg_sampler2.set_negative(max(1, round(neg_schema*len(neg_sampler2.role_list))))
    elif task == 'SOA':
        converter = SOAConverter(NAN='NAN')
        neg_sampler2.set_negative(max(1, round(neg_schema*len(neg_sampler2.role_list))))
    elif task == 'NER':
        converter = NERConverter()
        neg_sampler1.set_negative(max(1, round(neg_schema*len(neg_sampler1.type_list))))
    elif task == 'RF':
        converter = RFConverter()
        neg_sampler2.set_negative(max(1, round(neg_schema*len(neg_sampler2.role_list))))
    elif task == 'EP':
        converter = EPConverter()
        neg_sampler2.set_negative(max(1, round(neg_schema*len(neg_sampler2.role_list))))
    else:
        raise KeyError
    
    writer = open(tgt_path, "w", encoding="utf-8")
    with open(src_path, "r", encoding="utf-8") as reader:
        for line in reader:
            record = json.loads(line)
            sinstruct, output_text = convert_ie(
                record, 
                sample, 
                task, 
                neg_sampler1,
                neg_sampler2,
                converter,
                neg_ratio=neg_ratio,
                input_text='input',
                random_sort=random_sort,
            )
            new_record = {'id': stable_hash(record['input']),'instruction': sinstruct, 'input': record['input'], 'output': output_text}
            writer.write(json.dumps(new_record, ensure_ascii=False)+"\n")
    


if __name__ == "__main__":

    parse = argparse.ArgumentParser()
    parse.add_argument("--src_path", type=str, default="../sample/DDI/process_abstract_train_sample100.json")
    parse.add_argument("--tgt_path", type=str, default="../sample/DDI/subtask/train_sample100_re.json")
    parse.add_argument("--schema_path1", type=str, default='../sample/DDI/schema.json')
    parse.add_argument("--schema_path2", type=str, default='../sample/DDI/schema.json')
    parse.add_argument("--task", type=str, default="RTE", choices=['RTE', 'NER', 'RF', 'SOA', 'EP'])
    parse.add_argument("--sample", type=int, default=-1, help="If -1, randomly samples one of the multiple instructions and multiple output formats, otherwise it is the specified instruction format.")
    parse.add_argument("--neg_ratio", type=float, default=1, help="Fractions between 0 and 1, indicate the proportion of all samples sampled negatively, <=0 indicates no negative sampling.")
    parse.add_argument("--neg_schema", type=float, default=1, help="Decimal number between 0 and 1, indicates the percentage of negative samples from schema, <=0 means no negative samples.")
    parse.add_argument("--random_sort", action="store_true", default=True, help="whether to randomly sort the schema list in the command")    
    options = parse.parse_args()

    process(
        src_path=options.src_path,
        tgt_path=options.tgt_path,
        schema_path1=options.schema_path1,
        schema_path2=options.schema_path2,
        task=options.task,
        sample=options.sample,
        neg_ratio=options.neg_ratio,
        neg_schema=options.neg_schema,
        random_sort=options.random_sort
    )
    
    process_ft_file(
        input_file_path=options.tgt_path,
        output_file_path=options.tgt_path
    )
    
