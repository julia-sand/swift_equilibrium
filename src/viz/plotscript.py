import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import pandas as pd
import string

"""
This file contains the utility and plotting functions to 
present the results from integration

""" 


class PlotParams():
    def __init__(self):
        
        #set up fontsizes
        self.fontsizeticks = 18
        self.fontsizetitles = 22

        self.lw = 3
        

    def plot_func(self,ax,x,y,ylabel,legendlabel):
        """Simple plot and formatting to plot one line of data. Used for plotting
        Hamiltonian and running cost
        """

        ax.plot(x, y, lw = self.lw, label = legendlabel)
        ax.set_ylabel(ylabel,fontsize=self.fontsizetitles)
        ax.set_xlabel('t',fontsize=self.fontsizetitles)
        ax.tick_params(labelsize=self.fontsizeticks)

    def make_paramlabel(self,file_name):
        """Creates the parameter label to add to the base of the plots. 
        Parameters are taken from the file name of the run. 
        """
        #read params from filename? 
        params = file_name.rsplit(".",1)[0].split('_') #removes .csv from end
        tval = params[0].replace('-', '.')
        lambdaval = params[1].replace('-', '.')
        epsval = params[2].replace('-', '.')
        gval = params[-1].replace('-', '.')

        def get_idx(string):
            for i in enumerate(string):
                if str.isdigit(i[1]):
                    return i[0] 
            
        T = float(tval[get_idx(tval):])
        Lambda = float(lambdaval[get_idx(lambdaval):])
        epsilon = float(epsval[get_idx(epsval):])
        g = float(gval[get_idx(gval):])
        param_label = rf"$T={T}; \Lambda={Lambda}; \varepsilon={epsilon}; g={g}$"

        return param_label

    def get_data(self,model_type,method,equil):
        
        """
        function which gets the filepath of model and method 
        
        Returns a dataframe if the data is available. 
        """
        
        #get the right folder 
        if model_type=="hard":
            folder_path ="swift_equilibrium/results/hard/"
        elif model_type =="log":
            folder_path ="swift_equilibrium/results/log/"
        elif model_type =="harmonic":
            folder_path ="swift_equilibrium/results/harmonic/"
        elif model_type =="control":
            folder_path ="swift_equilibrium/results/control/"
        
        #add equilibrium
        if equil:
            folder_path = folder_path + "equil/"
        else: 
            folder_path = folder_path + "noneq/"

        if method =="direct":
            df = pd.DataFrame(pd.read_csv(folder_path + "direct/" + file_name))
        elif method =="indirect": 
            df = pd.DataFrame(pd.read_csv(folder_path + "indirect/" + file_name))
            
        elif method =="slowfast": 
            df = pd.DataFrame(pd.read_csv(folder_path + "slowfast/"+file_name))
           

        return df



    def make_plot(self,models,methods,file_name,param_label,equil=True):
        """
        Plots the data of specified parameters (via the filename) and returns matplotlib figure.

        """
        
        # figure setup
        fig = plt.figure(figsize=(15, 8))#, constrained_layout=True)
        gs_cumulants = gridspec.GridSpec(2, 6, 
                            width_ratios=[1, 1, 1, 1,1,1], 
                            height_ratios=[1, 1],
                            hspace=0.4,
                            wspace=1.2)

        pos_var_plot = plt.subplot(gs_cumulants[0, 2:4])
        xcorr_plot = plt.subplot(gs_cumulants[0, 4:])
        kappa_plot = plt.subplot(gs_cumulants[1,:3])
        lambda_plot = plt.subplot(gs_cumulants[1, 3:])
        mom_var_plot = plt.subplot(gs_cumulants[0, 0:2])
        
        def plot_func(ax,x,y,ylabel,legendlabel):
            
            if model_type=="hard": #overwrite legend label
                legendlabel = f"compact, {method}" 
            if method =="direct":
                ax.plot(x, y, label = legendlabel,lw=self.lw)
            else: 
                ax.plot(x, y, label = legendlabel,lw=self.lw,linestyle="dashed",zorder=100)
            ax.set_ylabel(ylabel,fontsize=self.fontsizetitles)
            ax.set_xlabel('t',fontsize=self.fontsizetitles)
            ax.tick_params(labelsize=self.fontsizeticks)
            ax.set_xlim((-0.1,3.1))


        for model_type in models:
            for method in methods:
                legendlabel=f"{model_type}, {method}"

                try:   
                    df = get_data(model_type,method,equil)

                    # Plot on the first subplot (top-left)
                    #"Position variance"
                    plot_func(pos_var_plot,df.t, df.x1,'Position Variance',legendlabel)#,f"{method}:{model_type}")
                    plot_func(xcorr_plot,df.t, df.x2,'Cross Correlation',legendlabel)
                    plot_func(mom_var_plot,df.t, df.x3,'Mom. Variance',legendlabel)
                    mom_var_plot.set_ylim((np.min(df.x3.to_numpy()-0.03),1.04))

                    # Plot on the fourth subplot (bottom-right)
                    plot_func(kappa_plot,df.t, df["kappa"],r'Stiffness, $\kappa_t$',legendlabel)

                    if model_type!="control":
                        plot_func(lambda_plot,df.t.to_numpy(), np.gradient(df["kappa"].to_numpy(),df.t.to_numpy())
                                            ,r'Control, $\lambda_t$',legendlabel)  
                
                
                except: 
                    pass

        #add panel labels
        mom_var_plot.text(x= 0.05, y = 0.85, s="(a)",transform=mom_var_plot.transAxes,fontsize=fontsizetitles)
        pos_var_plot.text(x= 0.05, y = 0.85, s="(b)",transform=pos_var_plot.transAxes,fontsize=fontsizetitles)
        xcorr_plot.text(x= 0.05, y = 0.85, s="(c)",transform=xcorr_plot.transAxes,fontsize=fontsizetitles)
        kappa_plot.text(x= 0.05*(2/3), y = 0.85, s="(d)",transform=kappa_plot.transAxes,fontsize=fontsizetitles)
        lambda_plot.text(x= 0.05*(2/3), y = 0.85 , s="(e)",transform=lambda_plot.transAxes,fontsize=fontsizetitles)

        #add legend
        kappa_plot.legend(fontsize=self.fontsizeticks,loc="lower center",frameon=False)

        plt.figtext(0.5, 0.01, param_label, ha="center", fontsize=self.fontsizetitles, bbox={"facecolor":"orange", "alpha":0.5, "pad":5})

        return fig