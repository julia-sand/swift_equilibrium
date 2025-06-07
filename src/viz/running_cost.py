import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from plotscript import PlotParams


def running_cost_plot(file_name,file_out,models,methods):
    plotter = PlotParams()
    
    #get parameter label from filename
    param_label = plotter.make_paramlabel(file_name)

    # Plotting the cumulants
    fig = plt.figure(figsize=(15, 8))#, constrained_layout=True)
    ax1 = fig.add_axes(rect = (0.1,0.1,0.8,0.8))

    for model_type in models:
        for method in methods:
            try:
            
                df = plotter.get_data(model_type,method,equil=True,file_name=file_name)
                
                g = plotter.get_g(file_name)
                Lambda = plotter.get_Lambda(file_name)
                
                #TODO fix this!!!
                # change to have same timestep in each
                #idx_step = df.index[df['t']==0.05]
                #print(idx_step)
                #df = df.iloc[::idx_step[0], :]

                #compute costs
                times_vec = df.t.to_numpy()
                cost_fun = df.x3.to_numpy()+g*plotter.get_Vfun(df,
                                                                        Lambda,g,
                                                                        model_type)
                plotter.plot_func(ax1,
                            times_vec,times_vec[1]*np.cumsum(cost_fun),
                            "Running Cost",
                            f"{method}:{model_type}")
            except FileNotFoundError:
                pass


    # Adjust layout to prevent overlap
    ax1.legend(fontsize = plotter.fontsizetitles)
    plt.figtext(0.5, 0.01, param_label, ha="center", fontsize=plotter.fontsizetitles, bbox={"facecolor":"orange", "alpha":0.5, "pad":5})
    plt.savefig(file_out,bbox_inches="tight")

    plt.close()


if __name__=="__main__":
        
    #input file
    file_names = ["T3-0_Lambda1-0_eps1-0_g0-01.csv",
                   "T3-0_Lambda3-0_eps1-0_g0-1.csv",
                   "T3-0_Lambda1-4_eps1-0_g0-1.csv",
                   "T3-0_Lambda1-4_eps1-0_g0-01.csv",
                   "T3-0_Lambda1-4_eps1-0_g0-001.csv",
                   "T3-0_Lambda3-0_eps1-0_g0-0001.csv",
                   "T3-0_Lambda5-0_eps1-0_g0-0001.csv",
                   "T5-0_Lambda1-4_eps1-0_g0-5.csv" ]
    
    #list what methods to try to plot. all those where the available parameters
    #  exist 
    #will be plotted, otherwise the entry will be skipped.
    models = ["harmonic","control","log","hard"] 
    methods = ["indirect","direct"]#["slowfast",
    equil = True  

    for file_name in enumerate(file_names):
        print(file_name)
        running_cost_plot(file_name[1],f"runningcost{file_name[0]}.png",models,methods)