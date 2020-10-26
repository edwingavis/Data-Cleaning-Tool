# -*- coding: utf-8 -*-
"""
Created on Tue Aug  7 13:00:38 2018

@author: jgavis
"""
import itertools
import math
import os
import cli
import columns
from readability import tprint
import jellyfish
#import numpy
#from pandas.api.types import is_string_dtype
from pandas.api.types import is_numeric_dtype

###LAST UPDATE IS: CHOOSE_RECORD()

def clean_columns(df):
    '''
    '''
    #could also just iterate through columns
    working = True
    while working: #NEED TO THINK ABOUT BOOL HERE, CURRENTLY NO END COND.
        print("DATA CLEANING")
        col, working = choose_col(df, working)   #df.iloc[:,i]
        cli.cls()
        if working and col: #lil ugly
            drop_na(df, col)
            cli.cls()
            numeric = assess_data_type(df[col])
            if numeric:
                clean_numeric(df, col)
            else:
                check_mixed_data(df, col)
            
def choose_col(df, working):
    '''
    '''
    columns.fix_current_columns(df, list_only = True) #really ugly fix in columns atm
    print()
    col = input("Choose the number of a column to clean (1, 2, 3...) or press Enter: ")
    try:
        i = int(col.strip()) - 1  #maybe should do something w/ the name...
        col_name = df.columns[i]
    except Exception as e: 
        col_name = ""
        tprint("No column selected")
        tprint("Would you like to continue cleaning columns?")
        working = cli.ask_yes(True)
        #print(e) #debugging
    return col_name, working 
    
def drop_na(df, col):
    '''
    '''
    tprint("Would you like to remove the rows that do not contain a value for: %s?" % col)
    if cli.ask_yes(True):
        df.dropna(subset = [col])

def assess_data_type(column):
    '''
    '''
    rv = is_numeric_dtype(column)  
    #may add other utilities
    return rv 
    
def check_mixed_data(df, col):
    '''
    '''
    #currently mostly unbuilt 
    df[col] = df[col].astype(str)
    if check_numeric(df[col]):
        pass
        #convert_data(df, col) #probably need a separate fxn for this
    elif check_dates(df[col]): #currently always False b/c not built
        convert_data(df, col) 
    elif ask_convert(df, col):
        convert_data(df, col) #just displays message 
    else:
        clean_strings(df,col)
    
def ask_convert(df, col):
    '''
    '''    
    rv = False
    print("This column seems to contain text data")
    tprint("Is this column supposed to contain dates or numeric data?")
    if cli.ask_yes(False):
        rv = True
    #cli.cls()
    return rv
    
#UNFINISHED
def convert_data(df, col):
    '''
    '''
    #replace when finished
    tprint("Unfortunately this feature is not currently supported")
    tprint("Stay tuned for future releases and updates")
    cli.cls()
    #clean_strings(df, col) #should probably just go back to selection screen

def check_numeric(column):
    '''
    '''
    #BigO - 2n-ish?
    nums = column.str.isnumeric()
    for n in nums:
        if n:
            return True
    return False

#UNFINISHED
def check_dates(col):
    '''
    this should only actually do conversion if we're adding support for 
    date functions. otherwise should just prevent string fxns being called on
    dates
    '''
    return False

WARN_LEVEL = 1000
def clean_strings(df, col):
    '''
    '''
    tprint("Removing excess white space from values in %s" % col)
    df[col] = df[col].str.strip()
    df[col] = df[col].str.replace(" ,", ",")
    df[col] = df[col].str.replace(",,", ",")
    df[col] = df[col].str.replace("  ", " ")
    df[col] = df[col].str.replace("\t", " ") 
    cli.cls()
    u = df[col].unique()
    num_unique = len(u)
    print("Column " + col + " contains " + str(num_unique) + " unique values")
    if num_unique > WARN_LEVEL:
        tprint("Large numbers of unique values may take significant time to analyze, depending on their length, your system and settings")
    tprint("Would you like to search for possible errors in the data?")
    guesses = []
    if cli.ask_yes(True):
        cli.cls(False)
        guesses = consolidate_guesses(guess_linkages(u)) #doing a lot w/ generator
        if guesses:
            review_guesses(df, col, guesses)
            tprint("All automatic revisions reviewed")
        else:
            tprint("Our review did not detect any likely errors")
    cli.cls()
    ######################
    #DO THE MANUAL VERSION
    print("Current unique values in %s:" % col)
    show_values(df, col)
    cli.cls()
    print("Would you like to further clean or modify the values in %s?" % col)
    if cli.ask_yes(True):
        previous = [] #make previous update w/ confirmed automatic fixes... 
        # ^ this will take some work
        fix_manual(df, col, previous)
    
def clean_numeric(df, col):
    '''
    '''
    tprint("Would you like to see summary statistics for the data in this column?")
    if cli.ask_yes(True):
        tprint(df[col].describe())
    cli.cls()
    #Nothing else currently but explore doing outliers etc.
    #no actual data cleaning occurring aside from dropping NA

def consolidate_guesses(guesses):
    '''
    guesses is iterable of (str, str) guesses
    this isn't awful in terms of complexity if half reasonable numbers
    memory could be better 
    but again shouldn't be a huge issue at reasonable sizes
    '''
    rv = []
    for g in guesses:
        placed = False
        for s in rv:
            if g[0] in s or g[1] in s:
                s.add(g[0])
                s.add(g[1])
                placed = True
        if not placed:
            s = set()
            s.add(g[0])
            s.add(g[1])
            rv.append(s)
    rv = [sorted(s) for s in rv]
    return rv

def review_guesses(df, col, guesses):
    '''
    '''
    #need to think about consolidating if there are a bunch of similar
    #build so g can contain 2+ values
    for g in guesses:
        print("Similar Value (Number in data):")
        i = 1
        #exists is a p-jank solution for not having consolidate_guesses...
        exists = 0
        for v in g: 
            num_v = len(df[df[col] == v])
            if num_v:
                exists += 1
            print("\t" + str(i) + ") "+ v + "\t(%d)" % num_v)
            i += 1
        if exists <= 1:
            cli.cls(False)
            continue
        tprint("Would you like to update one or more of these values?")
        if cli.ask_yes(False):
            fix_guess(g, df, col)
        cli.cls(True)
        
def fix_guess(g, df, col):
    '''
    '''
    #BUILD SOMETHING TO SAVE THESE CHANGES
    #NEEDS RETURNS HERE AND IN SWITCH DATA
    print() 
    c = input("Choose the number of the correct value (1, 2...) or press Enter to use a custom value:  ")
    try: 
        c = int(c.strip()) - 1
        correct = g[c]
        switch_data(df, col, g, c, correct)                                                          
    except Exception as e:
        #print(e) #debugging
        chosen = False
        while not chosen:
            custom = input("Enter a new correct value or press Enter to cancel:  ")
            custom = custom.strip()
            if custom:
                tprint("Use %s ?" & custom)
                chosen = cli.ask_yes(True)
                if chosen:
                    switch_data(df, col, g, -1, custom) 
                    #-1 is jank fix for how switch_data currently works
            else:
                chosen = True            

def switch_data(df, col, g, c, correct):
    '''
    '''
    try:
        for i in range(len(g)):
            if i != c:
                tprint("Would you like to convert " + g[i] + 
                       " to " + correct + "?")
                if cli.ask_yes(True): 
                    df.loc[df[col] == g[i], 
                           [col]] = correct
                    tprint("Converting " + g[i] + " -> " + correct, 0.5)
    except Exception as e: 
        tprint("Error converting data. Data not converted")
        #print(e) #debugging              

THRESHOLD = 0.9
def guess_linkages(u):
    '''
    Generator: yields tuples (str, str) 
    '''
    for v1, v2 in itertools.combinations(u, 2):
        jw = jellyfish.jaro_winkler(v1.lower(), v2.lower())
        if jw >= THRESHOLD:
            #print((v1, v2, jw)) DEBUGGING
            yield (v1, v2)    

def show_values(df, col, output = False, values = []):
    '''
    if output returns chosen value
    '''
    i = 0
    if not values: #THIS IS A BIT SILLY
        values = sorted(df[col].unique())
    pages = math.ceil(len(values)/10)
    print("Current unique values: (Page 1 of %d)" % pages)
    for v in values:
        i += 1
        print("\t" + str(i) + ") " + v)
        if not output:
            if i % 10 == 0 and i < len(values):
                tprint("Show more values?")
                if cli.ask_yes(True):
                    cli.cls(False)
                    print("Current unique values: (Page %d of %d)" 
                              % (i/10 + 1,pages))
                else:
                    break
        else:
            if i % 10 == 0 or i == len(values):
                print()
                more = i < len(values)
                choosing = True
                while choosing: #currently always true and break/return out
                    if more:
                        c = input("Type the number of a value (1, 2...) or press Enter to view more values: ")
                    else:
                        c = input("Type the number of a value to select it (1, 2, 3...):  ")
                    try:
                        c = int(c)
                        rv = str(values[c-1])
                        return rv
                    except:
                        tprint("No value selected")
                        if more:
                            tprint("View more values?")
                            if cli.ask_yes(True):
                                cli.cls(False)
                                print("Current unique values: (Page %d of %d)" 
                                      % (i/10 + 1,pages))
                                break

def select_value(df, col):
    '''
    '''
    rv = ""
    chosen = False
    print()
    while not chosen:
        rv = show_values(df, col, output = True) #NEEDS COL 
        chosen = cli.ask_meant(rv, default = True)
        if not chosen:
            cli.cls(verbose = False)
    return rv  

def fix_manual(df, col, previous = []):
    '''
    '''
    working = True
    while working: 
        tprint("Would you like to load a record of previously used changes?")
        if cli.ask_yes(True):
            fixes = choose_record(df, col, previous) #REDO/RENAME
            if not fixes:
                fixes = add_new_fixes(df, col, previous)
        else:
            cli.cls()
            fixes = add_new_fixes(df, col, previous)
        print("Applying fixes")
        for old, new in fixes.items():
            df.loc[df[col] == old, 
                   [col]] = new
        tprint("Fixes applied")
        cli.cls()
        show_values(df, col)
        tprint("Would you like to further modify the values in %s?" % col)
        working = cli.ask_yes(True)
        cli.cls()

def add_new_fixes(df, col, previous):
    finished = False
    fixes = {}
    while not finished: 
        #MAKE A FUNCTION FROM A BUNCH OF THIS SO CAN USE WITH EXISTING...
        tprint("Choose a value to replace")
        old = select_value(df, col)
        tprint("Would you like to choose another existing value to replace: %s ?" % old)
        print("(Otherwise you will be prompted to enter a custom replacement value)")
        if cli.ask_yes(True):
            cli.cls(False)
            tprint("Choose a value to replace '%s'" % old)
            new = select_value(df, col)
        else:
            chosen = False
            while not chosen:
                new = input("Enter custom value to replace %s:\t" % old)
                if new:
                    tprint("Use %s ?" % new)
                    chosen = cli.ask_yes(True)                         
        cli.cls(verbose = False)        
        if old and new:
            tprint("You chose: " + old + " -> " + new)
            tprint("Confirm this replacement?")
            if cli.ask_yes(True):
                tprint("Confirmed")
                fixes[old] = new
            cli.cls()
        if fixes:
            print("Your chosen replacements:")
            tprint("\tCurrent\tReplaced")
            sort_fixes = sorted(fixes.items())
            for old, new in sort_fixes:
                print("\t" + old + "\t" + new)
            tprint("Would you like to add another replacement?")
            if cli.ask_yes(True):  
                cli.cls()
                continue #*Slightly* jank
            tprint("Would you like to save a record of these replacements for future use?")
            if cli.ask_yes(True):
                if previous:
                    tprint("Would you like to include the changes you selected from our suggestions in this record?")
                    if cli.ask_yes():
                        for p in previous:
                            fixes[p[1]] = p[0]
                        sort_fixes = sorted(fixes.items())
                cli.cls()
                named = False
                while not named:
                    name = input("Choose a name for this record:\t")
                    name = name.lower().strip()
                    tprint("Do you want to name this record:  %s  ?" % name)
                    named = cli.ask_yes(True)
                    cli.cls(verbose = False)
                with open("data/" + name + ".txt", 'w') as f:
                    for old, new in sort_fixes:
                        f.write(old + '///' + new)
                        if old != sort_fixes[-1]:
                            f.write("\n")
            finished = True
    return fixes

def choose_record(df, col, previous): 
    '''
    returns dict of old -> new
    large parts of this fxn are currently deprecated, unclear if stable
    '''
    org = ""
    #suggest = True
    rv = {}
    chosen = False #this is basically a C paradigm tbh
    while not chosen:
        #REDO STRINGS/SELECTION
        '''
        if not org:
            print("Choose an organization from the list below:")
            for org in sorted(os.listdir("staff")): #REQUIRED DIR: staff
                print(org.strip(".txt").replace("_", " "))
            print("Other")
            print()
            org = input("Organization:\t").strip().upper().replace(" ", "_")
            print()
        if org == "OTHER":
            start_record(df, True)
            org = ""
            continue
            #DO SOMETHING FOR OTHER -- requires making new file --> continue, maybe redisplay orgs
        else:
        '''
        val = [n.strip(".txt") for n in os.listdir("data") if ".txt" in n] #that is some l-comp
        org = show_values(df, col, output = True, values = val)
        try:
            fname = org + ".txt"
            with open("data/" + fname) as f:
                data = f.readlines()
            for row in data:
                try:
                    old, fix = row.split("///")
                    rv[old] = fix.strip()
                except ValueError: 
                    #This may hurt abstraction too much as is
                    tprint("Bypassing incorrectly formatted data")
                    #print(row) #probably just cut this tbh
            chosen = True
            tprint(org + " data loaded")          
        except FileNotFoundError:
            tprint("Error loading record")
            tprint("Would you like to start a new record?")
            if cli.ask_yes(True):
                chosen = True
            '''
            print("Records not found")
            print()
            if suggest and org:
                likely = cli.guess(fname.strip(".txt"), 
                                   os.listdir('staff'))
                if likely:
                    corrected = cli.ask_meant(likely.strip(".txt"))
                    if corrected:
                        org = likely
                        suggest = False                           
                        continue
                    else:
                        org = "" 
                        cli.cls(verbose = False)
                else:
                    cli.cls(verbose = False)
            #put rest INSIDE THIS BLOCK block so correction -> straight to return rv
            if not suggest: 
                add_new_fixes(df, col, present)
            '''
    return rv        
    
def start_record(df, col, default = True):
    '''
    '''
    print("Would you like to create a new organization?")
    new = cli.ask_yes(default)
    print()
    if not new:
        #cli.ask_continue(False)
        cli.cls(verbose = False)
        return
    named = False
    while not named:
        name = input("Type organization name or abbreviation:\t")
        name = name.upper().strip()
        print()
        print("Do you want to name this record: %s ?" % name)
        named = cli.ask_yes(True)
        cli.cls(verbose = False)
    fname = name.replace(" ", "_") + ".txt"
    #maybe put failsafe guess here... or have option to merge records later 
    #^ probably latter tbh.
    add_new_fixes(df, col, fname)
