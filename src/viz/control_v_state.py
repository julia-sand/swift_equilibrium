import os

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from plotscript import *
from cost_v_time import append_Tf, compute_data

def w2_dist_equil_constrained_kappa():
    """estimate_w2.py
    compute_w2(20000,ex1())
    """

    return 0.27043526719524696

def w2_dist_stiffness_control_constrained_kappa():
    """estimate_w2.py
    compute_w2(20000,ex2())
    """
    
    return 0.28075074424154

def w2_dist_equil_negative_constrained_kappa():
    """estimate_w2.py
    compute_w2(20000,ex3())
    """
    
    return 0.2654354307708025


def w2_dist_stiffness_control_negative_constrained_kappa():
    """estimate_w2.py
    compute_w2(20000,ex4())
    """
    
    return 0.26973955322968945

def plot_w2(ax,w2,color1,case,tf):
    plt.subplot(ax).plot(np.linspace(3,tf,num=20),w2/np.linspace(3,tf,num=20),
                linestyle="dashed",color=color1,alpha=0.5,lw=plotter.lw, label=r"$\frac{1}{t_f}\mathcal{W}_2$"+"("+case+")")

def choose_w2(equilvar,constraint):
    function_name = "w2_dist_"+equilvar+"_"+constraint
    return {
        'w2_dist_equil_constrained_kappa': lambda: w2_dist_equil_constrained_kappa(),
        'w2_dist_stiffness_control_constrained_kappa': lambda: w2_dist_stiffness_control_constrained_kappa(),
        'w2_dist_equil_negative_constrained_kappa': lambda: w2_dist_equil_negative_constrained_kappa(),
        'w2_dist_stiffness_control_negative_constrained_kappa': lambda: w2_dist_stiffness_control_negative_constrained_kappa(),
    }[function_name]()

plotter = PlotParams()

def panel_a(ax,constraint,file_names,model_type,method,panel_label,plotter=plotter):
    results1 = compute_data(plotter,file_names,model_type,method,equil="equil",constrained_kappa=constraint)
    results2 = compute_data(plotter,file_names,model_type,method,equil="stiffness_control",constrained_kappa=constraint)

    plt.subplot(ax).plot(results1[0],results1[3],"-v",label="State (S.I)",#label=r"$\mathcal{W}_{t_f}$",
                                    markersize=10,linewidth=plotter.lw,color=plotter.c1)

    plt.subplot(ax).plot(results2[0],results2[3],"-o",label="Control (S.II)",#,label=r"$\mathcal{W}_{t_f}$",
                                    markersize=10,linewidth=plotter.lw,color=plotter.c2)

    plot_w2(ax,choose_w2("equil",constraint),plotter.c1,"S.I",np.max(results1[0]))
    plot_w2(ax,choose_w2("stiffness_control",constraint),plotter.c2,"S.II",np.max(results1[0]))

    plotter.format_ax_plain(plt.subplot(ax))
    #plt.subplot(ax).plot(results1[0],np.zeros(len(results1[0])),"--",linewidth=plotter.lw,color="gray",zorder=0,alpha=0.5)
    plt.subplot(ax).set_xticks([3,4,5,6,7,8,9,10])

    plt.subplot(ax).set_ylim((0.0,0.165))
    plt.subplot(ax).set_yticks([0,0.02,0.04,0.06,0.08,0.1,0.12,0.14,0.16])
    #plt.subplot(ax).set_yticks([-0.3,-0.2,-0.1,0.0,0.1,0.2,0.3,0.4])
    plt.subplot(ax).set_ylabel(r"$\mathcal{E}_{t_f}$",fontsize=plotter.fontsizetitles)

    plt.subplot(ax).text(x=0.02,y=0.95,s=f"{panel_label}",fontsize=plotter.fontsizetitles,fontweight="bold",transform=plt.subplot(ax).transAxes)
    

def make_plot(file_names,model_type,method,file_out,plotter=plotter):
    
    # Plotting the cumulants
    fig = plotter.make_fig()
    gs = plotter.make_gridspec(fig)

    #get parameter label from filename
    param_label = None #plotter.make_paramlabel(file_names[-1])
    for ax,constraint,label in zip([gs[:,:3],gs[:,3:]],["constrained_kappa","negative_constrained_kappa"],["(a)","(b)"]):

        panel_a(ax,constraint,file_names,model_type,method,label)
    
    h,l = plt.subplot(gs[:,:3]).get_legend_handles_labels()

    plt.subplot(gs[:,:3]).legend(h,l,
                                fontsize = plotter.fontsizetitles,
                                frameon=False,
                                handlelength=1,
                                loc="upper right")
    plt.figtext(0.5, 0.01, param_label, ha="center", fontsize=plotter.fontsizetitles, bbox={"facecolor":"orange", "alpha":0.5, "pad":5})
    plt.savefig(file_out,bbox_inches="tight")

    plt.close()

def fig3():

    #input file
    file_names = [#"T2-0_Lambda3-0_eps1_g0-1.csv",
                  "T3-0_Lambda3-0_eps1_g0-1.csv",
                  "T4-0_Lambda3-0_eps1_g0-1.csv",
                  "T5-0_Lambda3-0_eps1_g0-1.csv",
                  "T6-0_Lambda3-0_eps1_g0-1.csv",
                  "T7-0_Lambda3-0_eps1_g0-1.csv",
                  "T8-0_Lambda3-0_eps1_g0-1.csv",
                  "T9-0_Lambda3-0_eps1_g0-1.csv",                  
                  "T10-0_Lambda3-0_eps1_g0-1.csv",               
                  "T12-0_Lambda3-0_eps1_g0-1.csv",               
                  "T13-0_Lambda3-0_eps1_g0-1.csv",               
                  "T14-0_Lambda3-0_eps1_g0-1.csv",               
                  "T15-0_Lambda3-0_eps1_g0-1.csv",               
                  "T20-0_Lambda3-0_eps1_g0-1.csv",               
                  "T30-0_Lambda3-0_eps1_g0-1.csv",               
                  #"T40-0_Lambda3-0_eps1_g0-1.csv",               
                  #"T2-0_Lambda3-0_eps1_g0-1.csv",
                  "T3-0_Lambda9-0_eps1_g0-1.csv",
                  "T4-0_Lambda9-0_eps1_g0-1.csv",
                  "T5-0_Lambda9-0_eps1_g0-1.csv",
                  "T6-0_Lambda9-0_eps1_g0-1.csv",
                  "T7-0_Lambda9-0_eps1_g0-1.csv",
                  "T8-0_Lambda9-0_eps1_g0-1.csv",
                  "T9-0_Lambda9-0_eps1_g0-1.csv",                  
                  "T10-0_Lambda9-0_eps1_g0-1.csv",               
                  "T12-0_Lambda9-0_eps1_g0-1.csv",               
                  "T13-0_Lambda9-0_eps1_g0-1.csv",               
                  "T14-0_Lambda9-0_eps1_g0-1.csv",               
                  "T15-0_Lambda9-0_eps1_g0-1.csv",               
                  "T20-0_Lambda9-0_eps1_g0-1.csv",               
                  "T30-0_Lambda9-0_eps1_g0-1.csv",               
                  "T40-0_Lambda9-0_eps1_g0-1.csv",               
                  ]
    
    #list what methods to try to plot. all those where the available parameters
    #  exist 
    #will be plotted, otherwise the entry will be skipped.
    model_type = "hard"#["harmonic","control","log","hard"] 
    method = "direct"#,"nondegenerate"]
    make_plot(file_names,model_type,method,f"plots/fig3.png")
    
if __name__=="__main__":
    fig3()        
