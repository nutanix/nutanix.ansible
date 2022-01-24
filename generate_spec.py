import json


def generate_spec(data, variable_name="", default={}):
    is_list = False
    if "additionalProperties" in data.keys():
        data = data["additionalProperties"]
    if "items" in data.keys():
        data = data["items"]
        is_list = True
    if "properties" in data.keys():
        data = data["properties"]
    elif "type" in data.keys() and data["type"] in ["string", "integer", "boolean"]:
        return "{{" + variable_name + "}}"
    for k, v in data.items():
        data[k] = generate_spec(
            v, variable_name + "__" + str(k) if variable_name else str(k)
        )
    if is_list:
        data.update({"list_key": variable_name})
        return [data]
    return data


def parse_json_to_spec(json_files_dir="", spec_files_dir=""):
    import glob
    import os

    print(glob.glob(json_files_dir + "*json.json"))
    files = glob.glob(json_files_dir + "*json.json")
    for file in files:
        file_name = spec_files_dir + os.path.splitext(file)[0]

        with open(file) as f:
            data = json.loads(f.read())
        print("--------------------------------")
        spec = generate_spec(data)
        with open(file_name + "_spec.json", "w") as spec_file:
            spec_file.write(json.dumps(spec))
        print(json.dumps(spec, indent=4))
        return spec
