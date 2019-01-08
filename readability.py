# -*- coding: utf-8 -*-
"""
Created on Tue Aug  7 15:42:15 2018

@author: egavis
"""

#should do a tinput too if time

import time

DELAY = 0.15
def tprint(text = "", multiplier = 1):
    time.sleep(DELAY * multiplier)
    print()
    print(text)
