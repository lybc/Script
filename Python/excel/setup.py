__author__ = 'lybc'
from distutils.core import setup
import glob
import py2exe,sys,os


options = {"py2exe":
                {"compressed": 1,
                 "optimize": 2,
                 # "bundle_files": 1,
                 "packages": ["xlrd", "xlsxwriter", "tqdm"],
                 #"includes": extra_modules
                }
          }
setup(
    version = "1.0.0",
    description = "cut and merge excel",
    name = "excel",
    options = options,
    zipfile = None,
    console = [{"script": "main.py"}]
)