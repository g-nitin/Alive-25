#! /bin/bash

#SBATCH --job-name=geocoding
#SBATCH -o r_out%j.out
#SBATCH -e r_err%j.err

#SBATCH --mail-user=niting@email.sc.edu
#SBATCH --mail-type=ALL

#SBATCH -p defq-48core

module load python3/anaconda/2021.07 gcc/12.2.0 cuda/12.1
source activate /home/niting/miniconda3/envs/alive-25

echo $CONDA_DEFAULT_ENV

#Run script
hostname
python3 geocoding.py

#Exit the conda system
conda deactivate