import numpy as np
import math

import pandas as pd
import matplotlib.pyplot as plt

from plotscript import *

import pdb

def append_costs(plotter,file_name,model_type,method,equil,work_vec,ep_vec):
    Lambda = plotter.get_Lambda(file_name)
    g = plotter.get_g(file_name)
    df = plotter.get_data(model_type,method,equil,file_name)
    ep = np.trapz(plotter.compute_entropy_production(df,Lambda,g,model_type),df.t.to_numpy())
    work_vec = np.append(work_vec,ep)
    ep_vec = np.append(ep_vec,plotter.get_work_from_ep(df,ep))
    return work_vec,ep_vec

def append_Tf(plotter,file_name,T_vec):

    return np.append(T_vec,plotter.get_T(file_name))

def make_plot(file_names,model_type,method,equil,file_out):

    plotter = PlotParams()
    # Plotting the cumulants
    fig = plt.figure(figsize=(15, 8))#, constrained_layout=True)
    ax1 = fig.add_axes(rect = (0.1,0.1,0.8,0.8))
    T_vec = np.empty(0)
    work_vec = np.empty(0)
    ep_vec = np.empty(0) 
    
    #pdb.set_trace()
    
    for file_name in file_names:
        try:
            work_vec, ep_vec = append_costs(plotter,file_name,model_type,method,equil,work_vec,ep_vec)
            T_vec = append_Tf(plotter,file_name,T_vec)

        except FileNotFoundError:
            pass

    #get parameter label from filename
    param_label = plotter.make_paramlabel(file_names[-1])
    #print(T_vec)
    #print(work_vec)
    ax1.plot(T_vec,work_vec,label="Work")
    ax1.plot(T_vec,ep_vec,label="Entropy Production")
  
    # Adjust layout to prevent overlap
    plotter.format_ax(ax1,"Cost",np.max(T_vec))
    ax1.set_xlim(left=T_vec[0]-0.01)
    ax1.legend(fontsize = plotter.fontsizetitles)
    plt.figtext(0.5, 0.01, param_label, ha="center", fontsize=plotter.fontsizetitles, bbox={"facecolor":"orange", "alpha":0.5, "pad":5})
    plt.savefig(file_out,bbox_inches="tight")

    plt.close()

if __name__=="__main__":
        
    #input file
    file_names = ["T2-0_Lambda3-0_eps1_g0-01.csv",
                  "T3-0_Lambda3-0_eps1_g0-01.csv",
                  "T4-0_Lambda3-0_eps1_g0-01.csv",
                  "T5-0_Lambda3-0_eps1_g0-01.csv"]
    
    #list what methods to try to plot. all those where the available parameters
    #  exist 
    #will be plotted, otherwise the entry will be skipped.
    model_type = "hard"#["harmonic","control","log","hard"] 
    method = "direct"
    make_plot(file_names,model_type,method,True,f"equil_cost_{model_type}_{method}.png")
    make_plot(file_names,model_type,method,False,f"noneq_cost_{model_type}_{method}.png")
    