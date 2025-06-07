import string

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec

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

    def get_idx(self,string):
        for i in enumerate(string):
            if str.isdigit(i[1]):
                return i[0] 
    
    def get_param_value(self,param):
        tempval = param.replace('-', '.')
        return float(tempval[self.get_idx(tempval):])

    def get_params(self,file_name):
        
        #read params from filename? 
        params = file_name.rsplit(".",1)[0].split('_') #removes .csv from end
        return params 
 
    def make_paramlabel(self,file_name):
        """Creates the parameter label to add to the base of the plots. 
        Parameters are taken from the file name of the run. 
        """
        #read params from filename? 
        params = self.get_params(file_name)

        param_label = rf"$T={self.get_param_value(params[0])}; \Lambda={self.get_param_value(params[1])}; \varepsilon={self.get_param_value(params[2])}; g={self.get_param_value(params[3])}$"

        return param_label        
    
    def get_g(self,file_name):
        params = self.get_params(file_name)

        return self.get_param_value(params[1])

    def get_Lambda(self,file_name):
        params = self.get_params(file_name)

        return self.get_param_value(params[3])


    def get_data(self,model_type,method,equil,file_name):
        
        """
        function which gets the filepath of model and method 
        
        Returns a dataframe if the data is available. 
        """
        
        #get the right folder 
        #if model_type=="hard":
        #    
        #elif model_type =="log":
        #    folder_path ="results/log/"
        #elif model_type =="harmonic":
        #    folder_path ="results/harmonic/"
        #elif model_type =="control":
        #    folder_path ="results/control/"
        folder_path =f"results/{model_type}/"
        
        #add equilibrium
        if equil:
            folder_path = folder_path + "equil/"
        else: 
            folder_path = folder_path + "noneq/"

        return pd.DataFrame(pd.read_csv(folder_path + f"{method}/" + file_name))



    def make_plot(self,models,methods,file_name,param_label,equil):
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
                    df = self.get_data(model_type,method,equil,file_name)

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
                
                
                except (IOError, OSError):  #skip to next available data if file not found
                    pass

        #add panel labels
        mom_var_plot.text(x= 0.05, y = 0.85, s="(a)",transform=mom_var_plot.transAxes,fontsize=self.fontsizetitles)
        pos_var_plot.text(x= 0.05, y = 0.85, s="(b)",transform=pos_var_plot.transAxes,fontsize=self.fontsizetitles)
        xcorr_plot.text(x= 0.05, y = 0.85, s="(c)",transform=xcorr_plot.transAxes,fontsize=self.fontsizetitles)
        kappa_plot.text(x= 0.05*(2/3), y = 0.85, s="(d)",transform=kappa_plot.transAxes,fontsize=self.fontsizetitles)
        lambda_plot.text(x= 0.05*(2/3), y = 0.85 , s="(e)",transform=lambda_plot.transAxes,fontsize=self.fontsizetitles)

        #add legend
        kappa_plot.legend(fontsize=self.fontsizeticks,loc="lower center",frameon=False)

        plt.figtext(0.5, 0.01, param_label, ha="center", fontsize=self.fontsizetitles, bbox={"facecolor":"orange", "alpha":0.5, "pad":5})

        return fig
    
    def b(self,y4,model_type,Lambda,g):
        if model_type=="harmonic":
            return (y4*(Lambda**2))/(2*g)
        elif model_type=="log":
            return (g/(y4+1e-10))*(np.sqrt((1+(Lambda*y4/g)**2))-1)
        else:
            return 0
            

    def get_Vfun(self,df,Lambda,g,model_type):
        try:
            y4 = df.y4.to_numpy()
            lambda_vec = self.b(y4,model_type,Lambda,g)
        except AttributeError:
            lambda_vec = np.gradient(df.kappa.to_numpy(),df.t.to_numpy())

        if model_type=="harmonic":
            return (lambda_vec/Lambda)**2
        elif model_type=="hard":
            return 0
        elif model_type=="log":
            return np.where(np.abs(lambda_vec)<Lambda, -np.log(1-(lambda_vec/Lambda)**2),1e10)
        elif model_type=="control":
            return df.kappa.to_numpy()*(df.kappa.to_numpy()*df.x1.to_numpy()-1) 
        else:
            return 
