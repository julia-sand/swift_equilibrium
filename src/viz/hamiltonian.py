import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from plotscript import PlotParams


def ham_plot(file_name,file_out,equil):
    plotter = PlotParams()

    Lambda = np.sqrt(2)
    g = plotter.get_g(file_name)

    param_label = plotter.make_paramlabel(file_name)

    models = ["harmonic", "log"]#["control", #, "hard"] 

    # Plotting the cumulants
    fig = plt.figure(figsize=(15, 8)) #, constrained_layout=True)
    ax1 = fig.add_axes(rect = (0.1,0.1,0.8,0.8))

    for model_type in models:
        try:
            #get the right folder 
            df = plotter.get_data(model_type,"indirect",equil,file_name=file_name)

            times_vec = df.t.to_numpy()
            dt = times_vec[1]
            x1,x2,x3,x4 = df.x1.to_numpy(),df.x2.to_numpy(),df.x3.to_numpy(),df.kappa.to_numpy()
            y1,y2,y3,y4 = df.y1.to_numpy(),df.y2.to_numpy(),df.y3.to_numpy(),df.y4.to_numpy()
            ham = -(x3+g*plotter.get_Vfun(df,Lambda,g,model_type)) + y1*2*epsilon*x2 + y2*(-x2-epsilon*(x4*x1-x3)) + y3*2*(1-x3-epsilon*x4*x2) + y4*plotter.b(y4,model_type,Lambda,g)#np.gradient(x4,times_vec)

            plotter.plot_func(ax1,
                        times_vec,ham,
                        "pre-Hamiltonian",
                        f"{model_type}")
        except FileNotFoundError:
            pass


    # Adjust layout to prevent overlap
    ax1.legend(fontsize = plotter.fontsizetitles)
    plt.figtext(0.5, 0.01, param_label, ha="center", fontsize=plotter.fontsizetitles, bbox={"facecolor":"orange", "alpha":0.5, "pad":5})
    plt.savefig(file_out,bbox_inches="tight")

    plt.close()


if __name__=="__main__":

    #input file
    file_names = ["T3-0_Lambda1-4_eps1_g0-1.csv",
                    "T3-0_Lambda1-4_eps1_g0-01.csv",
                    "T3-0_Lambda1-4_eps1_g0-001.csv"]

    for file_name in enumerate(file_names):
        ham_plot(file_name[1],f"hamiltonian_equil{file_name[0]}.png",equil="equil")