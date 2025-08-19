import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from plotscript import *

"""
Produces Fig. 5 in paper
"""

def set_g(file_name,model_type,plotter):
    if (model_type=="hard"):
        g = 0
    else:
        g = plotter.get_g(file_name)

    return g #plotter.get_g(file_name)

def append_Tf(plotter,file_name,T_vec):

    return np.append(T_vec,plotter.get_T(file_name))

def compute_data(plotter,file_names,model_type,method,equil,constrained_kappa):
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
            cost_vec = np.append(cost_vec, plotter.compute_cost(df,set_g(file_name,model_type,plotter),plotter.get_Lambda(file_name),model_type))

            T_vec = append_Tf(plotter,file_name,T_vec)

        except (FileNotFoundError,ValueError):
            pass
    
    return T_vec,work_vec,heat_vec,ep_vec,cost_vec

def plot_work(ax,tvec,workvec,plotter):
    ax.plot(tvec,workvec,"-v",label=r"$\mathcal{W}_{t_f}$",markersize=10,linewidth=plotter.lw,color=plotter.c1)
    
def plot_heat(ax,tvec,heatvec,plotter):
    ax.plot(tvec,heatvec,"-x",label=r"$\mathcal{Q}_{t_f}$",markersize=10,linewidth=plotter.lw-1,color=plotter.c2,zorder=100)
    
def plot_ep(ax,tvec,epvec,plotter):
    ax.plot(tvec,epvec,"-o",label=r"$\mathcal{E}_{t_f}$",markersize=10,linewidth=plotter.lw,color=plotter.c3,zorder=200)

def add_panel_label(ax,panel_label,plotter):
    ax.text(x=0.02,y=0.95,s=panel_label,fontsize=plotter.fontsizetitles,
    fontweight="bold",transform=ax.transAxes)

def format_plot(ax,tvec,plot_title,plotter):
    ax.plot(tvec,np.zeros(len(tvec)),"--",linewidth=plotter.lw,color="gray",zorder=0,alpha=0.5)
    
    ax.set_xlabel(r"$t_f$")
    plotter.format_ax(ax,None,np.max(tvec),ti=np.min(tvec))
    ax.set_title(plot_title,fontsize=plotter.fontsizetitles)

def add_ylabel(ax,plotter):
    ax.set_ylabel("Cost",fontsize=plotter.fontsizetitles)

def make_split_gs_subplot(fig,gs):

    ax1 = fig.add_subplot(gs[0,3:])
    ax2 = fig.add_subplot(gs[1,3:], sharex=ax1)
    plt.setp(ax1.get_xticklabels(), visible=False)
        
    ax1.spines.bottom.set_visible(False)
    ax2.spines.top.set_visible(False)
    ax1.set_xticks([])
    #ax1.tick_params(labeltop=False)  # don't put tick labels at the top
    #ax2.xaxis.tick_bottom()

    #from matplotlib tutorials
    d = .5  # proportion of vertical to horizontal extent of the slanted line
    kwargs = dict(marker=[(-1, -d), (1, d)], markersize=12,
                linestyle="none", color='k', mec='k', mew=1, clip_on=False)
    ax1.plot([0, 1], [0, 0], transform=ax1.transAxes, **kwargs)
    ax2.plot([0, 1], [1, 1], transform=ax2.transAxes, **kwargs)

    ax1.set_ylim((-0.1,0.7))
    ax2.set_ylim((-8.6,-8))
    return ax1,ax2


def make_plot(file_names,model_type,method,file_out):

    plotter = PlotParams()
    # Plotting the cumulants
    fig = plotter.make_fig()
    gs = plotter.make_gridspec(fig,hspace=0.05)
    
    ax1,ax2 = make_split_gs_subplot(fig,gs)
    ax_equil = plt.subplot(gs[:,:3])

    #get parameter label from filename
    param_label = None #plotter.make_paramlabel(file_names[-1])
    results1 = compute_data(plotter,file_names,model_type,method,equil="equil",constrained_kappa="pass")
    results2 = compute_data(plotter,file_names,model_type,method,equil="noneq",constrained_kappa="pass")
    
    #add data to plots
    plot_ep(ax_equil,results1[0],results1[3],plotter)
    plot_work(ax_equil,results1[0],results1[1],plotter)
    plot_heat(ax_equil,results1[0],results1[2],plotter)

    plot_ep(ax1,results2[0],results2[3],plotter)
    plot_work(ax2,results2[0],results2[1],plotter)
    plot_heat(ax1,results2[0],results2[2],plotter)

    #formatting
    format_plot(ax_equil,results1[0],"Engineered Swift Equilibration",plotter)
    format_plot(ax1,results2[0],"Minimum Work",plotter)
    format_plot(ax2,results2[0],None,plotter)
    ax1.set_xlabel(None)
    ax2.set_ylabel(None)
    ax_equil.set_ylabel("Cost",fontsize=plotter.fontsizetitles)

    add_panel_label(ax_equil,"(a)",plotter)
    add_panel_label(plt.subplot(gs[:,3:]),"(b)",plotter)

    plt.subplot(gs[:,3:]).patch.set_alpha(0)
    plt.subplot(gs[:,3:]).set_ylabel("Cost",fontsize=plotter.fontsizetitles)
    plt.subplot(gs[:,3:]).yaxis.set_label_coords(-0.12,0.5)
    plt.subplot(gs[:,3:]).tick_params(which="both",axis="x",labelsize=plotter.fontsizeticks)
    plt.subplot(gs[:,3:]).set_yticks([])
    plt.subplot(gs[:,3:]).spines.left.set_visible(False)
    plt.subplot(gs[:,3:]).spines.right.set_visible(False)


    ax2.set_yticks([-8.5,-8.3,-8.1])

    ax2.xaxis.set_label_coords(0.5,-0.12)
    ax_equil.set_ylim((-0.38,0.25))
    ax_equil.yaxis.set_label_coords(-0.12,0.5)
    ax_equil.set_xticks([3,5,10,20,30,40])
    plt.subplot(gs[:,3:]).set_xticks([3,5,10,20,30,40])
    plt.subplot(gs[:,3:]).set_xlim((2.5,40.5))

    ax_inset = ax_equil.inset_axes(bounds=[0.3,0.22,0.5,0.3],transform=ax_equil.transAxes)
    plotter.format_ax_plain(ax_inset)
    ax_inset.scatter(results2[0], results1[3]-results2[3],lw=plotter.lw-1,color="black")
    ax_inset.set_xticks([3,10,20,30,40])
    ax_inset.plot(results2[0], 0*results2[3],lw=plotter.lw,linestyle="dashed",alpha=0.5,color="gray")
    ax_inset.set_ylabel(r"$\Delta \mathcal{E}_{t_f}$",fontsize=plotter.fontsizetitles)
    ax_inset.set_ylim((-0.6,0.05))
    #plt.subplots_adjust(hspace=0)

    h,l = ax_equil.get_legend_handles_labels()

    fig.legend(h,l,
                                fontsize = plotter.fontsizetitles,
                                frameon=False,
                                handlelength=1,
                                loc="center right")
    plt.figtext(0.5, 0.01, param_label, ha="center", fontsize=plotter.fontsizetitles, bbox={"facecolor":"orange", "alpha":0.5, "pad":5})
    plt.savefig(file_out,bbox_inches="tight")

    plt.close()

def fig6():

    #input file
    file_names = [#"T2-0_Lambda1-4_eps1_g0-01.csv",
                  "T3-0_Lambda1-4_eps1_g0-01.csv",
                  "T4-0_Lambda1-4_eps1_g0-01.csv",
                  "T5-0_Lambda1-4_eps1_g0-01.csv",
                  #"T6-0_Lambda1-4_eps1_g0-01.csv",
                  "T7-0_Lambda1-4_eps1_g0-01.csv",
                  "T8-0_Lambda1-4_eps1_g0-01.csv",
                  "T9-0_Lambda1-4_eps1_g0-01.csv",
                  "T10-0_Lambda1-4_eps1_g0-01.csv",
                  "T20-0_Lambda1-4_eps1_g0-01.csv",
                  "T30-0_Lambda1-4_eps1_g0-01.csv",
                  "T40-0_Lambda1-4_eps1_g0-01.csv",
                  #"T50-0_Lambda1-4_eps1_g0-01.csv"
		]
    
    #list what methods to try to plot. all those where the available parameters
    #  exist 
    #will be plotted, otherwise the entry will be skipped.
    model_type = "harmonic"#["harmonic","control","log","hard"] 
    method = "indirect"
    make_plot(file_names,model_type,method,f"plots/costs_v_time{model_type}_{method[0]}.png")
    make_plot(file_names,model_type,method,f"plots/costs_v_time{model_type}_{method[0]}.pdf")



if __name__=="__main__":
   fig6()