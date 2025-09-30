**Optimal control of engineered swift equilibration of
nanomechanical oscillators**

We propose a reformulation of the problem of optimally controlled transitions in
stochastic thermodynamics. We impose that any terminal cost specified by a thermodynamic
functional should depend only on state variables and not on control protocols, according to the
canonical Bolza form. In this way, we can unambiguously discriminate between transitions at
minimum dissipation between genuine equilibrium states, and transitions at minimum work driving
a system from a genuine equilibrium to a non-equilibrium state.

The code in this repository can be used to reproduce the plots found in the paper.

**Installation**
Integration is mostly done through the DifferentialEquations.jl and InfiniteOpt.jl packages in Julia, version 10 or above. The  Visualisations are made in Python using data from csvs with Matplotlib and include some data handling in Pandas. 

The following steps can be run from the command line once Python and Julia are installed. 

**Step 1.** Create results directory structure 
```
python src/make_results_dir.py
```
**Step 2.** Instantiate Julia environment for integration
```
julia --project=.
] instantiate
```
**Step 3.** To run individual simulations 
e.g. for minimum entropy production
```
julia src/direct/ipopt_equil.jl T g "penalty" Lambda "kappa"
```
for minimum work
```
julia src/direct/ipopt_noneq.jl T g "penalty" Lambda "kappa"
```
for minimising entropy production where the stiffness is the control (Case S2)
```
julia src/direct/stiffness_control.jl T g "penalty" Lambda "kappa"
```
ARGS (position):
- $T$: final time of the simulation
- $g$: size of penalty for "log"
- "penalty": choose from "log", "hard", "harmonic" (see Sec. 4)
- $\Lambda$: size of penalty for "log" and "hard"; "harmonic" penalty will use $\sqrt{2}$ by default.
- "kappa": for "hard" penalty, use the argument "kappa" to constrain the values of $\mathscr{k}_t$ or "neg3" to constrain the values in an interval which also includes negative values. Use "none" for no constraints. The value of $\kappa$ is not constrained by default. The exact constraints can be checked and edited in the file.

Alternatively, pre-made batch scripts that produce all results for a Figure can be found in the src/scripts folder. These can be run on a slurm cluster eg 
```
sbatch src/scripts/fig1.bash
```

**Step 4.**: Plotting is done through Python's matplotlib library
```
python src/viz/plotting.py
```
Costs for control vs state (as Figs.4) 
```
python src/viz/control_v_state.py
```
Costs for equilibration vs minimum work (as Figs.8&9) 
```
python src/viz/cost_v_time.py
```
Custom plots can be made by editing the functions within these files to include different method/file names. 
For other plots, please check the documentation found in the files in the src/viz folder.

