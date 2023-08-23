from setuptools import setup, find_packages

from shelp import __version__

setup(
  name = "shelp",
  version = __version__,
  description = "Helpful SLURM CLI",
  author = [ "Kelly Chang" ], 
  author_email = "kchang4@uw.edu", 
  packages = find_packages(include = "shelp"), 
  required_installs = [
      "cloudpathlib[aws,azure,gs]>=0.15.1"
  ], 
  python_requires = ">=3.10.12"
)