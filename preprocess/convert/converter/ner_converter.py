import json

class NERConverter:
    def __init__(self, template_path="preprocess/template/ner_template.json"):
        template = json.load(open(template_path, 'r'))
        self.entity_template = template['template']
        self.entity_int_out_format_en = {
            0: ["{[entity1], [entity2]}", self.entity_convert_target0]
        }
        self.entity_int_out_format = self.entity_int_out_format_en
    

    def extract_entities(self, entities):
        return [entity["entity"] for entity in entities if entity["entity"].strip()]

    def entity_convert_target0(self, entities):
        extracted_entities = self.extract_entities(entities)
        return ','.join([f'[{entity}]' for entity in extracted_entities])


    def convert(self, record, rand1, rand2, s_schema1="", s_schema2=""):
        output_template = self.entity_int_out_format[rand2]
        output_text = output_template[1](record)
        sinstruct = self.entity_template[str(rand1)].format(s_format=output_template[0], s_schema=s_schema1)
        return sinstruct, output_text
