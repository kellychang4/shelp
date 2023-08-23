import os
import os.path as op


CONFIG_JSON = op.join(os.environ["HOME"], ".config", "shelp", "config.json")

DEFAULT_CONFIG = {
  "account": os.environ["USER"],
  "cpus_per_task": 1, 
  "chdir": os.environ["HOME"],
  "error": "error.log", 
  "export": "", 
  "export_file": "", 
  "job_name": "job_name", 
  "mail_type": "all", 
  "mail_user": "", 
  "no_requeue": False, 
  "nodes": 1, 
  "output": "output.log", 
  "partition": "ckpt", 
  "quiet": False, 
  "time": "00-00:15:00",
  "mem": "8G", 
  "gpus": 0
}