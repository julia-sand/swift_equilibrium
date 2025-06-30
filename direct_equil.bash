#!/bin/bash
#SBATCH --account=project_2011332
#SBATCH --partition=small
#SBATCH --time=01:00:00
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --mem-per-cpu=5G
#SBATCH --array=7-10
#SBATCH --output=direct_equil_hard.%a.out

IDXTEN=$(bc <<<"scale=3;1/(10^$SLURM_ARRAY_TASK_ID)")

module load julia
julia --project=. -- src/direct/ipopt_equil.jl 3 0.01 "hard" $SLURM_ARRAY_TASK_ID

