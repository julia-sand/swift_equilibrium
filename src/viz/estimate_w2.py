import numpy as np 
import numpy.random as npr 
import pandas as pd

from plotscript import *

#Estimates the W2 distance between the initial and final distributions 

#generate the initial data
def generate_samples(batch_samples):
    return np.column_stack((Generator.normal(loc=0,scale=1,size=(batch_samples,1))  
                            ,Generator.standard_normal(size=(batch_samples,1))))

def get_ref_du(df,t,x):
    return df[df["t"]==t].kappa.values*x

def generate_innovation(dt,batch_samples):
    
    return Generator.standard_normal(size=(batch_samples,1))*np.sqrt(dt)

def get_ref_timegrid(df):

    return df.t.unique()

def em_step(xn,du_bar,dt,dw):

    xn[:,0,None] = xn[:,0,None] + epsilon*xn[:,1,None]*dt 
    xn[:,1,None] = xn[:,1,None] - (xn[:,1,None] + epsilon*du_bar)*dt \
                                    + np.sqrt(2)*dw
    return xn 
#compute 
def compute_xT(xinit,batch_samples,df):

    t_vec = get_ref_timegrid(df)
    #xinit = generate_samples(batch_samples)

    for i in range(0,len(t_vec)-1):
        dt = (t_vec[i+1]-t_vec[i])
        
        dw = generate_innovation(dt,batch_samples)
        #xdata = torch.column_stack(())
        du_bar = get_ref_du(df,t_vec[i],xinit[...,[0]])
        
        xinit = em_step(xinit,du_bar,dt,dw)
    
    return xinit

if __name__=="__main__":
    import ot 
        
    Generator = npr.default_rng(seed=None) #define rng 
    batch_samples = 500 #total number of samples
    epsilon = 1 
    plotter = PlotParams()
    
    df = plotter.get_data("hard","direct","equil","T4-0_Lambda3-0_eps1_g0-1.csv","constrained_kappa")
    xinit = generate_samples(batch_samples)
    xout = compute_xT(xinit,batch_samples,df)
    print("mom var =", np.nanvar(xout[:,1]))
    print("mom mean =", np.nanmean(xout[:,1]))
    print("pos var =", np.nanvar(xout[:,0]))
    print("pos mean =", np.nanmean(xout[:,0]))
    print("xcorr =", np.correlate(xout[:,0],xout[:,1])[0]/batch_samples)

    M = ot.dist(xinit, xout, metric="sqeuclidean")

    # reg term
    lambd = 1e-1
    a, b = np.ones((batch_samples,)) / batch_samples, np.ones((batch_samples,)) / batch_samples  # uniform distribution on samples

    Gs = ot.sinkhorn2(a, b, M, lambd)
    print(Gs)
