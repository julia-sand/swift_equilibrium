#!/bin/bash
#SBATCH --account=project_2011332
#SBATCH --partition=small
#SBATCH --time=02:00:00
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --mem-per-cpu=5G
#SBATCH --array=1-2
#SBATCH --output=direct_noneq.%a.out

IDXTEN=$(bc <<<"scale=3;1/(10^$SLURM_ARRAY_TASK_ID)")

module load julia
julia --project=. -- src/direct/ipopt_noneq.jl 3 0.01 "hard" $SLURM_ARRAY_TASK_ID
