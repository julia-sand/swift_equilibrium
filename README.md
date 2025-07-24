Code to reproduce plots of **REF**
Plotting and data manipulation is done in Python, integration is done through Julia

Integration is mostly done through the DifferentialEquations.jl and InfiniteOpt.jl packages. 

Step 1. Create results directory structure to save the file
```
python src/make_results_dir.py
```
Step 2. Instantiate Julia environment from Project.toml file
```
julia --project=.
] instantiate
```
Step 2. Run the results you would like to see 
e.g. for minimum entropy production
```
julia src/direct/ipopt_equil.jl T g "penalty" Lambda "kappa"
```
for minimum work
```
julia src/direct/ipopt_noneq.jl T g "penalty" Lambda "kappa"
```
for minimising entropy production where the control is no longer a state (Case S2)
```
julia src/direct/ipopt_noneq.jl T g "penalty" Lambda "kappa"
```
