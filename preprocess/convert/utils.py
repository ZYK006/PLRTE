import json
import hashlib

def get_string_list(l):
    return "[" + ', '.join(l) + "]"


def get_string_dict(d):
    s_d = []
    for k, value in d.items():
        s_value =  k + ": " + "[" + ', '.join(value) + "]"
        s_d.append(s_value)
    return '{' + ', '.join(s_d) + '}'


def read_from_json(path):
    datas = []
    with open(path, 'r', encoding='utf-8') as reader:
        for line in reader:
            data = json.loads(line)
            datas.append(data)
    return datas


def write_to_json(path, datas):
    with open(path, 'w', encoding='utf-8') as writer:
        for data in datas:
            writer.write(json.dumps(data, ensure_ascii=False)+"\n")


def stable_hash(input_str):
    sha256 = hashlib.sha256()
    sha256.update(input_str.encode('utf-8'))
    return sha256.hexdigest()

