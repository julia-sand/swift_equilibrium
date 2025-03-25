import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from plotscript import get_data,plot_func,param_label

#input file
file_name = "T3-0_Lambda2-0_eps1-0_g0-01.csv"
#output file
file_out = "swift_equilibrium/running_cost1.png"

#get parameter label from filename
param_label = make_paramlabel(file_name)

models = ["log", "harmonic", "hard", "control"] 
methods = ["indirect", "direct"]

# Plotting the cumulants
fig = plt.figure(figsize=(15, 8))#, constrained_layout=True)
ax1 = fig.add_axes(rect = (0.1,0.1,0.8,0.8))

for model_type in models:
    for method in methods:
        try:
            '''#get the right folder 
            if model_type=="hard":
                folder_path ="swift_equilibrium/results/hard/"
            elif model_type =="log":
                folder_path ="swift_equilibrium/results/log/"
            elif model_type =="harmonic":
                folder_path ="swift_equilibrium/results/harmonic/"
            elif model_type =="control":
                folder_path ="swift_equilibrium/results/control/"
            else:
                pass

            if method =="direct":
                df = pd.DataFrame(pd.read_csv(folder_path + "direct/"+file_name))
            else: 
                df = pd.DataFrame(pd.read_csv(folder_path + "indirect/"+file_name))
                #change headers
                #df = df.rename(columns={"timestamp": "t",
                #                        "value1": "x1",
                #                        "value2": "x2",
                #                        "value3": "x3",
                #                        "value4": "kappa",
                #                        "value5": "y1",
                #                        "value6": "y2",
                #                        "value7": "y3",
                #                        "value8": "y4"})
            '''

            df = get_data(model_type,method,equil=True)
            
            def V(y,posvar):
                lambda_vec = np.gradient(y,times_vec) if method=="direct" else b(df.y4.to_numpy())
                if model_type=="harmonic":
                    return (lambda_vec/Lambda)**2
                elif model_type=="hard":
                    return 0
                elif model_type=="log":
                    return np.where(np.abs(lambda_vec)<Lambda, -np.log(1-(lambda_vec/Lambda)**2),1e10)
                elif model_type=="control":
                    return y*(y*posvar-1) 
                else:
                    return 

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
