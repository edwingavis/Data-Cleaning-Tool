# -*- coding: utf-8 -*-
"""
Created on Tue Aug  7 12:49:19 2018

@author: egavis
"""

#REWRITE TO DO SOMETHING MUCH MORE COMPLICATED

#import pandas as pd
import cli
from readability import tprint

#NOTE: IF DF imported W/ header = None, column names will just be integers 

def rename_cols(df, named):
    '''
    takes dataframe, bool for whether columns are already named 
    modifies df in place, no return
    '''
    if not named: 
       give_new_names(df)
    else:
        tprint("Column names have been updated for compatibility")
    modify_column_names(df)

def give_new_names(df):
    '''
    '''
    names = []
    num_cols = len(df.columns)
    for i in range(num_cols):
        default_name = "column_" + str(i+1)
        print("Column " + str(i+1) + " of " + str(num_cols) + " is currently named: " + default_name)
        show_first_values(df, i)
        chosen = False
        while not chosen:
            name = input("Enter a new name for this column or press Enter to keep the default: ")
            name = name.strip() 
            if name:
                com_name = name.lower().replace(" ", "_")
                tprint("Modifying input for compatibility: " + name + " -> " + com_name)
                tprint("Would you like to name this column " + com_name + " ?")
                chosen = cli.ask_yes(True)
                if chosen: 
                    tprint("Setting column name")
                    if name in names:
                        print("Name already used for a column. Please choose another")
                    else:
                        names.append(name)
                else:
                    chosen = ask_default(names, default_name, False)
            else:
                chosen = ask_default(names, default_name, True)                  
        cli.cls()
    #setting the new names
    tprint("Adding column names")
    df.columns = names
    cli.cls()    
    
def ask_default(names, default_name, default = True):
    '''
    '''
    rv = False
    tprint("Would you like to use the default name?")
    if cli.ask_yes(default):
        names.append(default_name)
        rv = True
    return rv   

def show_first_values(df, col, count = 5):
    '''
    '''
    tprint("First %d unique values from this column:" % count) 
    values = list(df.iloc[:,col].unique())
    c = 0
    for v in values:
        print("\t" + str(v))
        c += 1
        if c >= count:
            break
    print()

    
def modify_column_names(df):
    '''
    '''
    modding = True 
    while modding:
        #THIS NEEDS TO BECOME A FXN CALL... SO CAN USE W/ named = False
        df.columns = fix_current_columns(df)
        tprint("Would you like to modify a column's name?")
        modding = cli.ask_yes(False) 
        if modding:
            print()
            col = input("Choose the number of the column to modify (1, 2, 3...): ")
            try:
                i = int(col.strip()) - 1
                cli.cls(verbose = False)
                tprint("Renaming column: " + df.columns[i])
                print()
                new = input("Type new name: ").strip()
                new = make_compatible(new)
                if new:
                    tprint("Converting name for compatibility")
                    tprint("Would you like to rename " 
                                + df.columns[i] + " to " + new + " ?")
                    if cli.ask_yes(True): 
                        change_one_column(new, df, i)                              
                else:
                    tprint("No new column name detected") 
            except Exception as e: #debugging
                tprint("Error renaming column")
               #print(e)
            cli.cls()

def change_one_column(new, df, i):
    '''
    given column name string (new), dataframe (df) and index of column (i)
    makes df.columns[i] = new
    '''
    updated = list(df.columns)
    updated[i] = new
    df.columns = updated

def fix_current_columns(df, list_only = False):
    '''
    given dataframe (df), accesses column names
    ensures column names are in format <column_name> then prints them
    returns list of properly formatted column names
    '''
    tprint("Columns:")
    compat = []
    i = 0 
    for old in df.columns:
        i += 1
        if not list_only:
            new = make_compatible(old)
            compat.append(new)
        else: #ugly fix atm
            new = old
        print("\t" + str(i) + ") " + new)
    return compat
    
def make_compatible(name):
    '''
    takes a string and returns a version of it with following modifications:
    ends stripped of white space
    lowercase
    " " -> "_" 
    '''
    return name.strip().lower().replace(" ", "_")
