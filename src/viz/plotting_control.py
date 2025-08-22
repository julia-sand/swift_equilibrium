import numpy as np
import matplotlib.pyplot as plt
from plotscript import PlotParams #contains the plotting functions

def plot_result(models,methods,file_names,file_out):
    plotter = PlotParams()
    #change here if you want the label or not
    #param_label = plotter.make_paramlabel(file_name)
    
    fig_out = plotter.make_fig()
    gs_cumulants = plotter.make_gridspec(fig_out)
    plotter.plot_all_cumulants(fig_out,gs_cumulants,
                                    ["hard"],
                                    ["direct"],
                                    ["T3-0_Lambda1-0_eps1_g0-1.csv"],
                                    equil="stiffness_control")
    plotter.plot_all_cumulants(fig_out,gs_cumulants,
                                    ["hard"],
                                    ["direct"],
                                    ["T3-0_Lambda10-0_eps1_g0-1.csv"],
                                    equil="equil")
    fig_out.savefig(file_out, bbox_inches="tight")

    plt.close()


if __name__=="__main__":

    #data input file name. This is the file that will 
    #be plotted if available. 
    file_names =  ["T3-0_Lambda10-0_eps1_g0-1.csv"]
                    #"T3-0_Lambda3-0_eps1_g0-01.csv",
                    #"T3-0_Lambda4-0_eps1_g0-01.csv"]
    models = ["control"] #"harmonic",
    methods = ["direct"]#["slowfast","direct","indirect"]
    plot_result(models,methods,file_names,f"plots/T70_plot_{models[0]}.pdf")
    plot_result(models,methods,file_names,f"plots/T70_plot_{models[0]}.png")
