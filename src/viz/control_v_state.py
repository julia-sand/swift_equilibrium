import os

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from plotscript import *
from cost_v_time import append_Tf, set_g, compute_data


def make_plot(file_names,model_type,method,file_out):
    #pdb.set_trace()
    plotter = PlotParams()
    # Plotting the cumulants
    fig = plotter.make_fig()
    gs = plotter.make_gridspec(fig)

    #get parameter label from filename
    param_label = None #plotter.make_paramlabel(file_names[-1])
    #equil = "equil"
    #pdb.set_trace()
    results1 = compute_data(plotter,file_names,model_type,method,equil="equil",file_out=file_out)
    results2 = compute_data(plotter,file_names,model_type,method,equil="stiffness_control",file_out=file_out)

    plt.subplot(gs[:,:3]).plot(results1[0],results1[3],"-v",label="State",#label=r"$\mathcal{W}_{t_f}$",
                                markersize=10,linewidth=plotter.lw,color=plotter.c1)

    plt.subplot(gs[:,:3]).plot(results2[0],results2[3],"-o",label="Control",#,label=r"$\mathcal{W}_{t_f}$",
                                markersize=10,linewidth=plotter.lw,color=plotter.c2)
    
    plt.subplot(gs[:,3:]).plot(results1[0],results1[1],"-v",label=r"$\mathcal{W}_{t_f}$",markersize=10,linewidth=plotter.lw,color=plotter.c2,zorder=200)
    plt.subplot(gs[:,3:]).plot(results2[0],results2[1],"-o",label=r"$\mathcal{E}_{t_f}$",markersize=10,linewidth=plotter.lw,color=plotter.c1,zorder=200)


    for ax in [gs[:,:3],gs[:,3:]]:
        plotter.format_ax_plain(plt.subplot(ax))
        plt.subplot(ax).plot(results1[0],np.zeros(len(results1[0])),"--",linewidth=plotter.lw,color="gray",zorder=0,alpha=0.5)


    if model_type=="hard":
        titles = ["Entropy Production","Work"]
    else:
        titles = ["Engineered Swift Equilibration","Minimum Work Transition"]
    plt.subplot(gs[:,:3]).set_title(titles[0],fontsize=plotter.fontsizetitles)
    plt.subplot(gs[:,3:]).set_title(titles[1],fontsize=plotter.fontsizetitles)

    plt.subplot(gs[:,3:]).text(x=0.02,y=0.95,s="(b)",fontsize=plotter.fontsizetitles,fontweight="bold",transform=plt.subplot(gs[:,3:]).transAxes)
    plt.subplot(gs[:,:3]).text(x=0.02,y=0.95,s="(a)",fontsize=plotter.fontsizetitles,fontweight="bold",transform=plt.subplot(gs[:,:3]).transAxes)
    
    h,l = plt.subplot(gs[:,:3]).get_legend_handles_labels()

    fig.legend(h,l,
                                fontsize = plotter.fontsizetitles,
                                frameon=False,
                                handlelength=1,
                                loc="center right")
    plt.figtext(0.5, 0.01, param_label, ha="center", fontsize=plotter.fontsizetitles, bbox={"facecolor":"orange", "alpha":0.5, "pad":5})
    plt.savefig(file_out,bbox_inches="tight")

    plt.close()

if __name__=="__main__":
        
    #input file
    file_names = ["T2-0_Lambda3-0_eps1_g0-1.csv",
                  "T3-0_Lambda3-0_eps1_g0-1.csv",
                  "T4-0_Lambda3-0_eps1_g0-1.csv",
                  #"T5-0_Lambda3-0_eps1_g0-1.csv",
                  "T6-0_Lambda3-0_eps1_g0-1.csv",
                  "T7-0_Lambda3-0_eps1_g0-1.csv",
                  "T8-0_Lambda3-0_eps1_g0-1.csv",
                  "T9-0_Lambda3-0_eps1_g0-1.csv",
                  #"T10-0_Lambda3-0_eps1_g0-1.csv",
                  #"T20-0_Lambda3-0_eps1_g0-1.csv",
                  #"T30-0_Lambda3-0_eps1_g0-1.csv"
                  #
                  ]
    
    #list what methods to try to plot. all those where the available parameters
    #  exist 
    #will be plotted, otherwise the entry will be skipped.
    model_type = "hard"#["harmonic","control","log","hard"] 
    method = "direct"#,"nondegenerate"]
    make_plot(file_names,model_type,method,f"plots/test_new_cost_{model_type}_{method}.png")
    #make_plot(file_names,model_type,method,f"plots/cost_{model_type}_{method}.pdf")

    #make_plot(file_names,model_type,method,False,f"noneq_cost_{model_type}_{method}.png")
    
