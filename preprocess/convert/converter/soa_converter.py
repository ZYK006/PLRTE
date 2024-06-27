import json

class SOAConverter:
    def __init__(self, NAN="NAN", template_path='preprocess/template/soa_template.json'):
        template = json.load(open(template_path, 'r'))
        self.NAN = NAN
        self.relation_template = template['template']
        self.relation_int_out_format_en = {
            0:['(Subject,Relation,Object)', self.relation_convert_target0],
            1:['{head entity is the relation of tail entity}', self.relation_convert_target1],
            2:['{Relation：Subject,Object}', self.relation_convert_target2],
        }
        self.relation_int_out_format = self.relation_int_out_format_en


    def nan(self, s):
        return s


    def relation_convert_target0(self, rels):
        output_text = []
        for rel in rels:
            head = self.nan(rel['head'])
            relation = self.nan(rel['relation'])
            tail = self.nan(rel['tail'])
            if head == "" or relation == "" or tail == "":
                continue
            output_text.append('(' + ','.join([head, relation, tail]) + ')')
        output_text = '\n'.join(output_text)
        if len(output_text.replace(self.NAN, '').replace('\n', '').strip()) == 0:
            return self.NAN
        return output_text 
    

    def relation_convert_target1(self, rels):
        output_text = []
        for rel in rels:
            head = self.nan(rel['head'])
            relation = self.nan(rel['relation'])
            tail = self.nan(rel['tail'])
            if head == "" or relation == "" or tail == "":
                continue
            output_text.append(f"{head} is the {relation} of {tail}")
        output_text = '\n'.join(output_text)
        if len(output_text.replace(self.NAN, '').replace('\n', '').strip()) == 0:
            return self.NAN
        return output_text


    def relation_convert_target2(self, rels):
        output_text = []
        for rel in rels:
            head = self.nan(rel['head'])
            relation = self.nan(rel['relation'])
            tail = self.nan(rel['tail'])
            if head == "" or relation == "" or tail == "":
                continue
            output_text.append(f"{relation}：{head},{tail}")
        output_text = '\n'.join(output_text)
        if len(output_text.replace(self.NAN, '').replace('\n', '').strip()) == 0:
            return  self.NAN
        return output_text 
    

    def convert(self, record, rand1, rand2, s_schema=""):
        output_template = self.relation_int_out_format[rand2]
        output_text = output_template[1](record)
        sinstruct = self.relation_template[str(rand1)].format(s_format=output_template[0], s_schema=s_schema)
        return sinstruct, output_text
