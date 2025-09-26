import string
import os

import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from scipy.ndimage import generic_filter
import scipy.ndimage as sc

"""
This file contains all the utility and plotting functions to make the plots that 
present our results

""" 

def update_mpl():
    """
    Sets default parameters for any matplotlib plotting formatting
    """

    #update matplotlib config
    mpl.rcParams['lines.linewidth'] = 3
    mpl.rcParams['xtick.labelsize'] = 18
    mpl.rcParams['ytick.labelsize'] = 18
    mpl.rcParams['font.size'] = 22
    mpl.rcParams['axes.labelsize'] = 22
    mpl.rcParams['legend.fontsize'] = 22

class PlotParams():
    def __init__(self):
        
        update_mpl()

        self.lw = 3
        
        self.c1 = "#1f77b4" #darkblue, DIRECT
        self.c2 = '#ff7f0e' #orange, INDIRECT
        self.c3 = '#2ca02c' #green SLOWFAST


    def plot_func(self,ax,x,y,legendlabel,linestyle="solid"):
        """Simple plot and formatting to plot one line of data. Used for plotting
        Hamiltonian and running cost
        """

        ax.plot(x, y, lw = self.lw, 
                label = legendlabel,
                linestyle=linestyle)
    
    def format_ax_plain(self,ax):
        """
        Adds x axis label and formats axis ticks
        """
        
        ax.set_xlabel(r'$t_f$',labelpad=-3)
        #ax.tick_params(labelsize=self.fontsizeticks)

    def format_ax(self,ax,ylabel,Tf,ti=0):
        """
        Formats x axis

        Args:
            ax : artist
                axis to apply formatting
            ylabel : str 
                text for y axis label
            Tf : float
                final time to set x axis limit
        """
        
        
        ax.set_xlabel(r'$t_f$')#,fontsize=self.fontsizetitles)
        #ax.tick_params(labelsize=self.fontsizeticks)
        ax.set_xlim((-0.5+ti,Tf+0.5))

    def filter_(self,x,filter_delta = 50):
        """Convenient function to apply a simple smoothing filter to
        a series of data
        """
        
        return generic_filter(x,sc.mean,filter_delta,mode = "nearest")
    
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
        """
        Creates the parameter label to add to the base of the plots. 
        Parameters are taken from the file name of the run. 
        """

        #read params from filename? 
        params = self.get_params(file_name)

        param_label = rf"$T={self.get_param_value(params[0])}; \Lambda={self.get_param_value(params[1])}; \varepsilon={self.get_param_value(params[2])}; g={self.get_param_value(params[3])}$"

        return param_label        
    
    def get_g(self,file_name):
        params = self.get_params(file_name)

        return self.get_param_value(params[3])

    def get_Lambda(self,file_name):
        params = self.get_params(file_name)
        lambdatemp = self.get_param_value(params[1])
        if lambdatemp == 1.4:
            lambdatemp = np.sqrt(2)

        return lambdatemp

    def get_T(self,file_name):
        params = self.get_params(file_name)

        return self.get_param_value(params[0])


    def get_data(self,model_type,method,equil,file_name,constrained_kappa):
        """
        function which gets the filepath of model and method 
        
        Returns a dataframe if the data is available. 
        """

        #currloc = 
        folder_path = os.path.dirname( __file__ )+f"/../../results/{model_type}/"+ f"{equil}/"+ f"{method}/"
        
        if constrained_kappa=="constrained_kappa":
            folder_path = folder_path + "constrained_kappa/"
        elif constrained_kappa=="negative_constrained_kappa":
            folder_path = folder_path + "negative_constrained_kappa/"
        elif constrained_kappa=="negative_constrained_kappa_small":
            folder_path = folder_path + "negative_constrained_kappa_small/"
        elif constrained_kappa=="contract":
            folder_path = folder_path + "contract/"
        else:
            pass

        return pd.DataFrame(pd.read_csv(folder_path + file_name))

    def get_legend_label(self,model_type,method,
                            param_label, file_name):
        
         
        if method == "slowfast":
            gtemp = self.get_g(file_name)
            legendlabel = f"centre manifold (g = {gtemp})" #legendlabel+f" (g = {gtemp})"
        elif method == "indirect":
            legendlabel = "first order solution"
        elif method == "direct":
            legendlabel = f"direct optimisation"

        return legendlabel

    def plot_func_cumulants(self,ax,x,y,model_type,method,param_label,file_name,equil
                                ,c_ind,label_ind):
        
        legendlabel = self.get_legend_label(model_type,method,param_label,file_name)
        if method =="direct":
            if (equil=="stiffness_control" and label_ind==1):
                #Stiffness as a control 
                ax.plot(x,self.filter_(y), label = "stiffness as a control",
                                        lw=self.lw,color=self.c2)
            elif (equil=="stiffness_control" and label_ind!=1):
                pass
            
            elif label_ind!=1:
                lambda_temp = self.get_Lambda(file_name)
                col = self.c1 if lambda_temp==1 else self.c3
                ax.plot(x, self.filter_(y), label="stiffness as a state"+ r" ($\Lambda =$"+ f"{lambda_temp})",lw=self.lw,zorder=100,color=col)
                #label = legendlabel + r" ($\Lambda =$"+ f"{lambda_temp})"
            
            else:
                    
                if c_ind==3:
                    ax.plot(x, self.filter_(y), label = legendlabel,lw=self.lw,zorder=100,color=self.c3)
                    #+r"($\Lambda=10$)"
                else:
                
                    ax.plot(x, self.filter_(y), label = legendlabel,lw=self.lw,zorder=100,color=self.c1)

                #ax.plot(x,self.filter_(y), label = legendlabel,lw=self.lw,color=self.c1)
        elif method =="indirect": 
            ax.plot(x, y, label = legendlabel,lw=self.lw,linestyle="dashed",
                    zorder=300,color=self.c2)
           
        elif method =="slowfast": 

            if c_ind==2:
                ax.plot(x, y, label = legendlabel,lw=self.lw,linestyle="dotted",zorder=1000,color=self.c3)
            else:
                ax.plot(x, y, label = legendlabel,lw=self.lw,linestyle="dotted",zorder=100,color="m")

    def format_subplot(self,params_dict,label_ind,c_ind):
        
        try:
            self.plot_func_cumulants(params_dict["subplot"],
                                        params_dict["tseries"], 
                                        params_dict["xseries"],
                                        params_dict["model_type"],
                                        params_dict["method"],
                                        params_dict["paramlabel"],
                                        params_dict["file_name"],
                                        params_dict["equil"],c_ind,label_ind)
            
            
        except AttributeError:
                    pass
    def make_fig(self):
        fig = plt.figure(figsize=(15, 8))#, constrained_layout=True)
        return fig

    def make_gridspec(self,fig,hspace=0.3):

        # figure setup
        #gs_cumulants = gridspec.GridSpec(2, 6, 
        gs_cumulants = fig.add_gridspec(2, 6, 
                            width_ratios=[1, 1, 1, 1,1,1], 
                            height_ratios=[1, 1],
                            hspace=hspace,
                            wspace=1.2)        
        
        return gs_cumulants


    def make_cumulant_dictionary(self,base_dict,update_params):
        dict_temp = base_dict.copy()

        dict_temp.update(update_params)
        return dict_temp


    def plot_all_cumulants(self,fig,gs_cumulants,models,methods,file_names,equil,constrained_kappa):
        """
        Plots the data of specified parameters (via the filename) and returns matplotlib figure.
        """

        label_ind = 1
        c_ind = 1
        for eq in equil:
            for file_name in file_names:
                
                param_label = self.make_paramlabel(file_name)
                xmax = 0
                #pdb.set_trace()
                for model_type in models:
                    for method in methods:
                        #legendlabel=f"{model_type}, {method}"

                        try:   
                            df = self.get_data(model_type,method,eq,file_name,constrained_kappa)

                            #use stiffness as a control in the plot for all values
                            if "stiffness_control" in equil:
                                eq_temp = "stiffness_control"
                            else:
                                eq_temp = eq
                            if "slowfast" in methods:
                                c_temp = "slowfast"
                            else:
                                c_temp = "0"
                    
                            plot_params_all = dict(tseries= df.t.to_numpy(),
                                                    model_type=model_type,
                                                    method=method,
                                                    paramlabel= param_label,
                                                    equil=eq,
                                                    file_name=file_name)
                            posvardict = self.make_cumulant_dictionary(plot_params_all,dict(subplot=plt.subplot(gs_cumulants[0, 2:4]) if eq_temp!="stiffness_control" else plt.subplot(gs_cumulants[0,3:]),
                                                                                            xseries= df.x1.to_numpy()))
                            self.format_subplot(posvardict,label_ind,c_ind)
                            momvardict = self.make_cumulant_dictionary(plot_params_all,dict(subplot=plt.subplot(gs_cumulants[0, 0:2]) if eq_temp!="stiffness_control" else plt.subplot(gs_cumulants[0,:3]),
                                                                    xseries= df.x3.to_numpy()))
                            self.format_subplot(momvardict,label_ind,c_ind)
                            xcordict = self.make_cumulant_dictionary(plot_params_all,dict(subplot=plt.subplot(gs_cumulants[0, 4:]) if eq_temp!="stiffness_control" else plt.subplot(gs_cumulants[1,:3]),
                                                                    xseries= df.x2.to_numpy()))
                            self.format_subplot(xcordict,label_ind,c_ind)
                            stiffnessdict = self.make_cumulant_dictionary(plot_params_all,dict(subplot=plt.subplot(gs_cumulants[1,:3]) if eq_temp!="stiffness_control" else plt.subplot(gs_cumulants[1,3:]),
                                                                    tseries = df.t.to_numpy(),
                                                                    xseries= df.kappa.to_numpy()))
                            self.format_subplot(stiffnessdict,label_ind,c_ind)
                            if (method =="direct" or (model_type=="control" and eq==False)):
                                lambda_series = np.gradient(df["kappa"].to_numpy(),df.t.to_numpy())
                            
                            elif method =="slowfast":
                            
                                lambda_series = self.b(df.f1,model_type,self.get_Lambda(file_name),self.get_g(file_name))

                            else:
                            
                                lambda_series = self.b(df.y4,model_type,self.get_Lambda(file_name),self.get_g(file_name))

                            lambdadict = self.make_cumulant_dictionary(plot_params_all,dict(subplot=plt.subplot(gs_cumulants[1, 3:]) if eq_temp!="stiffness_control" else None,
                                                                    xseries= lambda_series))
                                                                    
                            self.format_subplot(lambdadict,label_ind,c_ind)
                            #c_ind += 1
                            if c_temp =="slowfast":
                                c_ind += 1

                            if eq_temp == "stiffness_control":    
                                label_ind += 1
                            
                            #get max time for x axis adjusting
                            xmax = df.t.max() 
                        except FileNotFoundError:
                            pass     
                        
        plt.subplots_adjust(wspace=0.5)
        xloc = 0.02 if eq_temp!="stiffness_control" else (2/3)*0.02
        yloc= 0.88
        #xmax = 5
                                                    
        if eq_temp!="stiffness_control":
            self.add_labels(plt.subplot(gs_cumulants[0,0:2]),xmax,"(a)",xloc,yloc,"Mom. Variance")
            self.add_labels(plt.subplot(gs_cumulants[0,2:4]),xmax,"(b)",xloc,yloc,"Position Variance")
            self.add_labels(plt.subplot(gs_cumulants[0,4:]),xmax,"(c)",xloc,yloc,"Cross Correlation")
            self.add_labels(plt.subplot(gs_cumulants[1,:3]),xmax,"(d)",xloc*(2/3),yloc,r"Stiffness, $\mathscr{k}_t$")
            self.add_labels(plt.subplot(gs_cumulants[1,3:]),xmax,"(e)",xloc*(2/3),yloc,r"Control, $\lambda_t$")
        else: 
            self.add_labels(plt.subplot(gs_cumulants[0,:3]),xmax,"(a)",xloc*(2/3),yloc,"Mom. Variance")
            self.add_labels(plt.subplot(gs_cumulants[0,3:]),xmax,"(b)",xloc*(2/3),yloc,"Position Variance")
            self.add_labels(plt.subplot(gs_cumulants[1,:3]),xmax,"(c)",xloc*(2/3),yloc,"Cross Correlation")
            self.add_labels(plt.subplot(gs_cumulants[1,3:]),xmax,"(d)",xloc*(2/3),yloc,r"Stiffness, $\mathscr{k}_t$")

        return fig
  
    def add_labels(self,ax,xmax,letter_label,xloc,yloc,ylabel):

        #add axis labels 
        ax.text(x=xloc, 
                    y=yloc, 
                    s=letter_label,
                    transform=ax.transAxes,
                    fontweight="bold",
                    zorder=10000)
        ax.set_ylabel(ylabel)#,fontsize=self.fontsizetitles)
        ax.set_xlabel('t')#,fontsize=self.fontsizetitles)
        #ax.tick_params(labelsize=self.fontsizeticks)
        ax.set_xlim((-0.1,xmax+0.1))


    def integrator(self,y,x,dx=0.001):
        #
        ti = np.min(x) 
        tf = np.max(x)
        nsteps = int(np.ceil(tf/dx)) #number of steps in equally spaced discretisations

        t_axis = np.linspace(ti,tf,nsteps)
        
        #get y data
        interp_y = np.interp(t_axis,x,y)
        return np.trapz(y,x)#np.trapz(interp_y,t_axis)

    def b(self,y4,model_type,Lambda,g):
        if model_type=="harmonic":
            return y4/g #(y4*(Lambda**2))/(2*g)
        elif model_type=="log":
            return (g/(y4+1e-10))*(np.sqrt((1+(Lambda*y4/g)**2))-1)
        else:
            return y4/g #default as harmonic
            

    def get_Vfun(self,df,Lambda,g,model_type):
        try:
            y4 = df.y4.to_numpy()
            lambda_vec = self.b(y4,model_type,Lambda,g)
        except AttributeError: #when y4 cannot be found (eg direct method or stiffness as a control)
            lambda_vec = np.gradient(df.kappa.to_numpy(),df.t.to_numpy())

        if model_type=="harmonic":
            return (1/2)*(lambda_vec**2) #(lambda_vec/Lambda)**2
        elif model_type=="hard":
            return np.zeros_like(lambda_vec)
        elif model_type=="log":
            return np.where(np.abs(lambda_vec)<Lambda, -np.log(1-(lambda_vec/Lambda)**2),1e10)
        elif model_type=="control":
            return (1/2)*(lambda_vec**2) #default to control penalty
        else:
            return 

    def control_penalty_S(self,df):
        return (df.kappa.to_numpy()*df.x1.to_numpy()-1)**2
        #df.kappa.to_numpy()*(df.kappa.to_numpy()*df.x1.to_numpy()-1) 

    def compute_heat(self,df):
        """
        See Eq. (11).
        Q_T
        """
        
        return self.integrator(df.x3.to_numpy(),df.t.to_numpy()) - df.t.to_numpy()[-1]  
    
    def compute_work(self,df):
        """
        See Eq. (10)
        W_T
        """

        term1 = 0.5*(df.kappa.to_numpy()[-1]*df.x1.to_numpy()[-1] - df.kappa.to_numpy()[0]*df.x1.to_numpy()[0])
        return term1 + self.compute_heat(df) 

    

    def gibbs_shannon_entropy(self,mom,pos):
        """
        See Eq. (12)
        """

        return 0#np.log()
    
    def compute_entropy_production(self,df):
        """
        See Eq. (12)
        """

        term1 = 0.5*np.log(df.x1.to_numpy()[-1]/df.x1.to_numpy()[0])
        return term1 + self.compute_heat(df) 


    def compute_cost(self,df,g,Lambda,model_type):
        """
        This is C_T
        """

        alpha = 0.1 if model_type=="control" else 0  
        V = np.trapz(self.get_Vfun(df,Lambda,g,model_type),df.t.to_numpy()) 
        S = np.trapz(self.control_penalty_S(df),df.t.to_numpy())
        
        return self.compute_work(df) + g*V + alpha*S


    def reconstruct_kappa(self,t,x1,x2,x3):
        """
        This function returns an approximation for kappa given the cumulants, using the dynamical equation for cross-corellation
        """

        epsilon = 1 

        x2dot = np.gradient(x2,t)

        return (x2dot + self.filter_(x2) - epsilon*self.filter_(x3))/(-epsilon*self.filter_(x1))
