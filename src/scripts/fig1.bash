#!/bin/bash
#SBATCH --time=00:15:00
#SBATCH --nodes=1
#SBATCH --ntasks=4
#SBATCH --cpus-per-task=1
#SBATCH --mem-per-cpu=4G

module load julia
julia --project=. -- src/direct/ipopt_equil.jl 3 0.01 "harmonic" 1.4 "none"&
julia --project=. -- src/indirect/diffeq_equil.jl 3 0.01 "harmonic" 1.4 "none"&
julia --project=. -- src/indirect/slowfast.jl 3 0.01 "harmonic" 1.4 "none"&
julia --project=. -- src/indirect/slowfast.jl 3 0.001 "harmonic" 1.4 "none"&
wait
