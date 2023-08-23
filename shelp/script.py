import os
import re
import os.path as op

from .utils import dict_to_command, read_json
from ._constants import CONFIG_JSON


def header(user_config = None):
  config = read_json(CONFIG_JSON)
  if user_config: # if user supplied config
    config = {**config, **user_config}
  contents = "#!/usr/bin/env bash\n\n" # initialize
  for key, value in config.items():
    key = re.sub("_", "-", key) # replace underscores with hyphens
    if value and isinstance(value, bool):
      contents += f"#SBATCH --{key}\n"
    elif value: # if value is not empty
      contents += f"#SBATCH --{key}={value}\n"
  return contents


def modules(modules_list = None):
  if modules_list and isinstance(modules_list, str):
    modules_list = [modules_list]

  contents = "# Load Module(s)\n"
  for module in modules_list: # for each module
    contents += f"module load {module}\n"
  return contents


def apptainer(
  fname = None, 
  sif_fname = None,
  sbatch_options = {}, 
  apptainer_options = {}, 
  command_arguments = [], 
  command_options = {}
):
  
  contents = header(sbatch_options) + "\n"
  contents += modules("apptainer") + "\n"
  
  contents += "# Run Apptainer Command\n"
  contents += "apptainer run\\\n"

  if apptainer_options: # if optional apptainer arguments
    apptainer_options = dict_to_command(apptainer_options)
    for option in apptainer_options:
      contents += f"  {option} \\\n"
  
  contents += f"  {sif_fname} \\\n"
  if command_arguments: # if positional command arguments
    contents += "  " + " ".join(command_arguments) + " \\\n"

  if command_options: # if optional command arguments
    command_options = dict_to_command(command_options)
    for option in command_options:
      contents += f"  {option} \\\n"
  contents = re.sub("\\\s*$", "", contents.strip())
  
  if fname: # write if fname provided
    with open(fname, "w") as f:
      f.writelines(contents)
  
  return contents