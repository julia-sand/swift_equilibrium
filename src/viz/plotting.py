import numpy as np
import matplotlib.pyplot as plt
from plotscript import PlotParams #contains the plotting functions


def plot_result(models,methods,file_names,file_out,equil):
    plotter = PlotParams()
    for file_name in enumerate(file_names):
        print(file_name)
        #change here if you want the label or not
        param_label = plotter.make_paramlabel(file_name[1])
        
        fig_out = plotter.make_plot(models,methods,file_name[1],param_label,equil=equil) 
        fig_out.savefig(file_out+f"{file_name[0]}.png", bbox_inches="tight")

        plt.close()


if __name__=="__main__":

    #data input file name. This is the file that will 
    #be plotted if available. 
    file_names = ["T10-0_Lambda1-4_eps1-0_g0-5.csv"]
                   #"T3-0_Lambda3-0_eps1-0_g0-1.csv",
                   #"T3-0_Lambda1-4_eps1-0_g0-1.csv",
                   #"T5-0_Lambda1-4_eps1-0_g0-5.csv" ]
    file_out = "test10"

    #list what methods to try to plot. all those where the available parameters
    #  exist 
    #will be plotted, otherwise the entry will be skipped.
    models = ["harmonic","control","log","hard"] 
    methods = ["slowfast","indirect","direct"]
    equil = True  
    plot_result(models,methods,file_names,file_out, equil)
