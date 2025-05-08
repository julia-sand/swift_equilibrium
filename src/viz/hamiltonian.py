import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from plotscript import PlotParams


def ham_plot(file_name,file):
    plotter = PlotParams()

    param_label = plotter.make_paramlabel(file_name)

    models = ["hard", "control", "harmonic", "log"] 

    # Plotting the cumulants
    fig = plt.figure(figsize=(15, 8)) #, constrained_layout=True)
    ax1 = fig.add_axes(rect = (0.1,0.1,0.8,0.8))

    for model_type in models:
        try:
            #get the right folder 
            df = plotter.get_data(model_type,"indirect",equil=True)

            def b(y4):
                if model_type=="harmonic":
                    return (y4*(Lambda**2))/(2*g)
                elif model_type=="log":
                    return (g/(y4+1e-10))*(np.sqrt((1+(Lambda*y4/g)**2))-1)
                elif model_type=="control":
                    return 0 #todo
                else:
                    return 0
            
            def V(kappa,y4,posvar):
                lambda_vec = b(y4)#np.gradient(kappa,times_vec)

                if model_type=="harmonic":
                    return (lambda_vec/Lambda)**2
                elif model_type=="hard":
                    return 0
                elif model_type=="log":
                    return np.where(np.abs(lambda_vec)<Lambda, -np.log(1-(lambda_vec/Lambda)**2),1e10)
                elif model_type=="control":
                    return kappa*(kappa*posvar-1) 
                else:
                    return 

            times_vec = df.t.to_numpy()
            dt = times_vec[1]
            x1,x2,x3,x4 = df.x1.to_numpy(),df.x2.to_numpy(),df.x3.to_numpy(),df.kappa.to_numpy()
            y1,y2,y3,y4 = df.y1.to_numpy(),df.y2.to_numpy(),df.y3.to_numpy(),df.y4.to_numpy()
            ham = -(x3+g*V(x4,y4,x1)) + y1*2*epsilon*x2 + y2*(-x2-epsilon*(x4*x1-x3)) + y3*2*(1-x3-epsilon*x4*x2) + y4*b(y4)#np.gradient(x4,times_vec)

            plotter.plot_func(ax1,
                        times_vec,ham,
                        "pre-Hamiltonian",
                        f"{model_type}")
        except:
            pass


    # Adjust layout to prevent overlap
    ax1.legend(fontsize = fontsize)
    plt.figtext(0.5, 0.01, param_label, ha="center", fontsize=fontsizetitles, bbox={"facecolor":"orange", "alpha":0.5, "pad":5})
    plt.savefig(file_out,bbox_inches="tight")

    plt.close()


if __name__=="__main__":

    #input file
    file_name = "T3-0_Lambda2-0_eps1-0_g0-01.csv"
    #output file
    file_out = "swift_equilibrium/hamiltonian1.png"
    
    ham_plot(file_name,file)