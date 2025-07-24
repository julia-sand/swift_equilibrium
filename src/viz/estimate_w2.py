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

def em_step(xn,du_bar,dt,dw, epsilon=1):

    xn[:,0,None] = xn[:,0,None] + epsilon*xn[:,1,None]*dt 
    xn[:,1,None] = xn[:,1,None] - (xn[:,1,None] + epsilon*du_bar)*dt \
                                    + np.sqrt(2)*dw
    return xn 

def compute_xT(xinit,batch_samples,df, Generator):

    t_vec = get_ref_timegrid(df)
    #xinit = generate_samples(batch_samples)

    for i in range(0,len(t_vec)-1):
        dt = (t_vec[i+1]-t_vec[i])
        
        dw = generate_innovation(dt,batch_samples, Generator)
        #xdata = torch.column_stack(())
        du_bar = get_ref_du(df,t_vec[i],xinit[...,[0]])
        
        xinit = em_step(xinit,du_bar,dt,dw)
    
    return xinit

def compute_w2(batch_samples):
        
    #batch_samples = 500 #total number of samples
    epsilon = 1 
    plotter = PlotParams() #instantiate plotter
    Generator = npr.default_rng(seed=None) #define rng 
    
    #df = plotter.get_data("hard","direct","equil","T4-0_Lambda3-0_eps1_g0-1.csv","constrained_kappa")
    df = plotter.get_data("harmonic","indirect","equil","T4-0_Lambda1-4_eps1_g0-01.csv","none")
    xinit = generate_samples(batch_samples, Generator)
    xout = compute_xT(xinit,batch_samples,df, Generator)
    
    M = ot.dist(xinit, xout, metric="sqeuclidean")

    # reg term
    lambd = 1e-1
    a, b = np.ones((batch_samples,)) / batch_samples, np.ones((batch_samples,)) / batch_samples  # uniform distribution on samples

    Gs = ot.sinkhorn2(a, b, M, lambd)
    return Gs

if __name__=="__main__":
    

    Gs = compute_w2(10000)
    print(Gs)
