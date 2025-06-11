#!/bin/bash
#SBATCH --account=project_2011332
#SBATCH --partition=small
#SBATCH --time=00:30:00
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --mem-per-cpu=5G

module load julia
julia --project=. -- src/TEMP.jl 2 "../../../../scratch/project_2011332/kldescent_test/results/20250610-180558"

