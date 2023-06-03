#Online Bash Shell.
#Code, Compile, Run and Debug Bash script online.
#Write your code in this editor and press "Run" button to execute it.
#!/bin/bash

#configs generieren...
:'
inst = $ (python3 sb.py - i all);
while[sacct inst != done]
do
    sleep 60s
done
'
python3 sb.py -r hpl
python3 sb.py -r osu
python3 sb.py -r hpcc
python3 sb.py -r hpcg


arr=( "a" "b" "c" )
for val in "${arr[@]}"
do
 sleep 1s
done

python3 auswertung.py
echo ${1[1]}

  