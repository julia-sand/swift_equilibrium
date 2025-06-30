import numpy as np
import math

import pandas as pd
import matplotlib.pyplot as plt

from plotscript import *


def running_cost_plot(file_name,file_out,models,methods,equil):
    plotter = PlotParams()
    
    #get parameter label from filename
    param_label = plotter.make_paramlabel(file_name)

    # Plotting the cumulants
    fig = plt.figure(figsize=(15, 8))#, constrained_layout=True)
    ax1 = fig.add_axes(rect = (0.1,0.1,0.8,0.8))
    Tf = 0 
    for model_type in models:
        for method in methods:
            try:
            
                df = plotter.get_data(model_type,method,equil,file_name=file_name)
                
                g = plotter.get_g(file_name)
                Lambda = plotter.get_Lambda(file_name)#math.sqrt(2)
                epsilon = 1

                #compute costs
                times_vec = df.t.to_numpy()
                Tf = times_vec[-1]
                cost_fun = df.x3.to_numpy()+g*plotter.get_Vfun(df,Lambda,g,
                                                                        model_type)
                plotter.plot_func(ax1,
                            times_vec,times_vec[1]*np.cumsum(cost_fun),
                            "")#f"{method}:{model_type}")
                plotter.plot_func(ax1,
                            times_vec,times_vec[1]*np.cumsum(cost_fun)+0.5*(df.kappa.to_numpy()[-1]*df.x1.to_numpy()[-1]-df.kappa.to_numpy()[0]*df.x1.to_numpy()[0]),
                            f"{method}:{model_type}",linestyle="dashed")
            except FileNotFoundError:
                pass


    # Adjust layout to prevent overlap
    plotter.format_ax(ax1,"Cost",Tf)
    ax1.legend(fontsize = plotter.fontsizetitles)
    plt.figtext(0.5, 0.01, param_label, ha="center", fontsize=plotter.fontsizetitles, bbox={"facecolor":"orange", "alpha":0.5, "pad":5})
    plt.savefig(file_out,bbox_inches="tight")

    plt.close()


if __name__=="__main__":
        
    #input file
    file_names = ["T2-0_Lambda3-0_eps1_g0-1.csv",
                   "T3-0_Lambda3-0_eps1_g0-01.csv",
                   "T4-0_Lambda3-0_eps1_g0-01.csv",
                   "T5-0_Lambda3-0_eps1_g0-01.csv",
                   "T6-0_Lambda3-0_eps1_g0-01.csv",
                   "T7-0_Lambda3-0_eps1_g0-01.csv",
                   "T8-0_Lambda3-0_eps1_g0-01.csv",
                   "T8-0_Lambda3-0_eps1_g0-01.csv",
                   "T10-0_Lambda3-0_eps1_g0-01.csv",
                   "T20-0_Lambda3-0_eps1_g0-01.csv",
                   "T30-0_Lambda3-0_eps1_g0-01.csv",
                   "T40-0_Lambda3-0_eps1_g0-01.csv",
                   "T50-0_Lambda3-0_eps1_g0-01.csv"]
    
    #list what methods to try to plot. all those where the available parameters
    #  exist 
    #will be plotted, otherwise the entry will be skipped.
    models = ["harmonic","control","log","hard"] 
    methods = ["indirect","direct"]#["slowfast",

    for file_name in enumerate(file_names):
        print(file_name)
        running_cost_plot(file_name[1],f"runningcost_equil{file_name[0]}.png",models,methods,True)
        running_cost_plot(file_name[1],f"runningcost_noneq{file_name[0]}.png",models,methods,False)