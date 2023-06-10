#!/bin/bash
#SBATCH --partition=vl-parcio
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --output=/home/fschroed/forked-bm-tool/HPC-Benchmarks/script.out
#SBATCH --error=/home/fschroed/forked-bm-tool/HPC-Benchmarks/script.err

path="/home/fschroed/forked-bm-tool/HPC-Benchmarks"


: '
install=$(python3 sb.py -i hpl longspec)
install=echo $install | grep "Submitted batch job"
install=${install##* }
while [[ $(sacct -j  -n --parsable2 -X --format=State) ungleich "CPMPLETED"]]
    do
        sleep 10s
    done
'
while [[ $(sacct -j  -n --parsable2 -X --format=State) !="COMPLETED" ]]
do
    echo "still waiting"
    sleep 10s
done