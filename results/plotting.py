import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import pandas as pd
import string


#file name. This is the file that will 
#be plotted if available. 
file_name = "T3-0_Lambda1-0_eps1-0_g0-01.csv"
file_out = "swift_equilibrium/compact_log1.png"

#list what methods to try to plot. all those where the results exist 
#will be plotted, otherwise skipped.
models = ["hard", "log"] 
methods = ["indirect","direct"]


#read params from filename? 
params = file_name.rsplit(".",1)[0].split('_') #removes .csv from end
tval = params[0].replace('-', '.')
lambdaval = params[1].replace('-', '.')
epsval = params[2].replace('-', '.')
gval = params[-1].replace('-', '.')

def get_idx(string):
    for i in enumerate(string):
        if str.isdigit(i[1]):
            return i[0] 
    
T = float(tval[get_idx(tval):])
Lambda = float(lambdaval[get_idx(lambdaval):])
epsilon = float(epsval[get_idx(epsval):])
g = float(gval[get_idx(gval):])
param_label = rf"$T={T}; \Lambda={Lambda}; \varepsilon={epsilon}; g={g}$"


#set up fontsizes
fontsize = 20
fontsizeticks = 16
fontsizetitles = 20

# figure setup
fig = plt.figure(figsize=(15, 8))#, constrained_layout=True)
gs_cumulants = gridspec.GridSpec(2, 6, 
                    width_ratios=[1, 1, 1, 1,1,1], 
                    height_ratios=[1, 1],
                    hspace=0.4,
                    wspace=1.2)

pos_var_plot = plt.subplot(gs_cumulants[0, 2:4])
xcorr_plot = plt.subplot(gs_cumulants[0, 4:])
kappa_plot = plt.subplot(gs_cumulants[1,:3])
lambda_plot = plt.subplot(gs_cumulants[1, 3:])
mom_var_plot = plt.subplot(gs_cumulants[0, 0:2])

for model_type in models:
    for method in methods:
    
        def plot_func(ax,x,y,ylabel,legendlabel=f"{model_type}, {method}"):
            if method =="direct":
                ax.plot(x, y, label = legendlabel,lw=3,linestyle="dashed")
            else: 
                ax.plot(x, y, label = legendlabel,lw=3)
            ax.set_ylabel(ylabel,fontsize=fontsizetitles)
            ax.set_xlabel('t',fontsize=fontsizetitles)
            ax.tick_params(labelsize=fontsizeticks)

        try:    
            #get the right folder 
            if model_type=="hard":
                folder_path ="swift_equilibrium/results/hard/"
            elif model_type =="log":
                folder_path ="swift_equilibrium/results/log/"
            elif model_type =="harmonic":
                folder_path ="swift_equilibrium/results/harmonic/"
            elif model_type =="control":
                folder_path ="swift_equilibrium/results/control/"
            #else:
            #    pass
                #print("the model type is invalid. Please specify a valid model or recompute the results if the model type is set up. Use log, harmonic, control or hard.")

            if method =="direct":
                df = pd.DataFrame(pd.read_csv(folder_path + "direct/"+file_name))
            elif method =="indirect": 
                df = pd.DataFrame(pd.read_csv(folder_path + "indirect/"+file_name))
                #change headers
                df = df.rename(columns={"timestamp": "t",
                                        "value1": "x1",
                                        "value2": "x2",
                                        "value3": "x3",
                                        "value4": "kappa",
                                        "value5": "y1",
                                        "value6": "y2",
                                        "value7": "y3",
                                        "value8": "y4"})

            # Plot on the first subplot (top-left)
            #"Position variance"
            plot_func(pos_var_plot,df.t, df.x1,'Position Variance')#,f"{method}:{model_type}")
            plot_func(xcorr_plot,df.t, df.x2,'Cross Correlation')
            plot_func(mom_var_plot,df.t, df.x3,'Mom. Variance')

            # Plot on the fourth subplot (bottom-right)
            plot_func(kappa_plot,df.t, df["kappa"],r'Stiffness, $\kappa_t$')
            plot_func(lambda_plot,df.t.to_numpy(), np.gradient(df["kappa"].to_numpy(),df.t.to_numpy())
                                ,r'Control, $\lambda_t$')  
        except: 
            pass
        
kappa_plot.legend(fontsize=fontsizeticks,loc="lower center")

plt.figtext(0.5, 0.01, param_label, ha="center", fontsize=18, bbox={"facecolor":"orange", "alpha":0.5, "pad":5})

plt.savefig(file_out, bbox_inches="tight")

plt.close()
