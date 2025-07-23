import numpy as np 
import numpy.random as npr 
import pandas as pd

from plotscript import *

Generator = npr.default_rng(seed=None) #define rng 
batch_samples = 1000 #total number of samples 
plotter = PlotParams()

#generate the initial data
def generate_samples(self,batch_samples,mode):
    return np.column_stack((Generator.normal(loc=0,scale=np.sqrt(2),size=(batch_samples,1))  
                            ,Generator.standard_normal(size=(batch_samples,1))))

def get_drift(df,t,x):


def em_step(du,)

#compute 