"""
This file should be run first in order to make the results directory 
and save the results as CSVs. 

"""

import os

def make_results_dir():
    """
    Makes results directory to store CSVs from integration.
    """

    #get cwd
    cwd = os.getcwd()
    try:
        #hard penalty
        os.makedirs(cwd+"/results/hard/equil/direct", exist_ok = False) 
        os.makedirs(cwd+"/results/hard/noneq/direct", exist_ok = False) 
        os.makedirs(cwd+"/results/hard/stiffness_control/direct", exist_ok = False) 

        #log 
        os.makedirs(cwd+"/results/log/equil/indirect", exist_ok = False) 
        
        #harmonic
        for method in ["direct","indirect","slowfast"]:
            os.makedirs(cwd+f"/results/harmonic/equil/{method}", exist_ok = False)
        
        os.makedirs(cwd+f"/results/harmonic/noneq/indirect", exist_ok = False)

    except OSError:
        print("A results directory already exists in this folder.")
        pass

if __name__=="__main__":
    make_results_dir()