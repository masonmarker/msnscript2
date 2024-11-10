# launches a .msn2 script


# prepare msn2 interpreter
from msn2python import run

# cmd argument support
import sys

# filenames to run
if len(sys.argv) <= 1:
    print('[-] at least one .msn2 file needs to be specified')
    exit(1)

# for each command line argument
for i in range(1, len(sys.argv)):
    
    # obtain the filename
    filename = sys.argv[i]
    breaking = False
    
    # quick file access
    if filename == 'test':
        filename = 'tests/misc.msn2'
    # discovering UI elements
    elif filename == 'elements':
        filename = 'demos/practical/auto/clicked.msn2'
    # running the console tutorial
    elif filename == 'help':
        filename = 'TUTORIAL/driver.msn2'
    # verifying msn2 integrity
    elif filename == 'verify':
        filename = 'tests/validator.msn2'  
    # starts the msn2 interpreter
    elif filename == 'int':
        filename = 'system/int.msn2'
    # launches a file browser for running an msn2 script
    elif filename == 'file':
        filename = 'system/file.msn2'
        
    # if the file does not end in .msn2, add it
    if not filename.endswith('.msn2'):
        filename += '.msn2'
    
    # run the script
    run(filename, sys.argv[i:len(sys.argv)])
    
    if breaking:
        break