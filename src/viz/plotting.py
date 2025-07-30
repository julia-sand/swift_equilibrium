import numpy as np
import matplotlib.pyplot as plt

from plotscript import PlotParams #contains the plotting functions

def adjust_subplot_fig1(gs):
    plt.subplot(gs[1,3:]).set_ylim((-40,35))
    plt.subplot(gs[1,:3]).set_ylim((-0.7,1.5))
    plt.subplot(gs[0,4:]).set_ylim((-0.3,0.4))


def adjust_subplot_fig2(gs):
    plt.subplot(gs[1,3:]).set_ylim((-40,35))
    plt.subplot(gs[1,:3]).set_ylim((-0.7,1.5))
    plt.subplot(gs[0,4:]).set_ylim((-0.3,0.4))

def adjust_subplot_fig4(gs):
    plt.subplot(gs[1,3:]).set_ylim((-1.6,1.6))
    plt.subplot(gs[1,:3]).set_ylim((-0.35,0.4))

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

def fig4():
    file_names =  ["T3-0_Lambda9-0_eps1_g0-1.csv"]
    models = ["hard"] #"harmonic",
    methods = ["direct"]
    fig_out = plot_result(models,methods,file_names, ["stiffness_control","equil"],"negative_constrained_kappa",adjust_subplot_fig4)
    plt.gca().legend(labels= ["Control","State"]
                                        ,fontsize=20
                                        ,loc="lower left"
                                        ,frameon=False
                                        ,ncols=2
                                        ,handlelength=1
                                        ,columnspacing=0.7)
    fig_out.savefig(f"plots/fig4.png", bbox_inches="tight")
    fig_out.savefig(f"plots/fig4.pdf", bbox_inches="tight")
    plt.close()

if __name__=="__main__":
    
    fig4()

