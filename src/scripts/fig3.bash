#!/bin/bash
#SBATCH --time=00:15:00
#SBATCH --nodes=1
#SBATCH --ntasks=2
#SBATCH --cpus-per-task=1
#SBATCH --mem-per-cpu=4G

module load julia
julia --project=. -- ../src/direct/ipopt_equil.jl 3 0 "hard" 9 "none"&
julia --project=. -- ../src/indirect/diffeq_equil.jl 3 0.01 "log" 9 "none"&
wait