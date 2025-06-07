import numpy as np
import matplotlib.pyplot as plt
from plotscript import PlotParams #contains the plotting functions

def plot_result(models,methods,file_name,file_out,equil):
    plotter = PlotParams()
    #change here if you want the label or not
    param_label = plotter.make_paramlabel(file_name)
    
    fig_out = plotter.make_plot(models,methods,file_name,param_label,equil=equil) 
    fig_out.savefig(file_out, bbox_inches="tight")

    plt.close()


if __name__=="__main__":

    #data input file name. This is the file that will 
    #be plotted if available. 
    file_names = ["T3-0_Lambda1-4_eps1-0_g0-001.csv"]
    
    #list what methods to try to plot. all those where the available parameters
    #  exist 
    #will be plotted, otherwise the entry will be skipped.
    models = ["harmonic","control","log","hard"] 
    methods = ["slowfast","indirect","direct"]
    equil = True  
    for file_name in enumerate(file_names):
        plot_result(models,methods,file_name[1],f"plot{file_name[0]}.png", equil)
