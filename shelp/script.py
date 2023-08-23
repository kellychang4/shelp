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
    print(command_options)
    for option in command_options:
      contents += f"  {option} \\\n"
  contents = re.sub("\\\s*$", "", contents.strip())
  
  if fname: # write if fname provided
    with open(fname, "w") as f:
      f.writelines(contents)
  
  return contents


def qsiprep(
  fname, 
  data_dir, 
  out_dir,  
  participant_label,
  output_resolution, 
  work_dir = None,
  unringing_method = None, 
  fs_license = None,
  eddy_config = None,
  use_nvidia = False
):
  
  os.makedirs(op.dirname(fname), exist_ok = True)
  
  sbatch_options = {
    "job_name": participant_label,
    "output": f"{participant_label}_output.log", 
    "error": f"{participant_label}_error.log", 
  }

  apptainer_options = {} # initialize
  apptainer_options["cleanenv"] = True
  
  mount_dirs = [f"{data_dir}:/data", f"{out_dir}:/out"]
  if work_dir: # if using a working directory
    mount_dirs.append(f"{work_dir}:/work")
  apptainer_options["bind"] = mount_dirs
  apptainer_options["nv"] = use_nvidia 

  command_options = {} # initialize
  command_options["participant-label"] = participant_label
  command_options["output-resolution"] = output_resolution
  if unringing_method: # if using unringing method
    command_options["unringing-method"] = unringing_method
  if fs_license: # if fs license provided
    command_options["fs-license-file"] = "/license.txt"
  if eddy_config: # if eddy configuration provided
    command_options["eddy-config"] = "/eddy_config.json"
  if work_dir: # if using a working directory
    command_options["work"] = "/work"

  apptainer(
    fname = fname, 
    sif_fname = "qsiprep.sif", 
    sbatch_options = sbatch_options,
    apptainer_options = apptainer_options,
    command_arguments = [ "/data", "/out", "participant" ], 
    command_options = command_options
  )