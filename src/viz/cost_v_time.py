import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from plotscript import *

"""
Produces Fig. 8 in paper
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


def format_plot(ax,tvec,plot_title,plotter):
    
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

    return ax1,ax2

def adjust_inset_fig6(ax_inset):
    ax_inset.set_ylim((-0.02, 0.57))
  
def adjust_inset_fig6cd(ax_inset):
    ax_inset.set_ylim((-0.002, 0.065))

def adjust_subplots_fig6(ax1,ax2,ax_equil):
    ax2.set_yticks([-8.5,-8.3,-8.1])

    ax1.set_ylim((-0.1,0.7))
    ax2.set_ylim((-8.6,-8))
    ax_equil.set_ylim((-0.38,0.22))

def adjust_subplots_fig6cd(ax_noneq,ax2,ax_equil):

    ax_noneq.set_ylim((-0.35,0.62))
    ax_equil.set_ylim((-0.05,0.55)) 

def plot_inset(ax_equil,results1,results2,plotter,adjust_inset):

    ax_inset = ax_equil.inset_axes(bounds=[0.35,0.24,0.5,0.3],transform=ax_equil.transAxes)
    ax_inset.plot(results2[0], 0*results2[3],lw=plotter.lw,linestyle="dashed",alpha=0.5,color="gray")
    ax_inset.set_ylabel(r"$\Delta \mathcal{E}_{t_f}$",fontsize=plotter.fontsizetitles,
                    color="maroon")
    plotter.format_ax_plain(ax_inset)
    ax_inset.plot(results2[0], results2[3]-results1[3],marker="o",markersize=10,
                label=r"$\mathcal{E}^{\boldsymbol{(b)}}_{t_f}-\mathcal{E}^{\boldsymbol{(a)}}_{t_f}$",lw=plotter.lw-2,color="maroon")

    ax_inset.set_xticks([3,10,20,30,40])
    #ax_inset.set_ylim((-0.03,0.63))
    ax_inset.xaxis.label.set_color("maroon") 
    ax_inset.legend(frameon=False,
            loc="lower right",
            fontsize=plotter.fontsizetitles,
            handletextpad=-0.05)
    adjust_inset(ax_inset)


def make_plot(file_names,
                model_type,
                method,
                constrained_kappa,
                file_out,
                adjust_subplots_fun,
                adjust_inset):

    plotter = PlotParams()

    # Plotting the cumulants
    fig = plotter.make_fig()
    gs = plotter.make_gridspec(fig,hspace=0.05)
    
    ax_equil = plt.subplot(gs[:,:3])
    ax_noneq = plt.subplot(gs[:,3:])

    #get parameter label from filename
    param_label = None #plotter.make_paramlabel(file_names[-1])
    results1 = compute_data(plotter,file_names,model_type,method,equil="equil",constrained_kappa=constrained_kappa)
    results2 = compute_data(plotter,file_names,model_type,method,equil="noneq",constrained_kappa=constrained_kappa)
    
    #add data to plots
    plot_ep(ax_equil,results1[0],results1[3],plotter)
    plot_work(ax_equil,results1[0],results1[1],plotter)
    plot_heat(ax_equil,results1[0],results1[2],plotter)

    if constrained_kappa!="contract":
        ax1,ax2 = make_split_gs_subplot(fig,gs)
        plot_ep(ax1,results2[0],results2[3],plotter)
        plot_work(ax2,results2[0],results2[1],plotter)
        plot_heat(ax1,results2[0],results2[2],plotter)
        format_plot(ax1,results2[0],"Minimum Work",plotter)
        format_plot(ax2,results2[0],None,plotter)
        ax1.set_xlabel(None)
        ax2.set_ylabel(None)
        ax2.xaxis.set_label_coords(0.5,-0.12)
        ax2.set_xlabel(None)
        adjust_subplots_fun(ax1,ax2,ax_equil)
        ax1.plot(results2[0],np.zeros(len(results2[0])),"--",linewidth=plotter.lw,color="gray",zorder=0,alpha=0.5)

        #hide noneq axis if splitting the yax 
        ax_noneq.patch.set_alpha(0)
        ax_noneq.set_yticks([])
        ax_noneq.spines.left.set_visible(False)
        ax_noneq.spines.right.set_visible(False)
        ax1.text(x=0.02,y=0.9,s="(b)",fontsize=plotter.fontsizetitles,
            fontweight="bold",transform=ax1.transAxes,zorder=1000)

    else: 
        plot_ep(ax_noneq,results2[0],results2[3],plotter)
        plot_work(ax_noneq,results2[0],results2[1],plotter)
        plot_heat(ax_noneq,results2[0],results2[2],plotter)
        ax_noneq.plot(results2[0],np.zeros(len(results2[0])),"--",linewidth=plotter.lw,color="gray",zorder=0,alpha=0.5)
        adjust_subplots_fun(ax_noneq,None,ax_equil)
        ax_noneq.text(x=0.02,y=0.95,s="(b)",fontsize=plotter.fontsizetitles,
            fontweight="bold",transform=ax_noneq.transAxes,zorder=1000)
    
    ax_noneq.tick_params(which="both",axis="x",labelsize=plotter.fontsizeticks)
    ax_noneq.set_xticks([3,5,10,20,30,40])
    ax_equil.set_xticks([3,5,10,20,30,40])
    ax_noneq.yaxis.set_label_coords(-0.12,0.5)
    ax_noneq.set_xlim((2.5,40.5))  
    ax_noneq.set_ylabel("Cost",fontsize=plotter.fontsizetitles)
    ax_equil.plot(results1[0],np.zeros(len(results1[0])),"--",linewidth=plotter.lw,color="gray",zorder=0,alpha=0.5)
    ax_equil.text(x=0.02,y=0.95,s="(a)",fontsize=plotter.fontsizetitles,
            fontweight="bold",transform=ax_equil.transAxes,zorder=1000)
    
    #formatting
    format_plot(ax_noneq,results2[0],"Minimum Work",plotter)
    format_plot(ax_equil,results1[0],"Engineered Swift Equilibration",plotter)
    ax_equil.set_ylabel("Cost",fontsize=plotter.fontsizetitles)
    
    #formatting 
    ax_equil.yaxis.set_label_coords(-0.12,0.5)

    #plot inset
    plot_inset(ax_equil,results1,results2,plotter,adjust_inset)
 
    h,l = ax_equil.get_legend_handles_labels()
   
    fig.legend(h,l,
                                fontsize = plotter.fontsizetitles,
                                frameon=False,
                                handlelength=1,
                                loc="center right")
    plt.figtext(0.5, 0.01, param_label, ha="center", fontsize=plotter.fontsizetitles, bbox={"facecolor":"orange", "alpha":0.5, "pad":5})
    plt.savefig(file_out,bbox_inches="tight")

    plt.close()

def fig8():

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
    constrained_kappa = "pass"
    make_plot(file_names,model_type,method,constrained_kappa,f"plots/fig8.png",adjust_subplots_fig6,adjust_inset_fig6)
    make_plot(file_names,model_type,method,constrained_kappa,f"plots/fig8.pdf",adjust_subplots_fig6,adjust_inset_fig6)


def fig8cd():

    #input file
    file_names = ["T3-0_Lambda1-4_eps1_g0-01.csv",
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
        ]
    
    model_type = "harmonic"#["harmonic","control","log","hard"] 
    method = "indirect"
    constrained_kappa = "contract"
    make_plot(file_names,model_type,method,constrained_kappa,f"plots/fig8cd.png",adjust_subplots_fig6cd,adjust_inset_fig6cd)
    make_plot(file_names,model_type,method,constrained_kappa,f"plots/fig8cd.pdf",adjust_subplots_fig6cd,adjust_inset_fig6cd)

if __name__=="__main__":
   fig8()
   fig8cd()