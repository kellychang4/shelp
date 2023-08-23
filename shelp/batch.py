import glob
import subprocess
import os.path as op


def batch(slurm_dir):
  slurm_list = glob.glob(op.join(slurm_dir, "*.slurm"))
  for slurm_script in slurm_list: # for each slurm script
    subprocess.run(["sbatch", slurm_script])