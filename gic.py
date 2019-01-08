import cli
import initial
import columns
#import calcdates #Currently Defunct -- needs to be updated to column paradigm
import clean
import final
#from readability import tprint 


def main():
    #maybe wrap the whole thing in a try/except to help abstraction LOL 
    while True:
        #INTRO, loads file with intro text
        cli.cls(verbose = False)
        cli.load_cli_intro()
        cli.cls()
        
        #OPENING FILE
        df, named, fname = initial.load_in()
        cli.cls()
        
        #(RE)NAMING COLUMNS:
        columns.rename_cols(df, named)
        cli.cls()

        #ADD AGES FOR KIDS -- THIS IS GETTING ROLLED INTO CLEAN SOMEHOW     
        #calcdates.add_age(df)
        #cli.cls()

        #CLEAN THE STAFF
        #try:
        clean.clean_columns(df)
        #except Exception as e: #DEBUGGING
         #   print(e)
         #   input("")
        cli.cls()
       
        #WRITES TO CSV
        # Done but needs testing
        final.write_csv(df, fname)
        cli.cls()
    
        #Finish or restart
        cli.outro()
        
    #main() #recursive call, end cond is above (or earlier)
    #recursion may add up if run repeatedly; watch memory 
    #may add variable to run recursive call w/ more limited cli intro
    #could just make iterative tbh, though a giant loop
    
    
if __name__ == "__main__":
    main()
