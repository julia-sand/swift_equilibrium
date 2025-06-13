import numpy as np
import math

import pandas as pd
import matplotlib.pyplot as plt

from plotscript import PlotParams

def work_plot():

    plotter = PlotParams()
    
    #get parameter label from filename
    param_label = plotter.make_paramlabel(file_name)

    # Plotting the cumulants
    fig = plt.figure(figsize=(15, 8))#, constrained_layout=True)

    plotter.plot_func(ax,
                        times_vec,
                        entropy_production,
                        None,
                        f"{method}")