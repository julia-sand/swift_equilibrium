import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
#import pandas as pd
from plotscript import * #contains the plotting functions

#data input file name. This is the file that will 
#be plotted if available. 
file_name = "T3-0_Lambda3-0_eps1-0_g0-01.csv"
file_out = "swift_equilibrium/plots/test1.png"

#list what methods to try to plot. all those where the available parameters
#  exist 
#will be plotted, otherwise the entry will be skipped.
models = ["hard"]#,"control","log","hard"] 
methods = ["direct","indirect","slowfast"]

#change here if you want the label or not
param_label = make_paramlabel(file_name)

fig_out = make_plot(models,methods,file_name,param_label,equil=False) 
fig_out.savefig(file_out, bbox_inches="tight")

plt.close()
