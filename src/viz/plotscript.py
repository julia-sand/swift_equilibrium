import string
import os

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec

import pdb 

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
        

    def plot_func(self,ax,x,y,legendlabel,linestyle="solid"):
        """Simple plot and formatting to plot one line of data. Used for plotting
        Hamiltonian and running cost
        """

        ax.plot(x, y, lw = self.lw, label = legendlabel,linestyle=linestyle)
    
    def format_ax(self,ax,ylabel,Tf):
        ax.set_ylabel(ylabel,fontsize=self.fontsizetitles)
        ax.set_xlabel('t',fontsize=self.fontsizetitles)
        ax.tick_params(labelsize=self.fontsizeticks)
        ax.set_xlim((-0.01,Tf+0.01))

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

    def get_T(self,file_name):
        params = self.get_params(file_name)

        return self.get_param_value(params[0])


    def get_data(self,model_type,method,equil,file_name):
        
        """
        function which gets the filepath of model and method 
        
        Returns a dataframe if the data is available. 
        """
        #currloc = 
        folder_path =os.path.dirname( __file__ )+f"/../../results/{model_type}/"
        
        #add equilibrium
        if equil:
            folder_path = folder_path + "equil/"
        else: 
            folder_path = folder_path + "noneq/"
        #print(folder_path+ f"{method}/" + file_name)

        return pd.DataFrame(pd.read_csv(folder_path + f"{method}/" + file_name))

    def get_legend_label(self,model_type,method,param_label):

        if model_type=="hard": #overwrite legend label
            legendlabel = f"compact, {method}" 
        else:
            legendlabel = f"{model_type}, {method}" 

        if param_label is not None:
            legendlabel = legendlabel+f"; {param_label}"
        
        return legendlabel

    def plot_func_cumulants(self,ax,x,y,ylabel,model_type,method,param_label):
        
        legendlabel = self.get_legend_label(model_type,method,param_label)
        if method =="direct":
            ax.plot(x, y, label = legendlabel,lw=self.lw)
        else: 
            ax.plot(x, y, label = legendlabel,lw=self.lw,linestyle="dashed",zorder=100)
        ax.set_ylabel(ylabel,fontsize=self.fontsizetitles)
        ax.set_xlabel('t',fontsize=self.fontsizetitles)
        ax.tick_params(labelsize=self.fontsizeticks)
        ax.set_xlim((-0.1,3.1))

    def format_subplot(self,params_dict):
        self.plot_func_cumulants(params_dict["subplot"],
                                    params_dict["tseries"], 
                                    params_dict["xseries"],
                                    params_dict["ylabel"],
                                    params_dict["model_type"],
                                    params_dict["method"],
                                    params_dict["paramlabel"])
        params_dict["subplot"].text(x=params_dict["xloc"], 
                                    y=params_dict["yloc"], 
                                    s=params_dict["letter_label"],
                                    transform=params_dict["subplot"].transAxes,
                                    fontsize=self.fontsizetitles)

    def make_fig(self):
        fig = plt.figure(figsize=(15, 8))#, constrained_layout=True)
        return fig

    def make_gridspec(self,fig):

        # figure setup
        #gs_cumulants = gridspec.GridSpec(2, 6, 
        gs_cumulants = fig.add_gridspec(2, 6, 
                            width_ratios=[1, 1, 1, 1,1,1], 
                            height_ratios=[1, 1],
                            hspace=0.4,
                            wspace=1.2)        
        
        return gs_cumulants


    def plot_all_cumulants(self,fig,gs_cumulants,models,methods,file_names,equil):
        """
        Plots the data of specified parameters (via the filename) and returns matplotlib figure.
        """
    
        for file_name in file_names:
            param_label = self.make_paramlabel(file_name)
            #pdb.set_trace()
            for model_type in models:
                for method in methods:
                    #legendlabel=f"{model_type}, {method}"

                    try:   
                        df = self.get_data(model_type,method,equil,file_name)

                        
                        plot_params_all = dict(xloc = 0.05,
                                                yloc= 0.85,
                                                tseries= df.t.to_numpy(),
                                                model_type=model_type,
                                                method=method,
                                                paramlabel= param_label)

                        pos_var_dict = plot_params_all.copy()
                        pos_var_dict.update(dict(subplot=plt.subplot(gs_cumulants[0, 2:4]),
                                                                xseries= df.x1.to_numpy(),
                                                                letter_label="(b)",
                                                                ylabel='Position Variance'))
                        mom_var_dict = plot_params_all.copy()
                        mom_var_dict.update(dict(subplot=plt.subplot(gs_cumulants[0, 0:2]),
                                                                xseries= df.x3.to_numpy(),
                                                                letter_label="(a)",
                                                                ylabel='Mom. Variance'))
                        x_corr_dict = plot_params_all.copy()
                        x_corr_dict.update(dict(subplot=plt.subplot(gs_cumulants[0, 4:]),
                                                                xseries= df.x2.to_numpy(),
                                                                letter_label="(c)",
                                                                ylabel='Cross Correlation'))
                        kappa_dict = plot_params_all.copy()
                        kappa_dict.update(dict(subplot=plt.subplot(gs_cumulants[1,:3]),
                                                                xseries= df["kappa"].to_numpy(),
                                                                letter_label="(d)",
                                                                ylabel=r'Stiffness, $\kappa_t$',
                                                                xloc=0.05*(2/3)))
                        lambda_dict = plot_params_all.copy()
                        lambda_dict.update(dict(subplot=plt.subplot(gs_cumulants[1, 3:]),
                                                                xseries= np.gradient(df["kappa"].to_numpy(),df.t.to_numpy()),
                                                                letter_label="(e)",
                                                                ylabel=r'Control, $\lambda_t$',
                                                                xloc=0.05*(2/3)))

                        self.format_subplot(pos_var_dict)
                        self.format_subplot(mom_var_dict)
                        self.format_subplot(x_corr_dict)
                        self.format_subplot(kappa_dict)
                        self.format_subplot(lambda_dict)

                    except FileNotFoundError:
                        pass     
            
        #add legend
        plt.subplot(gs_cumulants[1, 3:]).legend(fontsize=self.fontsizeticks,loc="lower center",frameon=False)

        #plt.figtext(0.5, 0.01, param_label, ha="center", fontsize=self.fontsizetitles, bbox={"facecolor":"orange", "alpha":0.5, "pad":5})

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
    
    def compute_entropy_production(self,df,Lambda,g,model_type):
        return df.x3.to_numpy()+g*self.get_Vfun(df,Lambda,g,model_type)
      
    def compute_work(self,df,Lambda,g,model_type):
        
        return df.kappa.to_numpy()[-1]*df.x1.to_numpy()[-1] + self.compute_entropy_production(self,df,Lambda,g,model_type)

    
    def get_work_from_ep(self,df,ep):
        
        return df.kappa.to_numpy()[-1]*df.x1.to_numpy()[-1] + ep