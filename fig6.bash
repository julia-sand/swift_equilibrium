#!/bin/bash
#SBATCH --account=project_2011332
#SBATCH --partition=small
#SBATCH --time=00:30:00
#SBATCH --nodes=1
#SBATCH --ntasks=3
#SBATCH --cpus-per-task=1
#SBATCH --mem-per-cpu=4G
#SBATCH --array=2-5
#SBATCH --out=fig6.%a.out

IDXTEN=$(bc <<<"scale=3;10*$SLURM_ARRAY_TASK_ID")
IDXFIVE=$(bc <<<"scale=3;5+$SLURM_ARRAY_TASK_ID")

module load julia
julia --project=. -- src/indirect/diffeq_noneq_v2.jl $SLURM_ARRAY_TASK_ID 0.01 "harmonic" 1.4&
julia --project=. -- src/indirect/diffeq_noneq_v2.jl $IDXTEN 0.01 "harmonic" 1.4&
julia --project=. -- src/indirect/diffeq_noneq_v2.jl $IDXFIVE 0.01 "harmonic" 1.4&
wait
