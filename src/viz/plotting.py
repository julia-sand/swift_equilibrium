import numpy as np
import matplotlib.pyplot as plt

from plotscript import PlotParams #contains the plotting functions

def make_legend(h,l,fig):
    
    fig.legend(h,l
                ,loc="upper center"
                ,frameon=False
                ,ncols=2
                #,handlelength=1
                #,columnspacing=1.
                ,bbox_to_anchor=(0.5, -0.05))
    fig.subplots_adjust(bottom=0.01)

def make_legend_fig56(handles,labels,fig):
    
    handles = np.concatenate((handles[::2],handles[1::2]),axis=0)
    labels = np.concatenate((labels[::2],labels[1::2]),axis=0)

    make_legend(handles,labels,fig)


def make_legend_fig1(handles,labels,fig):
    
    handles = np.concatenate(([handles[-1]],handles[:3]),axis=0)
    labels = np.concatenate(([labels[-1]],labels[:3]),axis=0)

    make_legend(handles,labels,fig)


def adjust_subplot_fig1(gs):
    plt.subplot(gs[0,:2]).set_ylim((0.85,1.04))
    plt.subplot(gs[0,2:4]).set_ylim((0.96,2.14))
    plt.subplot(gs[0,4:]).set_ylim((-0.27,0.43))
    plt.subplot(gs[1,3:]).set_ylim((-17,17))
    plt.subplot(gs[1,:3]).set_ylim((-0.11,1.21))

def adjust_subplot_fig2(gs):
    plt.subplot(gs[0,:2]).set_ylim((0.87,1.06))
    plt.subplot(gs[0,2:4]).set_ylim((0.94,2.17))
    plt.subplot(gs[0,4:]).set_ylim((-0.27,0.43))
    plt.subplot(gs[1,3:]).set_ylim((-13,13))
    plt.subplot(gs[1,:3]).set_ylim((-0.84,1.54))

def adjust_subplot_fig3(gs):
    plt.subplot(gs[0,:2]).set_ylim((0.95,1.32))
    plt.subplot(gs[0,2:4]).set_ylim((0.31,1.21))
    plt.subplot(gs[0,4:]).set_ylim((-0.25,0.12))
    plt.subplot(gs[1,:3]).set_ylim((0.77,2.8))
    plt.subplot(gs[1,3:]).set_ylim((-10,10))

def adjust_subplot_fig5(gs):
    plt.subplot(gs[0,:3]).set_ylim((0.88,1.03))
    plt.subplot(gs[0,3:]).set_ylim((0.92,2.17))
    plt.subplot(gs[1,3:]).set_ylim((0.07,1.21))
    plt.subplot(gs[1,:3]).set_ylim((-0.21,0.27))

def adjust_subplot_fig6(gs):
    plt.subplot(gs[0,:3]).set_ylim((0.88,1.04))
    plt.subplot(gs[0,3:]).set_ylim((0.92,2.18))
    plt.subplot(gs[1,3:]).set_ylim((-0.25,1.35))
    plt.subplot(gs[1,:3]).set_ylim((-0.22,0.28))

def adjust_subplot_fig7(gs):
    #reset all ylims
    plt.subplot(gs[1,3:]).set_ylim((-130,40))
    plt.subplot(gs[1,:3]).set_ylim((-9,4))
    plt.subplot(gs[0,:2]).set_ylim((0.7,1.4))
    plt.subplot(gs[0,2:4]).set_ylim((0.9,2.6))
    plt.subplot(gs[0,4:]).set_ylim((-1.2,1.4))
    plt.subplot(gs[1,3:]).yaxis.set_label_coords(-0.12,0.5)

def adjust_subplot_fig8(gs):
    #reset all ylims
    plt.subplot(gs[1,3:]).set_ylim((-12,5.2))
    plt.subplot(gs[1,:3]).set_ylim((-0.52,1.72))
    plt.subplot(gs[0,:2]).set_ylim((0.88,1.32))
    plt.subplot(gs[0,2:4]).set_ylim((0.7,4.62))
    plt.subplot(gs[0,4:]).set_ylim((-0.55,0.25))
    plt.subplot(gs[1,3:]).yaxis.set_label_coords(-0.12,0.5)

def plot_result(models,methods,file_names,equil,constrained_kappa,
                adjust_subplot,make_legend=make_legend):
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
    h,l = plt.subplot(gs_cumulants[1,:3]).get_legend_handles_labels()
    make_legend(h,l,fig_out)

    return fig_out

def fig1():
    file_names =  ["T3-0_Lambda1-4_eps1_g0-01.csv","T3-0_Lambda1-4_eps1_g0-0001.csv"]
    models = ["harmonic"] #"harmonic",
    methods = ["slowfast","direct","indirect"]
    fig_out = plot_result(models,methods,file_names, ["equil"],"none",adjust_subplot_fig1,make_legend_fig1)
    
    fig_out.savefig(f"plots/fig1.png", bbox_inches="tight")
    fig_out.savefig(f"plots/fig1.pdf", format="pdf", bbox_inches="tight")

    plt.close()

def fig2():
    file_names =  ["T3-0_Lambda9-0_eps1_g0-001.csv","T3-0_Lambda9-0_eps1_g0-0.csv"]
    models = ["log","hard"] #"harmonic",
    methods = ["direct","indirect"]
    fig_out = plot_result(models,methods,file_names, ["equil"],"none",adjust_subplot_fig2)
    
    fig_out.savefig(f"plots/fig2.png", bbox_inches="tight")
    fig_out.savefig(f"plots/fig2.pdf", format="pdf", bbox_inches="tight")

    plt.close()

def fig3():
    file_names =  ["T3-0_Lambda1-4_eps1_g0-01.csv"]
    models = ["harmonic"] #"harmonic",
    methods = ["direct","indirect"]
    fig_out = plot_result(models,methods,file_names, ["equil"],"contract",adjust_subplot_fig3)
    fig_out.savefig(f"plots/fig3.png", bbox_inches="tight")
    fig_out.savefig(f"plots/fig3.pdf", format="pdf", bbox_inches="tight")

    plt.close()

def fig5():
    file_names =  ["T4-0_Lambda1-0_eps1_g0-1.csv","T4-0_Lambda10-0_eps1_g0-1.csv"]
    models = ["hard"] #"harmonic",
    methods = ["direct"]
    fig_out = plot_result(models,methods,file_names, ["equil","stiffness_control"],"constrained_kappa",adjust_subplot_fig5,make_legend_fig56)
    h,l = plt.gca().get_legend_handles_labels()
    fig_out.savefig(f"plots/fig5.png", bbox_inches="tight")
    fig_out.savefig(f"plots/fig5.pdf", format="pdf", bbox_inches="tight")
    plt.close()



def fig6():
    file_names =  ["T4-0_Lambda1-0_eps1_g0-1.csv","T4-0_Lambda10-0_eps1_g0-1.csv"]
    models = ["hard"] #"harmonic",
    methods = ["direct"]
    fig_out = plot_result(models,methods,file_names, ["equil","stiffness_control"],"negative_constrained_kappa_small",adjust_subplot_fig6,make_legend_fig56)
    fig_out.savefig(f"plots/fig6.png", bbox_inches="tight")
    fig_out.savefig(f"plots/fig6.pdf", format="pdf", bbox_inches="tight")
    plt.close()

def fig7():
    file_names =  ["T3-0_Lambda1-4_eps1_g0-01.csv"]#,"T3-0_Lambda1-4_eps1_g0-01.csv"]
                   #"T7-0_Lambda1-4_eps1_g0-01.csv"]
    models = ["harmonic"] #"harmonic",
    methods = ["indirect","direct"]
    fig_out = plot_result(models,methods,file_names, ["noneq"],"none",adjust_subplot_fig7)
    fig_out.savefig(f"plots/fig7.png", bbox_inches="tight")
    fig_out.savefig(f"plots/fig7.pdf", format="pdf", bbox_inches="tight")
    plt.close()


def fig8():
    file_names =  ["T7-0_Lambda1-4_eps1_g0-1.csv"]#,"T3-0_Lambda1-4_eps1_g0-01.csv"]#,"T3-0_Lambda1-4_eps1_g0-01.csv"]
                   #"T7-0_Lambda1-4_eps1_g0-01.csv"]
    models = ["harmonic"] #"harmonic",
    methods = ["indirect","direct"]
    fig_out = plot_result(models,methods,file_names, ["noneq"],"contract",adjust_subplot_fig8)
    fig_out.savefig(f"plots/fig8.png", bbox_inches="tight")
    fig_out.savefig(f"plots/fig8.pdf", format="pdf", bbox_inches="tight")
    plt.close()

if __name__=="__main__":
    
    fig1()
    #fig2()
    #fig3()
    #fig5()
    #fig6()
    #fig7()
    fig8()


