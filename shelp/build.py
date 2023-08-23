import sys
import tempfile
import subprocess
import os.path as op

from .utils import get_config


def build(
  image_path, 
  sif_output, 
  account = None, 
  partition = None, 
  stream = False
):
  account   = account if account else get_config("account")
  partition = partition if partition else get_config("partition")
  
  temp_sbatch = op.join(tempfile.gettempdir(), "build.slurm")
  with open(temp_sbatch, "w") as f:
    f.write("#!/usr/bin/env bash\n")
    f.write(f"#SBATCH --account={account}\n")
    f.write(f"#SBATCH --partition={partition}\n")
    f.write("\nmodule load apptainer\n")
    f.write(f"apptainer build {sif_output} {image_path}\n")
  sbatch_cmd = ["sbatch", temp_sbatch]

  if stream: # if streaming subprocess output
    with subprocess.Popen(sbatch_cmd, stdout = subprocess.PIPE) as process:
      for line in process.stdout: # for each line of stdout
        print(line.decode("utf8").strip("\n"))
  else: # else run subprocess with suppressed output
    subprocess.run(sbatch_cmd, stdout = subprocess.DEVNULL)