#!/bin/bash
#SBATCH --account=project_2011332
#SBATCH --partition=small
#SBATCH --time=03:00:00
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --mem-per-cpu=5G
#SBATCH --array=2-10
#SBATCH --output=indirect_noneq_T.%a.out

IDXTEN=$(bc <<<"scale=3;1/(10^$SLURM_ARRAY_TASK_ID)")

module load julia
julia --project=. -- src/indirect/diffeq_noneq_v2.jl $SLURM_ARRAY_TASK_ID 0.01 "harmonic" 1.4
