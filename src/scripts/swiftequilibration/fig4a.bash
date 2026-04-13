#!/bin/bash
#SBATCH --time=00:15:00
#SBATCH --nodes=1
#SBATCH --ntasks=4
#SBATCH --cpus-per-task=1
#SBATCH --mem-per-cpu=3G
#SBATCH --array=1-16

values=(2 3 4 5 6 7 8 9 10 11 12 15 20 30 40 50)

VAL=${values[$SLURM_ARRAY_TASK_ID-1]}

module load julia
julia --project=. -- src/julia/swiftequilibration/direct/ipopt_equil.jl $VAL 0.1 "hard" 1.0 "neg" &
julia --project=. -- src/julia/swiftequilibration/direct/stiffness_control.jl $VAL 0.1 "hard" 1.0 "neg"&
julia --project=. -- src/julia/swiftequilibration/direct/ipopt_equil.jl $VAL 0.1 "hard" 10.0 "kappa" &
julia --project=. -- src/julia/swiftequilibration/direct/stiffness_control.jl $VAL 0.1 "hard" 10.0 "kappa"&
wait
