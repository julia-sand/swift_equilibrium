import numpy as np
import math

import pandas as pd
import matplotlib.pyplot as plt

from plotscript import *

import pdb

def append_costs(plotter,file_name,model_type,method,equil,work_vec,heat_vec,ep_vec):
    Lambda = plotter.get_Lambda(file_name)
    g = plotter.get_g(file_name)
    df = plotter.get_data(model_type,method,equil,file_name)
    
    ep_vec = np.append(ep_vec,plotter.compute_entropy_production(df,Lambda,g,model_type))
    work_vec = np.append(work_vec,plotter.compute_work(df,Lambda,g,model_type))
    heat_vec = np.append(heat_vec,plotter.compute_heat(df,Lambda,g,model_type))
    
    return work_vec,heat_vec,ep_vec

def append_Tf(plotter,file_name,T_vec):

    return np.append(T_vec,plotter.get_T(file_name))

def compute_data(plotter,file_names,model_type,method,equil,file_out):
    T_vec = np.empty(0)
    work_vec = np.empty(0)
    ep_vec = np.empty(0) 
    heat_vec = np.empty(0) 
    
    #pdb.set_trace()
    
    for file_name in file_names:
        try:
            work_vec,heat_vec,ep_vec = append_costs(plotter,file_name,model_type,method,equil,work_vec,heat_vec,ep_vec)
            T_vec = append_Tf(plotter,file_name,T_vec)

        except (FileNotFoundError,ValueError):
            pass
    
    return T_vec,work_vec,heat_vec,ep_vec
    

def make_plot(file_names,model_type,method,file_out):

    plotter = PlotParams()
    # Plotting the cumulants
    fig = plotter.make_fig()
    gs = plotter.make_gridspec(fig)

    #get parameter label from filename
    param_label = None #plotter.make_paramlabel(file_names[-1])
    
    T_vec_equil,work_vec_equil,heat_vec_equil,ep_vec_equil = compute_data(plotter,file_names,model_type,method,equil=True,file_out=file_out)
    T_vec_noneq,work_vec_noneq,heat_vec_noneq,ep_vec_noneq = compute_data(plotter,file_names,model_type,method,equil=False,file_out=file_out)
    plt.subplot(gs[:,:3]).plot(T_vec_equil,work_vec_equil,"-v",label=r"$\mathcal{W}_{t_f}$",markersize=10,linewidth=plotter.lw,color=plotter.c1)
    plt.subplot(gs[:,:3]).plot(T_vec_equil,heat_vec_equil,"-x",label=r"$\mathcal{Q}_{t_f}$",markersize=10,linewidth=plotter.lw-1,color=plotter.c2,zorder=100)
    plt.subplot(gs[:,:3]).plot(T_vec_equil,ep_vec_equil,"-o",label=r"$\mathcal{E}_{t_f}$",markersize=10,linewidth=plotter.lw,color=plotter.c3,zorder=200)
    plt.subplot(gs[:,3:]).plot(T_vec_noneq,work_vec_noneq,"-v",markersize=10,linewidth=plotter.lw,color=plotter.c1)
    plt.subplot(gs[:,3:]).plot(T_vec_noneq,heat_vec_noneq,"-x",markersize=10,linewidth=plotter.lw,color=plotter.c2,zorder=100)
    plt.subplot(gs[:,3:]).plot(T_vec_noneq,ep_vec_noneq,"-o",markersize=10,linewidth=plotter.lw,color=plotter.c3,zorder=200)

    plt.subplot(gs[:,:3]).plot(T_vec_noneq,np.zeros(len(T_vec_noneq)),"--",linewidth=plotter.lw,color="gray",zorder=0,alpha=0.5)
    plt.subplot(gs[:,3:]).plot(T_vec_noneq,np.zeros(len(T_vec_noneq)),"--",linewidth=plotter.lw,color="gray",zorder=0,alpha=0.5)


    plt.subplot(gs[:,:3]).set_title("Engineered Swift Equilibration",fontsize=plotter.fontsizetitles)
    plt.subplot(gs[:,3:]).set_title("Minimum Work Transition",fontsize=plotter.fontsizetitles)

    plotter.format_ax(plt.subplot(gs[:,:3]),"Cost",np.maximum(np.max(T_vec_equil),np.max(T_vec_equil)))
    plotter.format_ax(plt.subplot(gs[:,3:]),"Cost",np.maximum(np.max(T_vec_equil),np.max(T_vec_equil)))
    plt.subplot(gs[:,:3]).set_xlim(left=np.minimum(np.min(T_vec_equil),np.min(T_vec_equil))-0.1,right=np.maximum(np.max(T_vec_equil),np.max(T_vec_equil))+0.1)
    plt.subplot(gs[:,3:]).set_xlim(left=np.minimum(np.min(T_vec_equil),np.min(T_vec_equil))-0.1,right=np.maximum(np.max(T_vec_equil),np.max(T_vec_equil))+0.1)
    plt.subplot(gs[:,:3]).set_ylim((-0.8,0.25))
    plt.subplot(gs[:,3:]).set_ylim((-0.8,0.25))
    plt.subplot(gs[:,3:]).text(x=0.02,y=0.95,s="(b)",fontsize=plotter.fontsizetitles,fontweight="bold",transform=plt.subplot(gs[:,3:]).transAxes)
    plt.subplot(gs[:,:3]).text(x=0.02,y=0.95,s="(a)",fontsize=plotter.fontsizetitles,fontweight="bold",transform=plt.subplot(gs[:,:3]).transAxes)
    
    fig.legend(fontsize = plotter.fontsizetitles,
                                frameon=False,
                                handlelength=1,
                                loc="center right")
    plt.figtext(0.5, 0.01, param_label, ha="center", fontsize=plotter.fontsizetitles, bbox={"facecolor":"orange", "alpha":0.5, "pad":5})
    plt.savefig(file_out,bbox_inches="tight")

    plt.close()

if __name__=="__main__":
        
    #input file
    file_names = ["T2-0_Lambda1-4_eps1_g0-01.csv",
                  "T3-0_Lambda1-4_eps1_g0-01.csv",
                  "T4-0_Lambda1-4_eps1_g0-01.csv",
                  "T5-0_Lambda1-4_eps1_g0-01.csv",
                  "T6-0_Lambda1-4_eps1_g0-01.csv",
                  "T7-0_Lambda1-4_eps1_g0-01.csv",
                  "T8-0_Lambda1-4_eps1_g0-01.csv",
                  "T9-0_Lambda1-4_eps1_g0-01.csv",
                  "T10-0_Lambda1-4_eps1_g0-01.csv",
                  "T20-0_Lambda1-4_eps1_g0-01.csv",
                  "T30-0_Lambda1-4_eps1_g0-01.csv",
                  "T40-0_Lambda1-4_eps1_g0-01.csv",
                  "T50-0_Lambda1-4_eps1_g0-01.csv"]
    
    #list what methods to try to plot. all those where the available parameters
    #  exist 
    #will be plotted, otherwise the entry will be skipped.
    model_type = "harmonic"#["harmonic","control","log","hard"] 
    method = "indirect"
    make_plot(file_names,model_type,method,f"plots/cost_{model_type}_{method}.png")
    make_plot(file_names,model_type,method,f"plots/cost_{model_type}_{method}.pdf")

    #make_plot(file_names,model_type,method,False,f"noneq_cost_{model_type}_{method}.png")
    
