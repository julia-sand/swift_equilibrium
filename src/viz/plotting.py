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
    plt.subplot(gs[1,3:]).set_ylim((-40,35))
    plt.subplot(gs[1,:3]).set_ylim((-0.7,1.5))
    plt.subplot(gs[0,4:]).set_ylim((-0.3,0.4))

def plot_result(models,methods,file_names,file_out,equil,constrained_kappa,adjust_subplot):
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
    fig_out.savefig(file_out, bbox_inches="tight")

    plt.close()

def fig1():
    file_names =  ["T3-0_Lambda9-0_eps1_g0-01.csv","T3-0_Lambda9-0_eps1_g0-1.csv"]
    models = ["log","hard"] #"harmonic",
    methods = ["direct","indirect"]
    plot_result(models,methods,file_names,f"plots/fig1.png", "equil","none",adjust_subplot_fig1)

def fig2():
    file_names =  ["T3-0_Lambda1-4_eps1_g0-01.csv","T3-0_Lambda1-4_eps1_g0-001.csv"]
    models = ["harmonic"] #"harmonic",
    methods = ["slowfast","direct","indirect"]
    plot_result(models,methods,file_names,f"plots/fig2.png", "equil","none",adjust_subplot_fig2)



def fig4():
    file_names =  ["T3-0_Lambda9-0_eps1_g0-1.csv"]
    models = ["hard"] #"harmonic",
    methods = ["direct"]
    plot_result(models,methods,file_names,f"plots/fig4.png", "stiffness_control","negative_constrained_kappa",adjust_subplot_fig4)


if __name__=="__main__":
    
    fig4()

