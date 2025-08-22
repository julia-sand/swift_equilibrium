#!/bin/bash
#SBATCH --account=project_2011332
#SBATCH --partition=small
#SBATCH --time=00:15:00
#SBATCH --nodes=1
#SBATCH --ntasks=10
#SBATCH --cpus-per-task=1
#SBATCH --mem-per-cpu=3G
#SBATCH --array=2-5
#SBATCH --output=direct_equil_hard.%a.out

IDXTEN=$(bc <<<"scale=3;10*$SLURM_ARRAY_TASK_ID")
IDXFIVE=$(bc <<<"scale=3;5+$SLURM_ARRAY_TASK_ID")

module load julia
julia --project=. -- src/direct/stiffness_control.jl $IDXFIVE 0.1 "hard" 10.0 "neg2"&
julia --project=. -- src/direct/stiffness_control.jl $SLURM_ARRAY_TASK_ID 0.1 "hard" 1.0 "neg2"&
julia --project=. -- src/direct/stiffness_control.jl $IDXFIVE 0.1 "hard" 1.0 "neg2"&
julia --project=. -- src/direct/stiffness_control.jl $IDXTEN 0.1 "hard" 1.0 "neg2"&
julia --project=. -- src/direct/ipopt_equil.jl $SLURM_ARRAY_TASK_ID 0.1 "hard" 10.0 "neg2"&
julia --project=. -- src/direct/ipopt_equil.jl $IDXFIVE 0.1 "hard" 10.0 "neg2"&
julia --project=. -- src/direct/ipopt_equil.jl $IDXTEN 0.1 "hard" 10.0 "neg2"&
julia --project=. -- src/direct/ipopt_equil.jl $SLURM_ARRAY_TASK_ID 0.1 "hard" 1.0 "neg2"&
julia --project=. -- src/direct/ipopt_equil.jl $IDXFIVE 0.1 "hard" 1.0 "neg2"&
julia --project=. -- src/direct/ipopt_equil.jl $IDXTEN 0.1 "hard" 1.0 "neg2"&
wait
