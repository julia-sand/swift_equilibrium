import os

import numpy as np
import pandas as pd

from plotscript import PlotParams #contains the plotting functions

#verifies boundary conditions of the  a given csv file

if __name__=="__main__":

    directory = os.fsencode("results/harmonic/noneq/indirect")
    plotter = PlotParams()

    for file in os.listdir(directory):
        filename = os.fsdecode(file)
        param_label = plotter.make_paramlabel("results/harmonic/noneq/indirect/"+filename)
        df = pd.read_csv("results/harmonic/noneq/indirect/"+filename)

        match_bc = (df.y4.to_numpy()[-1] - (-df.kappa.to_numpy()[-1]/2))
        print(rf"{param_label}")
        print(f"BC: {match_bc}")
    