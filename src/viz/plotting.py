import numpy as np
import matplotlib.pyplot as plt

from plotscript import PlotParams #contains the plotting functions

def adjust_subplot_fig5(gs):
    #reset all ylims
    plt.subplot(gs[1,3:]).set_ylim((-130,40))
    plt.subplot(gs[1,:3]).set_ylim((-9,4))
    plt.subplot(gs[0,:2]).set_ylim((0.7,1.4))
    plt.subplot(gs[0,2:4]).set_ylim((0.9,2.6))
    plt.subplot(gs[0,4:]).set_ylim((-1.2,1.4))
    plt.subplot(gs[1,3:]).yaxis.set_label_coords(-0.12,0.5)


def adjust_subplot_fig5b(gs):
    #reset all ylims
    plt.subplot(gs[1,3:]).set_ylim((-12,5.2))
    plt.subplot(gs[1,:3]).set_ylim((-1.52,1.72))
    plt.subplot(gs[0,:2]).set_ylim((0.88,1.32))
    plt.subplot(gs[0,2:4]).set_ylim((0.7,4.52))
    plt.subplot(gs[0,4:]).set_ylim((-0.55,0.25))
    plt.subplot(gs[1,3:]).yaxis.set_label_coords(-0.12,0.5)

def adjust_subplot_fig1(gs):
    plt.subplot(gs[1,3:]).set_ylim((-40,35))
    plt.subplot(gs[1,:3]).set_ylim((-0.7,1.5))
    plt.subplot(gs[0,4:]).set_ylim((-0.3,0.4))


def adjust_subplot_fig2(gs):
    plt.subplot(gs[1,3:]).set_ylim((-40,35))
    plt.subplot(gs[1,:3]).set_ylim((-0.7,1.5))
    plt.subplot(gs[0,4:]).set_ylim((-0.3,0.4))

def adjust_subplot_fig2b(gs):
    plt.subplot(gs[0,:2]).set_ylim((0.95,1.32))
    plt.subplot(gs[0,2:4]).set_ylim((0.1,1.2))
    plt.subplot(gs[0,4:]).set_ylim((-0.25,0.12))
    plt.subplot(gs[1,:3]).set_ylim((0,2.8))
    plt.subplot(gs[1,3:]).set_ylim((-10,10))

def adjust_subplot_fig4b(gs):
    plt.subplot(gs[0,:3]).set_ylim((0.88,1.04))
    plt.subplot(gs[0,3:]).set_ylim((0.95,2.15))
    plt.subplot(gs[1,3:]).set_ylim((0.05,1.15))
    plt.subplot(gs[1,:3]).set_ylim((-0.25,0.25))

def plot_result(models,methods,file_names,equil,constrained_kappa,adjust_subplot):
    plotter = PlotParams()

    #uncomment if you want the label
    #param_label = plotter.make_paramlabel(file_name)
    
    fig_out = plotter.make_fig()
    gs_cumulants = plotter.make_gridspec(fig_out)
    plotter.plot_all_cumulants(fig_out,gs_cumulants,
                                    models,
                                    methods,
                                    file_names,
                                    equil=equil,constrained_kappa=constrained_kappa)

    adjust_subplot(gs_cumulants)
    return fig_out

def fig1():
    file_names =  ["T3-0_Lambda9-0_eps1_g0-01.csv","T3-0_Lambda9-0_eps1_g0-1.csv"]
    models = ["log","hard"] #"harmonic",
    methods = ["direct","indirect"]
    fig_out = plot_result(models,methods,file_names, ["equil"],"none",adjust_subplot_fig1)
    fig_out.savefig(f"plots/fig1.png", bbox_inches="tight")

    plt.close()

def fig2():
    file_names =  ["T3-0_Lambda1-4_eps1_g0-01.csv","T3-0_Lambda1-4_eps1_g0-001.csv"]
    models = ["harmonic"] #"harmonic",
    methods = ["slowfast","direct","indirect"]
    fig_out = plot_result(models,methods,file_names, ["equil"],"none",adjust_subplot_fig2)
    fig_out.savefig(f"plots/fig2.png", bbox_inches="tight")

    plt.close()


def fig2b():
    file_names =  ["T3-0_Lambda1-4_eps1_g0-01.csv","T3-0_Lambda1-4_eps1_g0-001.csv"]
    models = ["harmonic"] #"harmonic",
    methods = ["slowfast","direct","indirect"]
    fig_out = plot_result(models,methods,file_names, ["equil"],"contract",adjust_subplot_fig2b)
    fig_out.savefig(f"plots/fig2b.png", bbox_inches="tight")
    fig_out.savefig(f"plots/fig2b.pdf", bbox_inches="tight")

    plt.close()

def fig4b():
    file_names =  ["T4-0_Lambda1-0_eps1_g0-1.csv","T4-0_Lambda10-0_eps1_g0-1.csv"]
    models = ["hard"] #"harmonic",
    methods = ["direct"]
    fig_out = plot_result(models,methods,file_names, ["stiffness_control","equil"],"constrained_kappa",adjust_subplot_fig4b)
    h,l = plt.gca().get_legend_handles_labels()
    plt.gca().legend(handles = h,labels= ["Control",r"State ($\Lambda=1$)",r"State ($\Lambda=10$)"]
                                        ,fontsize=20
                                        ,loc="lower center"
                                        ,frameon=False
                                        ,ncols=1
                                        ,handlelength=1
                                        ,columnspacing=0.7)
    fig_out.savefig(f"plots/fig4b_temp2.png", bbox_inches="tight")
    fig_out.savefig(f"plots/fig4b.pdf", bbox_inches="tight")
    plt.close()


def fig5():
    file_names =  ["T3-0_Lambda1-4_eps1_g0-01.csv"]#,"T3-0_Lambda1-4_eps1_g0-01.csv"]
                   #"T7-0_Lambda1-4_eps1_g0-01.csv"]
    models = ["harmonic"] #"harmonic",
    methods = ["indirect","direct"]
    fig_out = plot_result(models,methods,file_names, ["noneq"],"none",adjust_subplot_fig5)
    fig_out.savefig(f"plots/fig5.png", bbox_inches="tight")
    fig_out.savefig(f"plots/fig5.pdf",bbox_inches="tight")
    plt.close()


def fig5b():
    file_names =  ["T7-0_Lambda1-4_eps1_g0-1.csv"]#,"T3-0_Lambda1-4_eps1_g0-01.csv"]#,"T3-0_Lambda1-4_eps1_g0-01.csv"]
                   #"T7-0_Lambda1-4_eps1_g0-01.csv"]
    models = ["harmonic"] #"harmonic",
    methods = ["indirect","direct"]
    fig_out = plot_result(models,methods,file_names, ["noneq"],"contract",adjust_subplot_fig5b)
    fig_out.savefig(f"plots/fig5b.png", bbox_inches="tight")
    fig_out.savefig(f"plots/fig5b.pdf",bbox_inches="tight")
    plt.close()

if __name__=="__main__":
    
    fig4b()

