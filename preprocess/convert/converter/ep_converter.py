import json

class EPConverter:
    def __init__(self, NAN="NAN", template_path='preprocess/template/ep_template.json'):
        with open(template_path, 'r') as file:
            template = json.load(file)
        self.NAN = NAN
        self.ep_template = template['template']

        self.entity_pair_int_out_format_en = {
            0: ['[head entity1,tail entity1]\n[head entity2,tail entity2]', self.entity_pair_convert_target0],
            1: ['{head,tail} JSON format', self.entity_pair_convert_target_json]
        }
        self.entity_pair_int_out_format = self.entity_pair_int_out_format_en

    def nan(self, s):
        return s

    def entity_pair_convert_target0(self, rels):
        output_text = []
        for rel in rels:
            head = self.nan(rel['head']).strip()
            tail = self.nan(rel['tail']).strip()
            if head and tail:
                output_text.append(f"[{head},{tail}]")
        output_text = '\n'.join(output_text)
        if len(output_text.replace(self.NAN, '').replace('\n', '').strip()) == 0:
            return self.NAN
        return output_text

    def entity_pair_convert_target_json(self, rels):
        output_json = []
        for rel in rels:
            head = self.nan(rel['head']).strip()
            tail = self.nan(rel['tail']).strip()
            if head and tail:
                output_json.append({"head": head, "tail": tail})
        if len(output_json) == 0:
            return self.NAN
        return json.dumps(output_json, indent=2)

    def convert(self, record, rand1, rand2, s_schema1="", s_schema2=""):
        output_template = self.entity_pair_int_out_format[rand2]
        output_text = output_template[1](record)

        sinstruct = self.ep_template[str(rand1)].format(s_format=output_template[0], s_schema=s_schema2)
        
        return sinstruct, output_text
