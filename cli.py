# -*- coding: utf-8 -*-
"""
Created on Tue Aug  7 09:44:15 2018

@author: egavis
"""

import os
import sys
from readability import tprint
import jellyfish

def cls(verbose = True):
    if verbose:
        print()
        input("Press Enter\t")
    os.system('cls' if os.name=='nt' else 'clear')

def load_cli_intro():
    '''
    loads the intro from text/intro.txt
    currently no input/return
    '''
    with open("text/intro.txt") as f:
        t = f.read()
    tprint(t)
    print()

def end():
    '''
    just prints "Exiting" then calls sys.exit() 
    '''
    tprint("Exiting")
    print()
    input("Press Enter\t")
    sys.exit()

def ask_yes(positive = True):
    '''
    basically Y = True, N = False, works intuitively
    could make variables later to make this clearer
    '''
    #could add an unspecified to prevent them just clicking through vitals
    rv = positive
    if positive:
        choice = input("[Y]/N:\t")
        if choice.lower() == "n":
            rv = False
    else:
        choice = input("Y/[N]:\t")
        if choice.lower() == "y":
            rv = True
    print()
    return rv

def ask_continue(default = True):
    '''
    '''
    tprint("Would you like to continue cleaning data?")
    if not ask_yes(default):
        end()

def outro():
    '''
    '''
    print("Finished cleaning data")
    ask_continue(False)
    cls(verbose = False)

def ask_meant(guess, default = False):
    '''
    '''
    tprint("Did you mean to choose %s?" % guess)
    rv = ask_yes(default)
    return rv

def guess(original, options):
    '''
    original: string
    options: iterable of strings
    returns "" if Not original or 0 matchs, otherwise returns <guess>(str)
    
    currently using Jaro-Winkler metric for str comparison
    '''
    rv = ""
    if original:
        original = original.lower()
        base = 0
        for option in options:
            jw = jellyfish.jaro_winkler(original, option.lower())
            if jw > base:
                rv = option
                base = jw
    return rv
