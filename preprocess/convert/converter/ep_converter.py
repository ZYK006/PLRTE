import json

class EPConverter:
    def __init__(self, template_path='preprocess/template/ep_template.json'):
        with open(template_path, 'r') as file:
            template = json.load(file)
        self.ep_template = template['template']


    def entity_pair_convert(self, rels):
        output_text = []
        for rel in rels:
            head = rel['head'].strip()
            tail = rel['tail'].strip()
            if head and tail:
                output_text.append(f"[{head}, {tail}]")
        return '; '.join(output_text)


    def convert(self, record, rand1, s_schema=""):
        sinstruct = self.ep_template[str(rand1)].format(s_schema=s_schema, s_format="[subject1, object1]; [subject2, object2]")
        output_text = self.entity_pair_convert(record)
        return sinstruct, output_text
