import numpy as np
import matplotlib.pyplot as plt
from plotscript import PlotParams #contains the plotting functions

##plots different file names 
def plot_result(model,method,file_names,file_out,equil):
    plotter = PlotParams()
    #change here if you want the label or not
    param_label = plotter.make_paramlabel(file_names[0]) #label will show the top value
    
    fig_out = plotter.make_plot([model],[method],file_name,param_label,equil=equil) 
    fig_out.savefig(file_out, bbox_inches="tight")

    plt.close()


if __name__=="__main__":

    file_names = ["T3-0_Lambda1-4_eps1_g0-001.csv",
                    "T3-0_Lambda1-4_eps1_g0-01.csv",
                    "T3-0_Lambda1-4_eps1_g0-1.csv"]
    
    models = ["log","control"] #"harmonic",
    methods = ["slowfast","indirect","direct"]
    for file_name in enumerate(file_names):
        plot_result(models,methods,file_name[1],f"equil_plot{file_name[0]}.png", True)
        plot_result(models,methods,file_name[1],f"noneq_plot{file_name[0]}.png", False)
