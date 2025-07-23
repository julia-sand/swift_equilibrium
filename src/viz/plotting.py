import numpy as np
import matplotlib.pyplot as plt
from plotscript import PlotParams #contains the plotting functions

def plot_result(models,methods,file_names,file_out,equil,constrained_kappa):
    plotter = PlotParams()
    #change here if you want the label or not
    #param_label = plotter.make_paramlabel(file_name)
    
    fig_out = plotter.make_fig()
    gs_cumulants = plotter.make_gridspec(fig_out)
    plotter.plot_all_cumulants(fig_out,gs_cumulants,
                                    models,
                                    methods,
                                    file_names,
                                    equil=equil,constrained_kappa=constrained_kappa)
    
    fig_out.savefig(file_out, bbox_inches="tight")

    plt.close()


if __name__=="__main__":

    #data input file name. This is the file that will 
    #be plotted if available. 
    file_names =  [
                   # "T2-0_Lambda3-0_eps1_g0-1.csv",
                    "T4-0_Lambda3-0_eps1_g0-1.csv",
                   "T30-0_Lambda3-0_eps1_g0-1.csv",
                   #  "T5-0_Lambda3-0_eps1_g0-1.csv",
                   # "T6-0_Lambda3-0_eps1_g0-1.csv",
                   # "T7-0_Lambda3-0_eps1_g0-1.csv",
                   ]
    models = ["hard"] #"harmonic",
    methods = ["direct"]#["slowfast","direct","indirect"]
    #plot_result(models,methods,file_names,f"plots/equil_plot_{models[0]}.png", True)
    #plot_result(models,methods,file_names,f"plots/stiffness_control_plot_{models[0]}.png", "stiffness_control")
    plot_result(models,methods,file_names,f"plots/hard_equil_plot_{models[0]}.png", "equil","constrained_kappa")
    plot_result(models,methods,file_names,f"plots/hard_noneq_plot_{models[0]}.png", "noneq","constrained_kappa")
    plot_result(models,methods,file_names,f"plots/hard_stiffcontrol_plot_{models[0]}.png", "stiffness_control","none")
