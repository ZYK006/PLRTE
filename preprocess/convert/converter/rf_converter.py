import json

class RFConverter:
    def __init__(self, template_path="preprocess/template/rf_template.json"):
        template = json.load(open(template_path, 'r'))
        self.relation_template = template['template']
        self.relation_int_out_format_en = {
            0: ["{relation1,relation2}", self.relation_convert_target0]
        }
        self.relation_int_out_format = self.relation_int_out_format_en


    def extract_relations(self, relations):
        return [relation["relation"] for relation in relations]


    def relation_convert_target0(self, relations):
        extracted_relations = self.extract_relations(relations)
        return ','.join(extracted_relations)


    def convert(self, record, rand1, rand2, s_schema1="", s_schema2=""):
        output_template = self.relation_int_out_format[rand2]
        output_text = output_template[1](record)
        sinstruct = self.relation_template[str(rand1)].format(s_format=output_template[0], s_schema=s_schema2)
        return sinstruct, output_text
    



