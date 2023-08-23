import json
import os.path as op

from ._constants import CONFIG_JSON, DEFAULT_CONFIG
from .utils      import read_json, write_json


def init(force = False):
  print("Initializing configuration file...")
  if not force and op.isfile(CONFIG_JSON): # if configuration file exists
    print("WARNING: configuration file already exists.")

    response = input("Overwrite configuration file? [y/n] ")
    while response.lower() not in ("y", "n"):
      print("Please enter a valid response.\n")
      response = input("Overwrite configuration file? [y/n] ")
  
  if force or not op.isfile(CONFIG_JSON) or response == "y":
    write_json(CONFIG_JSON, DEFAULT_CONFIG) # write default config
    print("Created default configuration file.")


def edit(**kwargs):
  if not op.isfile(CONFIG_JSON): # if configuration file does not exist
    print("Configuration file does not exist, creating default configuration...")
    init(force = True) # force initialize

  config = read_json(CONFIG_JSON) # read configuration file
  for key, value in kwargs.items(): # for each argument
    config[key] = value # assign value to configuration
  write_json(CONFIG_JSON, config) # write edited configuration file


def view():
  print(json.dumps(read_json(CONFIG_JSON), indent = 2))
