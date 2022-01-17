import json


def generate_spec(data, variable_name='', default={}):
    is_list = False
    required = []
    if data.get('required'):
        required = data['required']
    if 'additionalProperties' in data.keys():
        data = data['additionalProperties']
    if 'items' in data.keys():
        data = data['items']
        is_list = True
    if 'properties' in data.keys():
        data = data['properties']
    # if 'default' in data.keys():
        # data = data['default']
        # return {'default':data['default']}
    elif 'type' in data.keys() and data['type'] in ['string', 'integer', 'boolean']:
        return '{{' + variable_name + '}}'
    for k, v in data.items():
        data[k] = generate_spec(v, variable_name + '__' + str(k) if variable_name else str(k))
    data['required'] = required
    if is_list:
        data.update({'list_key': variable_name})
        return [data]
    return data


def parse_json_to_spec(json_files_dir='', spec_files_dir=''):
    import glob
    import os
    print(glob.glob(json_files_dir + '*json.json'))
    files = glob.glob(json_files_dir + '*json.json')
    for file in files:
        file_name = spec_files_dir + os.path.splitext(file)[0]

        with open(file) as f:
            data = json.loads(f.read())
        print('--------------------------------')
        spec = generate_spec(data)
        with open(file_name + "_spec.json", 'w') as spec_file:
            spec_file.write(json.dumps(spec))
        print(json.dumps(spec, indent=4))
        return spec


spec = parse_json_to_spec()
print(spec)

def clean_spec(self, spec):
    if not isinstance(spec, dict):
        raise ValueError(spec)
    for k, v in spec.copy().items():
        if isinstance(v, str):
            if v.startswith('{{') and v.endswith('}}'):
                if self.get(v[2:-2]):
                    spec[k] = self.get(v[2:-2])
                else:
                    spec.pop(k)
        elif isinstance(v, dict):
            v = clean_spec(self,v)
            if v:
                spec[k] = v
            else:
                spec.pop(k)
        elif isinstance(v,list) and k != 'required':
            v = [clean_spec(self,i) for i in v]
            if tuple(i for i in v if i):
                spec[k] = v
            else:
                spec.pop(k)
    print('-----------------------------------')

    requirements = spec.get('required',())
    # print(requirements)
    # if not requirements:
    #     for k, v in spec.items():
    #         print(k,v,'////////////')
    #         if isinstance(v, dict) and v.get('required'):
    #             requirements.append(k)
    # print(requirements)
    # print(spec)
    # print('++++++++++++++++++++++++++++++')
    # print()
    # print()
    if not set(requirements) <= spec.keys() or not spec:
        return {'required': requirements}
    return spec


self = {'action': 'create', 'credentials': {'username': 'admin', 'password': 'Nutanix.123'},
        'ip_address': '10.44.77.6', 'port': '9440', 'cluster_uuid': '0005d2b3-16d0-829d-4591-ac1f6b6f97e7',
        'name': 'test', 'spec__name': 'test',
        # 'spec__cluster_reference__uuid': '0005d2b3-16d0-829d-4591-ac1f6b6f97e7',
        'wait': True, 'wait_timeout': 300, 'validate_certs': False,
        'spec__resources__nic_list__is_connected': False,
        'spec__cluster_reference__kind': 'cluster',
        'spec__resources__nic_list__subnet_reference__kind': 'subnet',
        'data': None, 'operations': None, 'uuid': None,
        'cpu_properties': None,
        'spec__cluster_reference__name': None,
        'spec__resources__nic_list__subnet_reference__uuid': None,
        'spec__resources__nic_list__subnet_reference__name': None, 'nic_list': None}

print(json.dumps(clean_spec(self,spec), indent=4))