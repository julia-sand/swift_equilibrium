import random as random

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from plotscript import *
from cost_v_time import *


def get_kappa(plotter,file_names,model_type,method,equil,constrained_kappa):
    T_vec = np.empty(0)
    kappa_vec = np.empty(0)

    for file_name in file_names:
        try:
            df = plotter.get_data(model_type,method,equil,file_name,constrained_kappa)

            kappa_vec = np.append(kappa_vec, df["kappa"].to_numpy()[-1])
            
            T_vec = append_Tf(plotter,file_name,T_vec)

        except (FileNotFoundError,ValueError):
            pass
    
    return T_vec, kappa_vec
    
def make_plot(model_type,method,file_out):
    plotter = PlotParams()
    # Plotting the cumulants
    fig = plotter.make_fig()
    gs = plotter.make_gridspec(fig)
    file_names_g00001 = ["T2-0_Lambda9-0_eps1_g0-0001.csv",
                  "T3-0_Lambda9-0_eps1_g0-0001.csv",
                  "T4-0_Lambda9-0_eps1_g0-0001.csv",
                  "T5-0_Lambda9-0_eps1_g0-0001.csv",
                  "T6-0_Lambda9-0_eps1_g0-0001.csv",
                  "T7-0_Lambda9-0_eps1_g0-0001.csv",
                  "T8-0_Lambda9-0_eps1_g0-0001.csv",
                  "T9-0_Lambda9-0_eps1_g0-0001.csv",
                  "T10-0_Lambda9-0_eps1_g0-0001.csv",
                  "T20-0_Lambda9-0_eps1_g0-0001.csv",
                  "T30-0_Lambda9-0_eps1_g0-0001.csv",
                  "T40-0_Lambda9-0_eps1_g0-0001.csv",
                  "T50-0_Lambda9-0_eps1_g0-0001.csv"]

    file_names_g0001 = ["T2-0_Lambda9-0_eps1_g0-001.csv",
                  "T3-0_Lambda9-0_eps1_g0-001.csv",
                  "T4-0_Lambda9-0_eps1_g0-001.csv",
                  "T5-0_Lambda9-0_eps1_g0-001.csv",
                  "T6-0_Lambda9-0_eps1_g0-001.csv",
                  "T7-0_Lambda9-0_eps1_g0-001.csv",
                  "T8-0_Lambda9-0_eps1_g0-001.csv",
                  "T9-0_Lambda9-0_eps1_g0-001.csv",
                  "T10-0_Lambda9-0_eps1_g0-001.csv",
                  "T20-0_Lambda9-0_eps1_g0-001.csv",
                  "T30-0_Lambda9-0_eps1_g0-001.csv",
                  "T40-0_Lambda9-0_eps1_g0-001.csv",
                  "T50-0_Lambda9-0_eps1_g0-001.csv"]
    
    file_names_g001 = ["T2-0_Lambda9-0_eps1_g0-01.csv",
                  "T3-0_Lambda9-0_eps1_g0-01.csv",
                  "T4-0_Lambda9-0_eps1_g0-01.csv",
                  "T5-0_Lambda9-0_eps1_g0-01.csv",
                  "T6-0_Lambda9-0_eps1_g0-01.csv",
                  "T7-0_Lambda9-0_eps1_g0-01.csv",
                  "T8-0_Lambda9-0_eps1_g0-01.csv",
                  "T9-0_Lambda9-0_eps1_g0-01.csv",
                  "T10-0_Lambda9-0_eps1_g0-01.csv",
                  "T20-0_Lambda9-0_eps1_g0-01.csv",
                  "T30-0_Lambda9-0_eps1_g0-01.csv",
                  "T40-0_Lambda9-0_eps1_g0-01.csv",
                  "T50-0_Lambda9-0_eps1_g0-01.csv"]
    

    file_names_g01 = ["T2-0_Lambda9-0_eps1_g0-1.csv",
                  "T3-0_Lambda9-0_eps1_g0-1.csv",
                  "T4-0_Lambda9-0_eps1_g0-1.csv",
                  "T5-0_Lambda9-0_eps1_g0-1.csv",
                  "T6-0_Lambda9-0_eps1_g0-1.csv",
                  "T7-0_Lambda9-0_eps1_g0-1.csv",
                  "T8-0_Lambda9-0_eps1_g0-1.csv",
                  "T9-0_Lambda9-0_eps1_g0-1.csv",
                  "T10-0_Lambda9-0_eps1_g0-1.csv",
                  "T20-0_Lambda9-0_eps1_g0-1.csv",
                  "T30-0_Lambda9-0_eps1_g0-1.csv",
                  "T40-0_Lambda9-0_eps1_g0-1.csv",
                  "T50-0_Lambda9-0_eps1_g0-1.csv"]

    plot_kappa_vec(plotter,fig,gs,file_names_g01,model_type,method)
    #plot_kappa_vec(plotter,fig,gs,file_names_g001,model_type,method)
    #plot_kappa_vec(plotter,fig,gs,file_names_g0001,model_type,method)
    #plot_kappa_vec(plotter,fig,gs,file_names_g00001,model_type,method)
    h,l = plt.subplot(gs[:,3:]).get_legend_handles_labels()

    fig.legend(h,l,
                                fontsize = plotter.fontsizetitles,
                                frameon=False,
                                handlelength=1,
                                loc="center right")
    

    #plt.figtext(0.5, 0.01, param_label, ha="center", fontsize=plotter.fontsizetitles, bbox={"facecolor":"orange", "alpha":0.5, "pad":5})
    plt.savefig(file_out,bbox_inches="tight")

    plt.close()

def plot_kappa_vec(plotter,fig,gs,file_names,model_type,method):

        
    r = random.random()
    b = random.random()
    g = random.random()

    color = (r, g, b)

    #get parameter label from filename
    param_label = None #plotter.make_paramlabel(file_names[-1])
    results = get_kappa(plotter,file_names,model_type,method,equil="equil",constrained_kappa="negative_constrained_kappa")
    results2 = get_kappa(plotter,file_names,model_type,method,equil="stiffness_control",constrained_kappa="negative_constrained_kappa")
    label_val = set_g(file_names[0],model_type,plotter)

    plt.subplot(gs[:,:3]).plot(results[0],results[1],"-x",label=f"g={label_val}",markersize=10,linewidth=plotter.lw-1,color=color,zorder=100)
    plt.subplot(gs[:,3:]).plot(results2[0],results2[1],"-x",label=f"g={label_val}",markersize=10,linewidth=plotter.lw-1,color=color,zorder=100)
    #plt.subplot(gs[:,:3]).text(x=0.02,y=0.95,s=panel_label,fontsize=plotter.fontsizetitles,fontweight="bold",transform=plt.subplot(ax).transAxes)
    plt.subplot(gs[:,:3]).set_ylim((0,1))
    plt.subplot(gs[:,:3]).set_xlabel(r"$t_f$")
    

if __name__=="__main__":
        
    #list what methods to try to plot. all those where the available parameters
    #  exist 
    #will be plotted, otherwise the entry will be skipped.
    model_type = "hard"#["harmonic","control","log","hard"] 
    method = "direct"
    make_plot(model_type,method,f"plots/kappa_v_time{model_type}_{method[0]}_0.png")
