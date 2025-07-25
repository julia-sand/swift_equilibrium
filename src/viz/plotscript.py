import string
import os

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
        self.fontsizetitles = 20

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
        ax.set_xlabel(r'$t_f$',fontsize=self.fontsizetitles)
        ax.tick_params(labelsize=self.fontsizeticks)

    def format_ax(self,ax,ylabel,Tf):
        ax.set_ylabel(ylabel,fontsize=self.fontsizetitles)
        ax.set_xlabel(r'$t_f$',fontsize=self.fontsizetitles)
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

        return self.get_param_value(params[3])

    def get_Lambda(self,file_name):
        params = self.get_params(file_name)
        lambdatemp = self.get_param_value(params[1])
        if lambdatemp ==1.4:
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
        folder_path = os.path.dirname( __file__ )+f"/../../results/{model_type}/"
        
        #add equilibrium
        if equil=="equil":
            folder_path = folder_path + "equil/"
        elif equil=="noneq": 
            folder_path = folder_path + "noneq/"
        else:
            folder_path = folder_path + "stiffness_control/"
        #print(folder_path+ f"{method}/" + file_name)

        if constrained_kappa=="constrained_kappa":
            folder_path = folder_path + f"{method}/" + "constrained_kappa/"
        elif constrained_kappa=="negative_constrained_kappa":
            folder_path = folder_path + f"{method}/" + "negative_constrained_kappa/"
        else:
            folder_path = folder_path + f"{method}/"

        return pd.DataFrame(pd.read_csv(folder_path + file_name))

    def get_legend_label(self,model_type,method,
                            param_label, file_name):

        #if model_type=="hard": #overwrite legend label
        #    legendlabel = f"compact, {method}" 
        #else:
        #    legendlabel = f"{model_type}, {method}" 

        #if param_label is not None:
        #    legendlabel = legendlabel+f"; {param_label}"
        
        legendlabel = f"{method}" 
        if method == "slowfast":
            gtemp = self.get_g(file_name)
            legendlabel = legendlabel+f" (g = {gtemp})"

        return legendlabel

    def plot_func_cumulants(self,ax,x,y,ylabel,model_type,method,param_label,file_name
                                ,c_ind):
        
        legendlabel = self.get_legend_label(model_type,method,param_label,file_name)
        if method =="direct":
            ax.plot(x[2:-2], y[2:-2], label = legendlabel,lw=self.lw,color=self.c1)
        elif method =="indirect": 
            ax.plot(x, y, label = legendlabel,lw=self.lw,linestyle="dashed",zorder=100,color=self.c2)
        elif method =="slowfast": 

            if c_ind==2:
                ax.plot(x, y, label = legendlabel,lw=self.lw,linestyle="dotted",zorder=100,color=self.c3)
            else:
                ax.plot(x, y, label = legendlabel,lw=self.lw,linestyle="dotted",zorder=100,color="red")
        ax.set_ylabel(ylabel,fontsize=self.fontsizetitles)
        ax.set_xlabel('t',fontsize=self.fontsizetitles)
        ax.tick_params(labelsize=self.fontsizeticks)
        ax.set_xlim((-0.1,x[-1]+0.1))

    def plot_func_cumulants_control(self,ax,x,y,ylabel,
                                    method,equil):
        
        #legendlabel = self.get_legend_label(model_type,method,param_label)
        if method =="direct":
            ax.plot(x[2:-2], y[2:-2], label = "direct",lw=self.lw,color=self.c1)
        elif (method =="indirect" and equil=="noneq"): 
            ax.plot(x, y, label = "indirect",lw=self.lw,linestyle="dashed",zorder=100,color=self.c2)
        elif (method =="indirect" and equil == "equil"): 
            ax.plot(x, y, label = "equilibration",lw=self.lw,linestyle="dotted",zorder=100,color=self.c3)
            #ax.plot(x, y,lw=self.lw,zorder=50,color="gray",alpha=0.5)
        ax.set_ylabel(ylabel,fontsize=self.fontsizetitles)
        ax.set_xlabel('t',fontsize=self.fontsizetitles)
        ax.tick_params(labelsize=self.fontsizeticks)
        ax.set_xlim((-0.1,x[-1]+0.1))

    def format_subplot(self,params_dict,label_ind,c_ind):
        

        if params_dict["model_type"]=="control":
            self.plot_func_cumulants_control(params_dict["subplot"],
                                    params_dict["tseries"], 
                                    params_dict["xseries"],
                                    params_dict["ylabel"],
                                    params_dict["method"],
                                    params_dict["equil"])
        else:
            self.plot_func_cumulants(params_dict["subplot"],
                                    params_dict["tseries"], 
                                    params_dict["xseries"],
                                    params_dict["ylabel"],
                                    params_dict["model_type"],
                                    params_dict["method"],
                                    params_dict["paramlabel"],
                                    params_dict["file_name"],c_ind)

        if label_ind:         
            params_dict["subplot"].text(x=params_dict["xloc"], 
                                        y=params_dict["yloc"], 
                                        s=params_dict["letter_label"],
                                        transform=params_dict["subplot"].transAxes,
                                        fontsize=self.fontsizetitles,
                                        fontweight="bold",
                                        zorder=10000)

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


    def make_cumulant_dictionary(self,base_dict,update_params):
        dict_temp = base_dict.copy()

        dict_temp.update(update_params)
        return dict_temp


    def plot_all_cumulants(self,fig,gs_cumulants,models,methods,file_names,equil,constrained_kappa):
        """
        Plots the data of specified parameters (via the filename) and returns matplotlib figure.
        """
        label_ind = True
        c_ind = 1
        for file_name in file_names:
            

            param_label = self.make_paramlabel(file_name)
            #pdb.set_trace()
            for model_type in models:
                for method in methods:
                    #legendlabel=f"{model_type}, {method}"

                    try:   
                        df = self.get_data(model_type,method,equil,file_name,constrained_kappa)
                       
                        plot_params_all = dict(xloc = 0.05,
                                                yloc= 0.85,
                                                tseries= df.t.to_numpy(),
                                                model_type=model_type,
                                                method=method,
                                                paramlabel= param_label,
                                                equil=equil,
                                                file_name=file_name)

                        self.format_subplot(self.make_cumulant_dictionary(plot_params_all,dict(subplot=plt.subplot(gs_cumulants[0, 2:4]),
                                                                                        xseries= df.x1.to_numpy(),
                                                                                        letter_label="(b)",
                                                                                        ylabel='Position Variance')),label_ind,c_ind)
                        self.format_subplot(self.make_cumulant_dictionary(plot_params_all,dict(subplot=plt.subplot(gs_cumulants[0, 0:2]),
                                                                xseries= df.x3.to_numpy(),
                                                                letter_label="(a)",
                                                                ylabel='Mom. Variance')),label_ind,c_ind)
                        self.format_subplot(self.make_cumulant_dictionary(plot_params_all,dict(subplot=plt.subplot(gs_cumulants[0, 4:]),
                                                                xseries= df.x2.to_numpy(),
                                                                letter_label="(c)",
                                                                ylabel='Cross Correlation')),label_ind,c_ind)
                        self.format_subplot(self.make_cumulant_dictionary(plot_params_all,dict(subplot=plt.subplot(gs_cumulants[1,:3]),
                                                                tseries = df.t.to_numpy(),
                                                                xseries= df["kappa"].to_numpy(),
                                                                letter_label="(d)",
                                                                ylabel=r'$\kappa_t$',
                                                                xloc=0.05*(2/3))),label_ind,c_ind)
                        #if (method =="direct" or (model_type=="control" and equil==False)):
                        lambda_series = np.gradient(df["kappa"].to_numpy(),df.t.to_numpy())
                        
                        #else:
                        #    lambda_series = self.b(df.y4,model_type,self.get_Lambda(file_name),self.get_g(file_name))

                        self.format_subplot(self.make_cumulant_dictionary(plot_params_all,dict(subplot=plt.subplot(gs_cumulants[1, 3:]),
                                                                #tseries = df.t.to_numpy(),
                                                                xseries= lambda_series,
                                                                letter_label="(e)",
                                                                ylabel=r'$\lambda_t$',
                                                                xloc=0.05*(2/3))),label_ind,c_ind)
                        
                        if method =="slowfast":
                            c_ind += 1
                        label_ind = False #add labels only on the first pass

                    except FileNotFoundError:
                        pass     
        plt.subplot(gs_cumulants[0, 0:2]).set_ylim(top=1.05,bottom=0.87)
        plt.subplot(gs_cumulants[0, 4:]).set_ylim(top=0.45,bottom=-0.2)
        plt.subplot(gs_cumulants[1, 3:]).set_ylim(top=14,bottom=-14)
        plt.subplot(gs_cumulants[1, :3]).set_ylim(top=1.2,bottom=-0.3)
        #add legend
        plt.subplot(gs_cumulants[1, 3:]).legend(fontsize=self.fontsizeticks
                                        ,loc="lower center"
                                        ,frameon=False
                                        ,ncols=2
                                        ,handlelength=1
                                        ,columnspacing=0.7)

        #plt.figtext(0.5, 0.01, param_label, ha="center", fontsize=self.fontsizetitles, bbox={"facecolor":"orange", "alpha":0.5, "pad":5})

        return fig
  
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
        
        return np.trapz(df.x3.to_numpy(),df.t.to_numpy()) - df.t.to_numpy()[-1]  
    
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

    def get_w2_dist(self):
        """
        This is an estimate of the W2 distance between the initial and final distributions
        computed with 20000 samples
        """

        return 0.30077160452189255

    def get_w2_dist_stiffness_control(self):
        """
        This is an estimate of the W2 distance between the initial and final distributions
        when we use the stiffness as a control.
        computed with 20000 samples
        """

        return 0.2600020057905375
