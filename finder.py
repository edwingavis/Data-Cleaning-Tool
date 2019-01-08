# -*- coding: utf-8 -*-
"""
Created on Tue Aug  7 10:07:05 2018

@author: egavis
"""

import os
import sys

if getattr(sys, 'frozen', False):
    CurrentPath = sys._MEIPASS
else:
    CurrentPath = os.path.dirname(__file__)

def get_dir_path(dir_name):
       return os.path.join(CurrentPath, dir_name)

def get_file_path(dir_name, file_name):
    dir_path = get_dir_path(dir_name)
    return os.path.join(dir_path, file_name)
