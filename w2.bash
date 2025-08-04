#!/bin/bash
#SBATCH --account=project_2011332
#SBATCH --partition=small
#SBATCH --time=01:00:00
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --mem-per-cpu=300G
#SBATCH --output=w2_dists.out

module load python-data
source ../kldescent/klenv/bin/activate
python src/viz/estimate_w2.py
