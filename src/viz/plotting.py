import numpy as np
import matplotlib.pyplot as plt
from plotscript import PlotParams #contains the plotting functions

def adjust_subplot_lims(gs):
    plt.subplot(gs[1,3:]).set_ylim((-20,20))
    plt.subplot(gs[1,:3]).set_ylim((-0.7,1.5))
    plt.subplot(gs[0,4:]).set_ylim((-0.3,0.4))

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


    adjust_subplot_lims(gs_cumulants)
    fig_out.savefig(file_out, bbox_inches="tight")

    plt.close()


if __name__=="__main__":

    #data input file name. This is the file that will 
    #be plotted if available. 
    file_names =  [
                   # "T2-0_Lambda3-0_eps1_g0-1.csv",
                    "T3-0_Lambda1-4_eps1_g0-0001.csv",
                    #"T3-0_Lambda3-0_eps1_g0-01.csv",
                   #"T30-0_Lambda3-0_eps1_g0-1.csv",
                   #  "T5-0_Lambda3-0_eps1_g0-1.csv",
                   # "T6-0_Lambda3-0_eps1_g0-1.csv",
                   # "T7-0_Lambda3-0_eps1_g0-1.csv",
                   ]
    models = ["harmonic"] #"harmonic",
    methods = ["indirect"]#["slowfast","direct","indirect"]
    plot_result(models,methods,file_names,f"plots/cumulants_noneq_{models[0]}.png", "noneq","none")
    #plot_result(models,methods,file_names,f"plots/cumulants_stiffnesscontrol_{models[0]}.pdf", "stiffness_control","negative_constrained_kappa")
