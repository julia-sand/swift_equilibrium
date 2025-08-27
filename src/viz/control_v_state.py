import os

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from plotscript import *
from cost_v_time import append_Tf, compute_data


def w2_dist_equil_constrained_kappa_lambda1():
    """estimate_w2.py
    compute_w2(20000,ex1())
    """

    return 0,0
    
    #0.27497567812511065
    #0.27043526719524696

def w2_dist_equil_constrained_kappa_lambda10():
    """estimate_w2.py
    compute_w2(20000,ex1a())
    """

    return 0.2666750978904591,0.2156160217610507
    #0.27609550015160056

def w2_dist_stiffness_control_constrained_kappa():
    """estimate_w2.py
    compute_w2(20000,ex2())
    """
    
    return 0,0
    #0.27868650834397246
    #0.28075074424154

def w2_dist_equil_negative_constrained_kappa():
    """estimate_w2.py
    compute_w2(20000,ex3())
    """
    
    return 0.2757935786361591
    #0.2654354307708025

def w2_dist_equil_negative_constrained_kappa_small_lambda1():
    """estimate_w2.py
    compute_w2(20000,**())
    returns: 
        w2 (state), w2 (configuration)
    """
    
    return 0.27273010958133515, 0.22192763442459496
    #0.25493365343063396

def w2_dist_equil_negative_constrained_kappa_small_lambda10():
    """estimate_w2.py
    compute_w2(20000,**())
    """
    
    return 0.27449983054736726,0.22277244235018087
    #0.2738703038801249

def w2_dist_stiffness_control_negative_constrained_kappa():
    """estimate_w2.py
    compute_w2(20000,ex4())
    """
    
    return 0.2677920569772281

def w2_dist_stiffness_control_negative_constrained_kappa_small():
    """estimate_w2.py
    compute_w2(20000,ex5())
    """
    
    return 0.2644955232145077,0.21335551558235102
    #0.2678660709004442

def plot_w2(ax,w2,color1,case,tf):
        
    w2_state = w2[1]
    w2_conf = w2[0]

    plt.subplot(ax).plot(np.linspace(3,tf,num=20),
                        w2_conf/np.linspace(3,tf,num=20),
                        linestyle="--",
                        label=r"$\frac{1}{t_f}\mathcal{W}_2$"+"("+"Config."+")")
    plt.subplot(ax).fill_between(np.linspace(3,tf,num=20),
                        (w2_conf-(20000**-0.5))/np.linspace(3,tf,num=20),
                        (w2_conf+(20000**-0.5))/np.linspace(3,tf,num=20)
                        ,color=color1,alpha=0.5)
    plt.subplot(ax).plot(np.linspace(3,tf,num=20),
                        w2_state/np.linspace(3,tf,num=20),
                        linestyle="dotted",
                        label=r"$\frac{1}{t_f}\mathcal{W}_2$"+"("+"State"+")")
    plt.subplot(ax).fill_between(np.linspace(3,tf,num=20),
                        (w2_state-(20000**-0.5))/np.linspace(3,tf,num=20),
                        (w2_state+(20000**-0.5))/np.linspace(3,tf,num=20)
                        ,color=color1,alpha=0.5)

def choose_w2(equilvar,constraint,lambda_val):
    function_name = "w2_dist_"+equilvar+"_"+constraint+"_"+lambda_val
    return {
        'w2_dist_equil_constrained_kappa_lambda1': lambda: w2_dist_equil_constrained_kappa_lambda1(),
        'w2_dist_equil_constrained_kappa_lambda10': lambda: w2_dist_equil_constrained_kappa_lambda10(),
        'w2_dist_equil_negative_constrained_kappa': lambda: w2_dist_equil_negative_constrained_kappa(),
        'w2_dist_equil_negative_constrained_kappa_small_lambda1': lambda: w2_dist_equil_negative_constrained_kappa_small_lambda1(),
        'w2_dist_equil_negative_constrained_kappa_small_lambda10': lambda: w2_dist_equil_negative_constrained_kappa_small_lambda10(),
        'w2_dist_stiffness_control_constrained_kappa_': lambda: w2_dist_stiffness_control_constrained_kappa(),
        'w2_dist_stiffness_control_negative_constrained_kappa_': lambda: w2_dist_stiffness_control_negative_constrained_kappa(),
        'w2_dist_stiffness_control_negative_constrained_kappa_small_': lambda: w2_dist_stiffness_control_negative_constrained_kappa_small(),
    }[function_name]()

plotter = PlotParams()

def panel_a(ax,constraint,file_names,model_type,method,panel_label,plotter=plotter):
    results1 = compute_data(plotter,file_names,model_type,method,equil="equil",constrained_kappa=constraint)
    results2 = compute_data(plotter,file_names,model_type,method,equil="stiffness_control",constrained_kappa=constraint)

    plt.subplot(ax).plot(results1[0],results1[3],"-v",label="State (S.I)",#label=r"$\mathcal{W}_{t_f}$",
                                    markersize=10,linewidth=plotter.lw,color=plotter.c1)

    plt.subplot(ax).plot(results2[0],results2[3],"-o",label="Control (S.II)",#,label=r"$\mathcal{W}_{t_f}$",
                                    markersize=10,linewidth=plotter.lw,color=plotter.c2)

    plot_w2(ax,choose_w2("equil",constraint,f"lambda{str(int(plotter.get_Lambda(file_names[0])))}"),plotter.c1,"S.I",np.max(results1[0]))
    #plot_w2(ax,choose_w2("stiffness_control",constraint,""),plotter.c2,"S.II",np.max(results1[0]))

    plotter.format_ax_plain(plt.subplot(ax))
    #plt.subplot(ax).plot(results1[0],np.zeros(len(results1[0])),"--",linewidth=plotter.lw,color="gray",zorder=0,alpha=0.5)
    plt.subplot(ax).set_xticks([3,4,5,6,7,8,9,10])

    plt.subplot(ax).set_ylim((-0.01,0.238))
    plt.subplot(ax).set_xlim((2.8,10.2))
    plt.subplot(ax).set_yticks([0,0.04,0.08,0.12,0.16,0.2])
    #plt.subplot(ax).set_yticks([-0.3,-0.2,-0.1,0.0,0.1,0.2,0.3,0.4])
    plt.subplot(ax).set_ylabel(r"$\mathcal{E}_{t_f}$",fontsize=plotter.fontsizetitles)

    plt.subplot(ax).text(x=0.01,y=0.9,s=f"{panel_label}",fontsize=plotter.fontsizetitles,fontweight="bold",
                transform=plt.subplot(ax).transAxes)
    

def make_plot(model_type,method,file_out,plotter=plotter):
    
    #input file
    lambda_1 = ["T3-0_Lambda1-0_eps1_g0-1.csv",
                  "T4-0_Lambda1-0_eps1_g0-1.csv",
                  "T5-0_Lambda1-0_eps1_g0-1.csv",
                  "T6-0_Lambda1-0_eps1_g0-1.csv",
                  "T7-0_Lambda1-0_eps1_g0-1.csv",
                  "T8-0_Lambda1-0_eps1_g0-1.csv",
                  "T9-0_Lambda1-0_eps1_g0-1.csv",                  
                  "T10-0_Lambda1-0_eps1_g0-1.csv",               
                  "T12-0_Lambda1-0_eps1_g0-1.csv",               
                  "T13-0_Lambda1-0_eps1_g0-1.csv",               
                  "T14-0_Lambda1-0_eps1_g0-1.csv",               
                  "T15-0_Lambda1-0_eps1_g0-1.csv",               
                  "T20-0_Lambda1-0_eps1_g0-1.csv",               
                  "T30-0_Lambda1-0_eps1_g0-1.csv"]
    lambda_10 = ["T3-0_Lambda10-0_eps1_g0-1.csv",
                  "T4-0_Lambda10-0_eps1_g0-1.csv",
                  "T5-0_Lambda10-0_eps1_g0-1.csv",
                  "T6-0_Lambda10-0_eps1_g0-1.csv",
                  "T7-0_Lambda10-0_eps1_g0-1.csv",
                  "T8-0_Lambda10-0_eps1_g0-1.csv",
                  "T9-0_Lambda10-0_eps1_g0-1.csv",                  
                  "T10-0_Lambda10-0_eps1_g0-1.csv",               
                  "T12-0_Lambda10-0_eps1_g0-1.csv",               
                  "T13-0_Lambda10-0_eps1_g0-1.csv",               
                  "T14-0_Lambda10-0_eps1_g0-1.csv",               
                  "T15-0_Lambda10-0_eps1_g0-1.csv",               
                  "T20-0_Lambda10-0_eps1_g0-1.csv",               
                  "T30-0_Lambda10-0_eps1_g0-1.csv",               
                  "T40-0_Lambda10-0_eps1_g0-1.csv"]
    # Plotting the cumulants
    fig = plotter.make_fig()
    gs = plotter.make_gridspec(fig)

    #get parameter label from filename
    param_label = None #plotter.make_paramlabel(file_names[-1])

    panel_a(gs[0,:3],"constrained_kappa",lambda_1,model_type,method,"(a)")
    panel_a(gs[0,3:],"constrained_kappa",lambda_10,model_type,method,"(b)")

    panel_a(gs[1,:3],"negative_constrained_kappa_small",lambda_1,model_type,method,"(c)")
    panel_a(gs[1,3:],"negative_constrained_kappa_small",lambda_10,model_type,method,"(d)")

    h,l = plt.subplot(gs[0,:3]).get_legend_handles_labels()

    plt.subplot(gs[0,3:]).legend(h,l,
                                fontsize = plotter.fontsizetitles-4,
                                frameon=False,
                                handlelength=1,
                                ncols=2,
                                loc="upper right")
    #plt.tight_layout()
    plt.figtext(0.5, 0.01, param_label, ha="center", fontsize=plotter.fontsizetitles, bbox={"facecolor":"orange", "alpha":0.5, "pad":5})
    plt.savefig(file_out,bbox_inches="tight")

    plt.close()

def fig4():

    
    #list what methods to try to plot. all those where the available parameters
    #  exist 
    #will be plotted, otherwise the entry will be skipped.
    model_type = "hard"#["harmonic","control","log","hard"] 
    method = "direct"#,"nondegenerate"]
    make_plot(model_type,method,f"plots/fig4.png")
    make_plot(model_type,method,f"plots/fig4.pdf")
    
if __name__=="__main__":
    fig4()        
