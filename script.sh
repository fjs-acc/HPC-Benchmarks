#!/bin/bash
#SBATCH --partition=vl-parcio
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --output=/home/fschroed/forked-bm-tool/HPC-Benchmarks/script.out
#SBATCH --error=/home/fschroed/forked-bm-tool/HPC-Benchmarks/script.err

path="/home/fschroed/forked-bm-tool/HPC-Benchmarks"



install=$(python3 sb.py -i hpl longspec)
install=$(echo "$install" | grep "Submitted batch job")
install=${install##* }
#while [[ $(sacct -A=fschroed -j $install -n --parsable2 -X --format=State) != "COMPLETED" ]]
while [[ $(squeue  -j $install -h --state=COMPLETED) == "" ]]

do
    echo "still installing"
    echo "$install"
    sleep 10s
done
echo "installation complete"

run=$(python3 sb.py -r hpl longspec)
run=$(echo "$run" | grep "Submitted batch job")
run=${run##* }
#while [[ $(sacct -A=fschroed -j $install -n --parsable2 -X --format=State) != "COMPLETED" ]]
while [[ $(squeue  -j $run -h --state=COMPLETED) == "" ]]

do
    echo "still running"
    echo "$run"
    sleep 10s
done
echo "run complete"
echo "shutting down"
