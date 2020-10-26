# -*- coding: utf-8 -*-
"""
Created on Tue Aug  7 12:56:01 2018

@author: jgavis
"""

import pandas as pd
import cli
#from readability import tprint

def _convert_dates(df):
    '''
    called only in add_age
    '''
    rv = True
    #print("Converting dates")
    try:
        df['date'] = pd.to_datetime(pd.Series(df['date']))
        df['birthdate'] = pd.to_datetime(pd.Series(df['birthdate']))
        #print("Dates converted")
    except: 
        cli.ask_continue()
        rv = False
    return rv

def add_age(df):
    '''
    '''
    print("Would you like to calculate participants' ages?")
    age = cli.ask_yes(True)
    if not age:
        return
    print("Adding ages")
    converted = _convert_dates(df)
    if converted:
        y = []
        for i in range(len(df)):
            y.append(df["date"].iloc[i].year 
                     - df["birthdate"].iloc[i].year)
        df["age"] = y
        print("Ages added")
        print()
        #May want try/except and prompt to continue
    else:
        print("Error converting dates. Ages not calculated")
        print()
