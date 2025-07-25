import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from plotscript import *

def set_g(file_name,model_type,equil,plotter):
    if (model_type == ["control"] and equil=="noneq"):
        g = 0 
    elif (model_type=="hard"):
        g = 0
    else:
        g = plotter.get_g(file_name)

    return plotter.get_g(file_name)

def append_Tf(plotter,file_name,T_vec):

    return np.append(T_vec,plotter.get_T(file_name))

def compute_data(plotter,file_names,model_type,method,equil,file_out,constrained_kappa):
    T_vec = np.empty(0)
    work_vec = np.empty(0)
    ep_vec = np.empty(0) 
    heat_vec = np.empty(0) 
    cost_vec = np.empty(0) 

    #pdb.set_trace()
    
    for file_name in file_names:
        try:
            df = plotter.get_data(model_type,method,equil,file_name,constrained_kappa)

            work_vec = np.append(work_vec, plotter.compute_work(df))
            heat_vec = np.append(heat_vec, plotter.compute_heat(df))
            ep_vec = np.append(ep_vec, plotter.compute_entropy_production(df))
            cost_vec = np.append(cost_vec, plotter.compute_cost(df,set_g(file_name,model_type,equil,plotter),plotter.get_Lambda(file_name),model_type))

            T_vec = append_Tf(plotter,file_name,T_vec)

        except (FileNotFoundError,ValueError):
            pass
    
    return T_vec,work_vec,heat_vec,ep_vec,cost_vec
    

def make_plot(file_names,model_type,method,file_out):

    plotter = PlotParams()
    # Plotting the cumulants
    fig = plotter.make_fig()
    gs = plotter.make_gridspec(fig)

    #get parameter label from filename
    param_label = None #plotter.make_paramlabel(file_names[-1])
    results1 = compute_data(plotter,file_names,model_type,method,equil="equil",file_out=file_out,constrained_kappa="no")
    results2 = compute_data(plotter,file_names,model_type,method,equil="noneq",file_out=file_out,constrained_kappa="no")

    for ax,results in zip([gs[:,:3],gs[:,3:]],[results1,results2]):
        plt.subplot(ax).plot(results[0],results[1],"-v",label=r"$\mathcal{W}_{t_f}$",markersize=10,linewidth=plotter.lw,color=plotter.c1)
        plt.subplot(ax).plot(results[0],results[2],"-x",label=r"$\mathcal{Q}_{t_f}$",markersize=10,linewidth=plotter.lw-1,color=plotter.c2,zorder=100)
        plt.subplot(ax).plot(results[0],results[3],"-o",label=r"$\mathcal{E}_{t_f}$",markersize=10,linewidth=plotter.lw,color=plotter.c3,zorder=200)
    
        plt.subplot(ax).plot(results[0],np.zeros(len(results[0])),"--",linewidth=plotter.lw,color="gray",zorder=0,alpha=0.5)

    plt.subplot(gs[:,:3]).set_title("Engineered Swift Equilibration",fontsize=plotter.fontsizetitles)
    plt.subplot(gs[:,3:]).set_title("Minimum Work Transition",fontsize=plotter.fontsizetitles)

    ax_inset = plt.subplot(gs[:,:3]).inset_axes(bounds=[0.1,0.1,0.4,0.3],transform=plt.subplot(gs[:,:3]).transAxes)
    
    
    
    plt.subplot(gs[:,3:]).text(x=0.02,y=0.95,s="(b)",fontsize=plotter.fontsizetitles,fontweight="bold",transform=plt.subplot(gs[:,3:]).transAxes)
    plt.subplot(gs[:,:3]).text(x=0.02,y=0.95,s="(a)",fontsize=plotter.fontsizetitles,fontweight="bold",transform=plt.subplot(gs[:,:3]).transAxes)
    
    h,l = plt.subplot(gs[:,3:]).get_legend_handles_labels()

    fig.legend(h,l,
                                fontsize = plotter.fontsizetitles,
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
                  "T30-0_Lambda1-4_eps1_g0-01.csv"]
    
    #list what methods to try to plot. all those where the available parameters
    #  exist 
    #will be plotted, otherwise the entry will be skipped.
    model_type ="harmonic"#["harmonic","control","log","hard"] 
    method = "indirect"
    make_plot(file_names,model_type,method,f"plots/new_cost_{model_type}_{method[0]}.png")
    #make_plot(file_names,model_type,method,f"plots/cost_{model_type}_{method}.pdf")

    #make_plot(file_names,model_type,method,False,f"noneq_cost_{model_type}_{method}.png")
    
