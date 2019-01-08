# -*- coding: utf-8 -*-
"""
Created on Tue Aug  7 13:04:18 2018

@author: egavis
"""
import os
import re
from readability import tprint

def write_csv(df, name):
    '''
    probably ok may cut index or redo
    '''
    #GIVE THEM AN OPTION TO CHANGE THE NAME
    f = re.sub(u"\.csv","", name)
    fname = f + "_cleaned.csv"
    c = 1
    matched = True
    while matched: #should prevent it from overwriting previous runs
        if fname in os.listdir("output"):
            fname = f + "_cleaned_" + str(c) + ".csv"
            c += 1
        else:
            matched = False
    tprint("Writing CSV: %s" % fname)
    df.to_csv("output/" + fname, index_label="index")
    tprint("Finished writing cleaned data to Output")
