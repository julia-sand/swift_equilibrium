import os

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from plotscript import *
from cost_v_time import append_Tf, set_g, compute_data

plotter = PlotParams()

def panel_a(ax,constraint,file_out,panel_label,plotter=plotter):
    results1 = compute_data(plotter,file_names,model_type,method,equil="equil",file_out=file_out,constrained_kappa=constraint)
    results2 = compute_data(plotter,file_names,model_type,method,equil="stiffness_control",file_out=file_out,constrained_kappa=constraint)
    print(np.max(results1[3]))
    plt.subplot(ax).plot(results1[0],results1[3],"-v",label="State (S.I)",#label=r"$\mathcal{W}_{t_f}$",
                                    markersize=10,linewidth=plotter.lw,color=plotter.c1)

    plt.subplot(ax).plot(results2[0],results2[3],"-o",label="Control (S.II)",#,label=r"$\mathcal{W}_{t_f}$",
                                    markersize=10,linewidth=plotter.lw,color=plotter.c2)

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
        panel_a(ax,constraint,file_out,label)
    
    #plot w2 distance
    plt.subplot(gs[:,:3]).plot(np.linspace(3,10,num=8),plotter.get_w2_dist()*np.ones(8)/np.linspace(3,10,num=8),
                    linestyle="dashed",color=plotter.c3,alpha=0.5,lw=plotter.lw, label=r"$\frac{1}{t_f}\mathcal{W}_2$ (S.I)")
    plt.subplot(gs[:,:3]).plot(np.linspace(3,10,num=8),plotter.get_w2_dist_stiffness_control()*np.ones(8)/np.linspace(3,10,num=8),
                    linestyle="dashed",color="pink",alpha=0.8,lw=plotter.lw, label=r"$\frac{1}{t_f}\mathcal{W}_2$ (S.II)")
        
    h,l = plt.subplot(gs[:,:3]).get_legend_handles_labels()

    plt.subplot(gs[:,:3]).legend(h,l,
                                fontsize = plotter.fontsizetitles,
                                frameon=False,
                                handlelength=1,
                                loc="upper right")
    plt.figtext(0.5, 0.01, param_label, ha="center", fontsize=plotter.fontsizetitles, bbox={"facecolor":"orange", "alpha":0.5, "pad":5})
    plt.savefig(file_out,bbox_inches="tight")

    plt.close()

if __name__=="__main__":
        
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
                  #"T12-0_Lambda3-0_eps1_g0-1.csv",               
                  #"T13-0_Lambda3-0_eps1_g0-1.csv",               
                  #"T14-0_Lambda3-0_eps1_g0-1.csv",               
                  #"T15-0_Lambda3-0_eps1_g0-1.csv",               
                  #"T20-0_Lambda3-0_eps1_g0-1.csv",               
                  #"T30-0_Lambda3-0_eps1_g0-1.csv",               
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
                  #"T12-0_Lambda9-0_eps1_g0-1.csv",               
                  #"T13-0_Lambda9-0_eps1_g0-1.csv",               
                  #"T14-0_Lambda9-0_eps1_g0-1.csv",               
                  #"T15-0_Lambda9-0_eps1_g0-1.csv",               
                  #"T20-0_Lambda9-0_eps1_g0-1.csv",               
                  #"T30-0_Lambda9-0_eps1_g0-1.csv",               
                  #"T40-0_Lambda9-0_eps1_g0-1.csv",               
                  ]
    
    #list what methods to try to plot. all those where the available parameters
    #  exist 
    #will be plotted, otherwise the entry will be skipped.
    model_type = "hard"#["harmonic","control","log","hard"] 
    method = "direct"#,"nondegenerate"]
    make_plot(file_names,model_type,method,f"plots/neg_kappa_state_v_control_cost_{model_type}_{method}.png")
    #make_plot(file_names,model_type,method,f"plots/neg_kappa_state_v_control_cost_{model_type}_{method}.pdf")
    
