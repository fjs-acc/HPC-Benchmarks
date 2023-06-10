#!/bin/bash
#SBATCH --partition=vl-parcio
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=48
#SBATCH --output=/home/fjs/ba/thesis/HPC-Benchmarks/install_python.out
#SBATCH --error=/home/fjs/ba/thesis/HPC-Benchmarks/install_python.err

source /home/fjs/spack//share/spack/setup-env.sh
spack install python
