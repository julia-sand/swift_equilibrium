#!/bin/bash
#SBATCH --time=00:15:00
#SBATCH --nodes=1
#SBATCH --ntasks=3
#SBATCH --cpus-per-task=1
#SBATCH --mem-per-cpu=4G

module load julia
julia --project=. -- src/direct/stiffness_control.jl 4 0 "hard" 1 "kappa"&
julia --project=. -- src/direct/ipopt_equil.jl 4 0 "hard" 1 "kappa"&
julia --project=. -- src/direct/ipopt_equil.jl 4 0 "hard" 10 "kappa"&
wait
