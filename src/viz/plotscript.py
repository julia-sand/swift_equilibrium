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
    mpl.rcParams['font.size'] = 20
    mpl.rcParams['axes.labelsize'] = 20
    mpl.rcParams['legend.fontsize'] = 20

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

    def filter_(self,x,filter_delta = None):
        """Convenient function to apply a simple smoothing filter to
        a series of data
        """

        if filter_delta is None:
            return x 
        else:
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
            legendlabel = "solution of first order conditions"
        elif method == "direct":
            legendlabel = f"direct optimisation"

        return legendlabel

    def g_color(self,g):
        if g==0.01:
            return self.c2#"brown"
        elif g==0.001:
            return self.c3
        else: 
            return "m"#"brown"

    def plot_func_cumulants(self,ax,xseries,c_ind,label_ind,filter_delta,**params_dict):
                                               
        
        legendlabel = self.get_legend_label(params_dict["model_type"],params_dict["method"],params_dict["paramlabel"],params_dict["file_name"])
        if params_dict["method"] =="direct":
            if params_dict["equil"]=="stiffness_control":
                #Stiffness as a control 
                ax.plot(params_dict["tseries"],self.filter_(xseries,filter_delta), label = "stiffness as a control",
                                        lw=self.lw,color=self.c2)
            #elif (params_dict["equil"]=="stiffness_control" and label_ind!=1):
            #    pass
            
            elif label_ind>1:
                lambda_temp = self.get_Lambda(params_dict["file_name"])
                col = self.c1 if lambda_temp==1 else self.c3
                ax.plot(params_dict["tseries"], self.filter_(xseries,filter_delta), label="stiffness as a state"+ r" ($\Lambda =$"+ f"{lambda_temp})",lw=self.lw,zorder=100,color=col)
                #label = legendlabel + r" ($\Lambda =$"+ f"{lambda_temp})"
            
            else:
                    
                ax.plot(params_dict["tseries"], self.filter_(xseries,filter_delta), label = legendlabel,lw=self.lw,zorder=100,color=self.c1)

                #ax.plot(x,self.filter_(y), label = legendlabel,lw=self.lw,color=self.c1)
        elif params_dict["method"] =="indirect": 
            
            ax.plot(params_dict["tseries"], self.filter_(xseries,filter_delta), label = legendlabel,lw=self.lw,linestyle="dashed",
                    zorder=300,color=self.c2)
           
        elif params_dict["method"] =="slowfast": 
                
            ax.plot(params_dict["tseries"], self.filter_(xseries,filter_delta), label = legendlabel,lw=self.lw,zorder=100000,linestyle="dashed",color=self.g_color(self.get_g(params_dict["file_name"])))
            
    def format_subplot(self,ax,xseries,label_ind,c_ind,filter_delta,**params_dict):
        
        try:
            self.plot_func_cumulants(ax,xseries,c_ind,label_ind,filter_delta,**params_dict)
            
            
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
        xmax = 0

        for eq in equil:
            for file_name in file_names:
                
                param_label = self.make_paramlabel(file_name)
                #pdb.set_trace()
                for model_type in models:
                    for method in methods:
                        #legendlabel=f"{model_type}, {method}"

                        try:   
                            df = self.get_data(model_type,method,eq,file_name,constrained_kappa)

                            #use stiffness as a control in the plot for all values
                            if "stiffness_control" in equil:
                                eq_temp = "stiffness_control"
                                filter_delta=50
                                label_ind += 1
                            else:
                                eq_temp = eq
                                filter_delta=None
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

                            ax =plt.subplot(gs_cumulants[0, 2:4]) if eq_temp!="stiffness_control" else plt.subplot(gs_cumulants[0,3:])
                            self.format_subplot(ax,df.x1.to_numpy(),label_ind,c_ind,filter_delta,**plot_params_all)
                            ax=plt.subplot(gs_cumulants[0, 0:2]) if eq_temp!="stiffness_control" else plt.subplot(gs_cumulants[0,:3])
                            self.format_subplot(ax,df.x3.to_numpy(),label_ind,c_ind,filter_delta,**plot_params_all)
                            ax=plt.subplot(gs_cumulants[0, 4:]) if eq_temp!="stiffness_control" else plt.subplot(gs_cumulants[1,:3])
                            self.format_subplot(ax,df.x2.to_numpy(),label_ind,c_ind,filter_delta,**plot_params_all)
                            ax=plt.subplot(gs_cumulants[1,:3]) if eq_temp!="stiffness_control" else plt.subplot(gs_cumulants[1,3:])
                            self.format_subplot(ax,df.kappa.to_numpy(),label_ind,c_ind,filter_delta,**plot_params_all)
                            
                            
                            if (method =="direct" or (model_type=="control" and eq==False)):
                                lambda_series = np.gradient(df["kappa"].to_numpy(),df.t.to_numpy())
                            
                            elif method =="slowfast":
                            
                                lambda_series = self.get_slowfast_y4(df,self.get_g(file_name))
                           
                            else:
                            
                                lambda_series = self.b(df.y4,model_type,self.get_Lambda(file_name),self.get_g(file_name))

                            ax = plt.subplot(gs_cumulants[1, 3:]) if eq_temp!="stiffness_control" else None                                      
                            self.format_subplot(ax,lambda_series,label_ind,c_ind,filter_delta,**plot_params_all)
                            #c_ind += 1
                            if method =="slowfast":
                                c_ind += 1
                           
                            #get max time for x axis adjusting
                            xmax = np.maximum(xmax, df.t.max())

                        except FileNotFoundError:
                            pass
                                                
        plt.subplots_adjust(wspace=0.5)
        xloc = 0.02 if eq_temp!="stiffness_control" else (2/3)*0.02
        yloc= 0.88
                                                    
        if eq_temp!="stiffness_control":
            self.add_labels(plt.subplot(gs_cumulants[0,0:2]),xmax,"(a)",xloc,yloc,r"Mom. Variance, $\mathscr{x}_t^{(3)}$") #mom variance 
            self.add_labels(plt.subplot(gs_cumulants[0,2:4]),xmax,"(b)",xloc,yloc,r"Pos. Variance, $\mathscr{x}_t^{(1)}$") #pos variance
            self.add_labels(plt.subplot(gs_cumulants[0,4:]),xmax,"(c)",xloc,yloc,r"Cross Corr., $\mathscr{x}_t^{(2)}$") #x correlation
            self.add_labels(plt.subplot(gs_cumulants[1,:3]),xmax,"(d)",xloc*(2/3),yloc,r"Stiffness, $\mathscr{k}_t$") #stiffness
            self.add_labels(plt.subplot(gs_cumulants[1,3:]),xmax,"(e)",xloc*(2/3),yloc,r"Control, $\lambda_t$") #control , lambda
        else: 
            self.add_labels(plt.subplot(gs_cumulants[0,:3]),xmax,"(a)",xloc*(2/3),yloc,r"Mom. Variance, $\mathscr{x}_t^{(3)}$") #mom variance
            self.add_labels(plt.subplot(gs_cumulants[0,3:]),xmax,"(b)",xloc*(2/3),yloc,r"Pos. Variance, $\mathscr{x}_t^{(1)}$") #pos variance
            self.add_labels(plt.subplot(gs_cumulants[1,:3]),xmax,"(c)",xloc*(2/3),yloc,r"Cross Corr., $\mathscr{x}_t^{(2)}$") #x correlation
            self.add_labels(plt.subplot(gs_cumulants[1,3:]),xmax,"(d)",xloc*(2/3),yloc,r"Stiffness, $\mathscr{k}_t$") #stiffness

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
        ax.set_xlabel('t')
        ax.set_xlim((-0.1,xmax+0.1))

    def get_slowfast_y4(self,df,g):
        eps = 1
        f00 = 2*eps*df.x2*(4*eps*df.x3-5*df.x2) + df.x1*(9*eps*df.x3-3*df.x2-6*eps)-3*eps*(df.x1**2)*df.kappa-(8*(eps**2)*(df.x2**3)/df.x1)
        phi10 = -f00/(eps*(df.x1**2))
        phi11 = 0
        return (df.f1 + phi10)#-np.gradient(df["kappa"].to_numpy(),df.t.to_numpy())
        #)#-np.gradient(df["kappa"].to_numpy(),df.t.to_numpy())
        #df.f1 + phi10 #phi10 + g*phi11

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
