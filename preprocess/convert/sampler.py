import json
import os
from collections import defaultdict
import random
random.seed(42)

def get_positive_type_role(records, task):
    positive_type = set()
    positive_role = set()
    positive_type_role = defaultdict(set)
    if task == "NER":
        for record in records:
            positive_type.add(record['entity'])
    elif task == "RTE":
        for record in records:
            positive_role.add(record['relation'])
    elif task == "RF":
        for record in records:
            positive_role.add(record['relation'])
    return positive_type, positive_role, positive_type_role



class Sampler:
    def __init__(self, type_list, role_list, type_role_dict, negative=3):
        self.type_list = set(type_list)
        self.role_list = set(role_list)
        self.type_role_dict = defaultdict(set)
        for key, value in type_role_dict.items():
            self.type_role_dict[key] = set(value)
        self.negative = negative

    def set_negative(self, negative):
        self.negative = negative

    def negative_sample(self, record, task):
        positive_type, positive_role, positive_type_role = get_positive_type_role(record, task)
        negative = list()
        if task == "RTE":
            negative = self.role_list - positive_role
            if self.negative > 0:
                negative = random.sample(self.role_list, self.negative)
            for it in negative:
                if it not in positive_role:
                    record.append({"head":"", "relation":it, "tail":""})
        if task == "RF":
            negative = self.role_list - positive_role  
            if self.negative > 0:     # <0, 
                negative = random.sample(self.role_list, self.negative)
            for it in negative:
                if it not in positive_role:
                    record.append({"relation":it})
        elif task == "NER":
            negative = self.type_list - positive_type
            if self.negative > 0:
                negative = random.sample(self.type_list, self.negative)
            for it in negative:
                if it not in positive_type:
                    record.append({"entity":"", "entity_type":it})
        return record


    @staticmethod
    def read_from_file(filename, negative=3):
        if os.path.exists(filename) == False:
            return Sampler(set(), set(), defaultdict(set), negative)
        lines = open(filename).readlines()
        type_list = json.loads(lines[0])
        role_list = json.loads(lines[1])
        type_role_dict = json.loads(lines[2])
        return Sampler(type_list, role_list, type_role_dict, negative)


