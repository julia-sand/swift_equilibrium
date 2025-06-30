#!/bin/bash
#SBATCH --account=project_2011332
#SBATCH --partition=small
#SBATCH --time=03:00:00
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --mem-per-cpu=5G
#SBATCH --array=1-3
#SBATCH --output=indirect_equil.%a.out

IDXTEN=$(bc <<<"scale=3;1/(10^$SLURM_ARRAY_TASK_ID)")

module load julia
julia --project=. -- src/indirect/diffeq_equil.jl 3 $IDXTEN "control" 1.4 
