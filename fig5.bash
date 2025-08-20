#!/bin/bash
#SBATCH --account=project_2011332
#SBATCH --partition=small
#SBATCH --time=01:00:00
#SBATCH --nodes=1
#SBATCH --ntasks=2
#SBATCH --cpus-per-task=1
#SBATCH --mem-per-cpu=4G

module load julia
julia --project=. -- src/direct/contraction/ipopt_noneq_contract.jl 3 0.01 "harmonic" 1.4 "none"&
julia --project=. -- src/direct/contraction/ipopt_equil_contract.jl 3 0.01 "harmonic" 1.4 "none"&
wait
