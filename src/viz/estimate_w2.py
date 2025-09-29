import numpy as np 
import numpy.random as npr 
import pandas as pd
import ot 

from plotscript import *

#Estimates the W2 distance between the initial and final distributions 

#generate the initial data
def generate_samples(batch_samples, Generator):
    return np.column_stack((Generator.normal(loc=0,scale=1,size=(batch_samples,1))  
                            ,Generator.standard_normal(size=(batch_samples,1))))

def get_ref_du(df,t,x):
    return df[df["t"]==t].kappa.values*x

def generate_innovation(dt,batch_samples, Generator):
    
    return Generator.standard_normal(size=(batch_samples,1))*np.sqrt(dt)

def get_ref_timegrid(df):

    return df.t.unique()

def em_step(xn,du_bar,dt,batch_samples,Generator,epsilon=1):

    xn[:,0,None] = xn[:,0,None] + epsilon*xn[:,1,None]*dt 
    xn[:,1,None] = xn[:,1,None] - (xn[:,1,None] + epsilon*du_bar)*dt \
                                    + np.sqrt(2)*generate_innovation(dt,batch_samples, Generator)
    return xn 

def compute_xT(xinit,batch_samples,df, Generator):

    t_vec = get_ref_timegrid(df)
    #xinit = generate_samples(batch_samples)

    for i in range(0,len(t_vec)-1):
        dt = (t_vec[i+1]-t_vec[i])
        
        #dw = generate_innovation(dt,batch_samples, Generator)
        du_bar = get_ref_du(df,t_vec[i],xinit[...,[0]])
        
        xinit = em_step(xinit,du_bar,dt,batch_samples,Generator,)
    
    return xinit

def return_w2(xinit, xout,batch_samples):

    M = ot.dist(xinit, xout, metric="sqeuclidean")

    # reg term
    lambd = 1e-1
    a, b = np.ones((batch_samples,)) / batch_samples, np.ones((batch_samples,)) / batch_samples  # uniform distribution on samples

    Gs = ot.sinkhorn2(a, b, M, lambd)
    return Gs


def compute_w2(batch_samples,df):
        
    #batch_samples = 500 #total number of samples
    epsilon = 1 
    #plotter = PlotParams() #instantiate plotter
    Generator = npr.default_rng(seed=None) #define rng 
    
    #df = plotter.get_data("hard","direct","equil","T4-0_Lambda3-0_eps1_g0-1.csv","constrained_kappa")
    xinit = generate_samples(batch_samples, Generator)
    xout = compute_xT(xinit.copy(),batch_samples,df, Generator)
    
    Gs_marg = return_w2(xinit[:,[0]],xout[:,[0]],batch_samples)
    Gs_all = return_w2(xinit,xout,batch_samples)
    return Gs_all,Gs_marg

def ex1():
    """
    computes the W2 distance in w2_dist_equil_constrained_kappa
    """

    plotter = PlotParams()
    df = plotter.get_data("hard",
                            "direct",
                            "equil",
                            "T3-0_Lambda1-0_eps1_g0-1.csv",
                            "constrained_kappa")
    res = compute_w2(20000,df)
    print("w2_dist_equil_constrained_kappa_lambda1 ",res[0])
    print("w2_dist_equil_constrained_kappa_lambda1 ",res[1])

    return 

def ex2():
    """
    computes the W2 distance in get_w2_dist_equil_constrained_kappa
    """

    plotter = PlotParams()
    df = plotter.get_data("hard",
                            "direct",
                            "stiffness_control",
                            "T3-0_Lambda1-0_eps1_g0-1.csv",
                            "constrained_kappa")

    return df

def ex1a():
    """
    computes the W2 distance in get_w2_dist_equil_constrained_kappa_lambda10
    """

    plotter = PlotParams()
    df = plotter.get_data("hard",
                            "direct",
                            "equil",
                            "T3-0_Lambda10-0_eps1_g0-1.csv",
                            "constrained_kappa")
    res = compute_w2(20000,df)
    print("w2_dist_equil_constrained_kappa_lambda10 ",res[0])
    print("w2_dist_equil_constrained_kappa_lambda10 ",res[1])

    return 

def ex3():
    """
    computes the W2 distance in get_w2_dist_equil_negative_constrained_kappa
    """

    plotter = PlotParams()
    df = plotter.get_data("hard",
                            "direct",
                            "equil",
                            "T3-0_Lambda10-0_eps1_g0-1.csv",
                            "negative_constrained_kappa")

    return df


def ex3a():
    """
    computes the W2 distance in get_w2_dist_equil_negative_constrained_kappa_small_lambda10
    """

    plotter = PlotParams()
    df = plotter.get_data("hard",
                            "direct",
                            "equil",
                            "T3-0_Lambda1-0_eps1_g0-1.csv",
                            "negative_constrained_kappa_small")

    res = compute_w2(20000,df)
    print("w2_dist_equil_negative_constrained_kappa_small_lambda1 ",res[0])
    print("w2_dist_equil_negative_constrained_kappa_small_lambda1_marg ",res[1])

    return 


def ex3b():
    """
    computes the W2 distance in get_w2_dist_equil_negative_constrained_kappa_small_lambda10
    """

    plotter = PlotParams()
    df = plotter.get_data("hard",
                            "direct",
                            "equil",
                            "T3-0_Lambda10-0_eps1_g0-1.csv",
                            "negative_constrained_kappa_small")

    res = compute_w2(20000,df)
    print("w2_dist_equil_negative_constrained_kappa_small_lambda10 ",res[0])
    print("w2_dist_equil_negative_constrained_kappa_small_lambda10_marg ",res[1])

    return 

def ex4():
    """
    computes the W2 distance in get_w2_dist_stiffness_control_negative_constrained_kappa
    """

    plotter = PlotParams()
    df = plotter.get_data("hard",
                            "direct",
                            "stiffness_control",
                            "T3-0_Lambda10-0_eps1_g0-1.csv",
                            "negative_constrained_kappa")

    return df

def ex5():
    """
    computes the W2 distance in get_w2_dist_stiffness_control_negative_constrained_kappa_small
    """

    plotter = PlotParams()
    df = plotter.get_data("hard",
                            "direct",
                            "stiffness_control",
                            "T3-0_Lambda10-0_eps1_g0-1.csv",
                            "negative_constrained_kappa_small")
    res = compute_w2(20000,df)

    print("w2_dist_stiffness_control_negative_constrained_kappa_small ",res[0])
    print("w2_dist_stiffness_control_negative_constrained_kappa_small_marg ",res[1])

    return 



if __name__=="__main__":
    
    #print("w2_dist_equil_constrained_kappa ",compute_w2(20000,ex1()))
    #print("w2_dist_stiffness_control_constrained_kappa ",compute_w2(20000,ex2()))
    #print("w2_dist_equil_negative_constrained_kappa ",compute_w2(20000,ex3()))
    #print("w2_dist_stiffness_control_negative_constrained_kappa ",compute_w2(20000,ex4()))

    #ex1a()
    #ex3a()
    #ex3b()
    #ex5()
    ex1()
