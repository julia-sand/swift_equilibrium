"""computes the cost from a given csv file"""

import numpy as np
import matplotlib.pyplot as plt
from plotscript import PlotParams #contains the plotting functions

if __name__=="__main__":

    plotter = PlotParams()
    file_names =  ["T3-0_Lambda1-4_eps1_g0-1.csv","T3-0_Lambda1-4_eps1_g0-01.csv"]
    models = ["harmonic"] #"harmonic",
    methods = ["indirect","direct","slowfast"]
    equil=False
    for file_name in file_names:
        param_label = plotter.make_paramlabel(file_name)
        print(rf"{param_label} \n")
        for model_type in models:
            for method in methods:
                print(f"model: {model_type}; method: {method}")
                try:
                    df = plotter.get_data(model_type,method,equil,file_name)
                    ep = plotter.compute_entropy_production(df)#,plotter.get_g(file_name),plotter.get_Lambda(file_name),model_type)
                    cost = plotter.compute_work(df)#,plotter.get_g(file_name),plotter.get_Lambda(file_name),model_type)
                    print(f"EP: {ep}")
                    print(f"W: {cost}")
                except FileNotFoundError:
                    print("Requested data not available.")
                    pass