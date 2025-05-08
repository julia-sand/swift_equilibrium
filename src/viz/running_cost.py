import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from plotscript import PlotParams


def running_cost_plot(file_name,file_out,models,methods):
    plotter = PlotParams()
    
    #get parameter label from filename
    param_label = make_paramlabel(file_name)

    # Plotting the cumulants
    fig = plt.figure(figsize=(15, 8))#, constrained_layout=True)
    ax1 = fig.add_axes(rect = (0.1,0.1,0.8,0.8))

    for model_type in models:
        for method in methods:
            try:
            
                df = get_data(model_type,method,equil=True)
                

                #change to have same timestep in each
                idx_step = df.index[df['t']==0.05]
                df = df.iloc[::idx_step[0], :]

                #compute costs
                times_vec = df.t.to_numpy()
                cost_fun = df.x3.to_numpy()+g*V(df.kappa.to_numpy(),df.x1.to_numpy())
                plot_func(ax1,
                            times_vec,times_vec[1]*np.cumsum(cost_fun),
                            "Running Cost",
                            f"{method}:{model_type}")
            except:
                pass


    # Adjust layout to prevent overlap
    ax1.legend(fontsize = fontsize)
    plt.figtext(0.5, 0.01, param_label, ha="center", fontsize=fontsizetitles, bbox={"facecolor":"orange", "alpha":0.5, "pad":5})
    plt.savefig(file_out,bbox_inches="tight")

    plt.close()


if __name__=="__main__":
        
    #input file
    file_name = "T3-0_Lambda2-0_eps1-0_g0-01.csv"
    #output file
    file_out = "swift_equilibrium/running_cost1.png"


    models = ["log", "harmonic", "hard", "control"] 
    methods = ["indirect", "direct"]
