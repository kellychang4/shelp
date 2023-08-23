import json

from ._constants import CONFIG_JSON


def read_json(fname):
  with open(fname, "r") as f:
    contents = json.load(f)
  return contents


def write_json(fname, json_dict, indent = 2):
  contents = json.dumps(json_dict, indent = indent)
  with open(fname, "w") as f:
    f.write(contents)  


def get_config(key = None):
  if key: # if key specified
    return read_json(CONFIG_JSON)[key]
  return read_json(CONFIG_JSON)