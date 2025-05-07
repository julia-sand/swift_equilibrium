import numpy as np
import matplotlib.pyplot as plt
from plotscript import PlotParams #contains the plotting functions


def plot_result(models,methods,file_name,file_out):
    plotter = PlotParams()

    #change here if you want the label or not
    param_label = plotter.make_paramlabel(file_name)

    fig_out = plotter.make_plot(models,methods,file_name,param_label,equil=False) 
    fig_out.savefig(file_out, bbox_inches="tight")

    plt.close()


if __name__=="__main__":

    #data input file name. This is the file that will 
    #be plotted if available. 
    file_name = "T3-0_Lambda3-0_eps1-0_g0-01.csv"
    file_out = "swift_equilibrium/plots/test1.png"

    #list what methods to try to plot. all those where the available parameters
    #  exist 
    #will be plotted, otherwise the entry will be skipped.
    models = ["hard"]#,"control","log","hard"] 
    methods = ["direct","indirect","slowfast"]

    plot_result(models,methods,file_name,file_out)
