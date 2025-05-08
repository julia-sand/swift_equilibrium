#!/bin/bash
#SBATCH --account=project_2011332
#SBATCH --partition=small
#SBATCH --time=01:00:00
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --mem-per-cpu=1G
#SBATCH --array=4-6
#SBATCH --output slowfast.%a.out

IDXTEN=$(bc <<<"scale=3;1/(10^$SLURM_ARRAY_TASK_ID)")

module load julia
julia --project=. -e 'using Pkg; Pkg.instantiate()'
julia --project=. src/indirect/slowfast.jl --g=0.01 --tf=$SLURM_ARRAY_TASK_ID --epsilon=1
julia --project=. slowfast.jl --g=$IDXTEN --tf=3 --epsilon=1
