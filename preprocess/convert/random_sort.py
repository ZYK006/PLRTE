import sys
sys.path.append('./')
import random
random.seed(42)


def match_sublist(the_list, to_match):
    len_to_match = len(to_match)
    matched_list = list()
    for index in range(len(the_list) - len_to_match + 1):
        if to_match == the_list[index:index + len_to_match]:
            matched_list += [(index, index + len_to_match)]
    return matched_list


# Consider the head and tail entity positions first, then the relationship type
def rel_sort(text, rels):
    new_rels = []
    rels_mapper = {}
    for rel in rels:
        if rel['relation'] not in rels_mapper:
            type_id = random.randint(0, 1000)
            rels_mapper[rel['relation']] = type_id
        else:
            type_id = rels_mapper[rel['relation']] 
        head_offset = match_sublist(list(text), list(rel['head']))
        tail_offset = match_sublist(list(text), list(rel['tail']))
        if len(head_offset) == 0:
            head_offset = [[-100,-100],]
        if len(tail_offset) == 0:
            tail_offset = [[-100,-100],]
        head_offset = head_offset[0]
        tail_offset = tail_offset[0]
        new_rels.append([rel, [head_offset[0], tail_offset[0], type_id]])
    new_rels = sorted(new_rels, key=lambda x: (x[1][0], x[1][1], x[1][2]))
    new_rels = [it[0] for it in new_rels]
    rels_list = sorted(rels_mapper.items(), key=lambda x: x[1])
    rels_list = [it[0] for it in rels_list]
    return new_rels, rels_list

def rf_sort(rels):
    rels_mapper = {}
    for rel in rels:
        if rel['relation'] not in rels_mapper:
            type_id = random.randint(0, 1000)
            rels_mapper[rel['relation']] = type_id
        else:
            type_id = rels_mapper[rel['relation']] 
    rels_list = sorted(rels_mapper.items(), key=lambda x: x[1])
    rels_list = [it[0] for it in rels_list]
    return rels_list


def ent_sort(text, ents):
    new_ents = []
    for ent in ents:
        ent_offset = match_sublist(list(text), list(ent['entity']))
        if len(ent_offset) == 0:
            ent_offset = [[-100, -100],]
        ent_offset = ent_offset[0]
        new_ents.append([ent, ent_offset[0]])
    new_ents = sorted(new_ents, key=lambda x: x[1])
    new_ents = [it[0] for it in new_ents]
    return new_ents
