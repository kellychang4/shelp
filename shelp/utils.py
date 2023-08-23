import json

from ._constants import CONFIG_JSON


def command_option(key, value):
  return f"--{key} {value}"


def dict_to_command(options):
  cmd = [] # initialize
  for key, value in options.items():
    if value and isinstance(value, bool):
      cmd.append(f"--{key}") # add boolean flag option
    elif value and (isinstance(value, list) or isinstance(value, tuple)):
      cmd.extend([command_option(key, x) for x in value])
    elif value and (isinstance(value, int) or isinstance(value, str)): 
      cmd.append(command_option(key, value))
  return cmd


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