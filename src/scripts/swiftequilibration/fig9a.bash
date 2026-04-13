#!/bin/bash
#SBATCH --time=00:30:00
#SBATCH --nodes=1
#SBATCH --ntasks=2
#SBATCH --cpus-per-task=1
#SBATCH --mem-per-cpu=4G
#SBATCH --array=1-16

values=(2 3 4 5 6 7 8 9 10 11 12 15 20 30 40 50)

# Get the value for this task
VAL=${values[$SLURM_ARRAY_TASK_ID-1]}

module load julia
julia --project=. -- src/julia/swiftequilibration/indirect/diffeq_noneq.jl $VAL 0.01 "harmonic" 1.4&
julia --project=. -- src/julia/swiftequilibration/indirect/diffeq_equil.jl $VAL 0.01 "harmonic" 1.4&
wait
