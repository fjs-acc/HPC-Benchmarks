import sys
import os
import subprocess
import re

from sb import shell, check_expr_syn, error_log


meta=sys.argv[1].split('#')
expr=[_.split('$') for _ in sys.argv[2].split('#')]
menutxt=''

#plot.py Path
LOC=str(os.path.dirname(os.path.abspath(__file__)))

#Shellfunktion aus sb.py (Hauptprogramm)
"""
def shell(cmd):
    #Ausgabe soll nicht direkt auf's Terminal
    p = subprocess.run(str(cmd), stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)   
    #.stdout liefert einen Binärstring desw. die Dekodierung
    return p.stdout.decode('UTF-8')



#Prüft Installationsausdruck auf grobe Syntaxfehler
def check_expr_syn(expr):
    expr_list=['@%','%@','^%','%^','^@','@^']
   
   
    Hinweis bzgl. regulärem Ausdruck:
    {min,max} min/max vorkommen der vorrangegangenen Zeichenkette 
    \w Symbolmenge: [a-z, A-Z, 0-9, _]            
    * Vorangegangene Zeichenkette kommt beliebig oft vor (inkl. 0 mal)
    (...) Gruppe -> praktisch eine Zeichenkette
    \. Punktsymbol, da einfach nur . für einzelnes Zeichen steht            
  
    if re.search(r'@{1,1}(\w*\.*[%]{0,0}\w*)*@{1,}',expr):
        return False
    for _ in expr_list:
        r=expr.find(_)        
        if r != -1:
            sb.error_log('echo Syntaxfehler an Position: {} >> {}/install.err'.format(str(r),LOC),locals())
            sb.err
            return False
    return True
"""

#Überprüft ob ein einzelner spec (Name + Version) existiert
def check_spec(name,version=-1):       
    out = shell('spack info '+str(name))
    #Falls keine Version vorhanden
    if version == -1:
        if out.find('Error')== -1:
            return True 
    elif out.find(version) != -1:
        return True         
    return False


#Prüft ob Installationsausdruck gültig ist (alle Specs)
def check_expr(expr,name):
    global menutxt
    if check_expr_syn(expr,name)==True:
        arr = expr.split('^')       
        
        for spec in arr:
            s=spec.split('%')           
            #Untersuchung von einzelnem Package und Version
            for _ in s:            
                if _[0][:0]=='@':
                    menutxt+='\n'+FCOL[6]+'<warning> '+FEND+'profile: '+FCOL[6]+name+FEND+' was deselected! \n<spec error> at {}: packagename is missing\n'.format(name)
                    error_log('<spec error> at {}: packagename is missing\n'.format(name),locals())
                    return False               
                
                _=_.split('@')                
                if len(_) > 1:
                    if not check_spec(_[0],_[1]):
                        #Version existiert nicht
                        menutxt+='\n'+FCOL[6]+'<warning> '+FEND+'profile: '+FCOL[6]+name+FEND+' was deselected! \n<spec error> at {}: version {} does not exist\n'.format(name,_[0]+'@'+_[1])
                        error_log('<spec error> at {}: version {} does not exist\n'.format(name,_[0]+'@'+_[1]),locals())                        
                        return False
                else:
                    if not check_spec(_[0]):
                        #Package existiert nicht
                        menutxt+='\n'+FCOL[6]+'<warning> '+FEND+'profile: '+FCOL[6]+name+FEND+' was deselected! \n<spec error> at {}: package {} does not exist\n'.format(name,_[0])
                        error_log('<spec error> at {}: package {} does not exist\n'.format(name,_[0]),locals())
                        return False
       
        return True
    #Syntaxfehler im Ausdruck     
    return False

              
#Schreibt Script zum installieren der specs 
def install_spec(expr):
    partition=meta[0]
    node=meta[1]
    task=meta[2]
    cpus=meta[3]
    #Check ob angegebene Partition existiert
    if shell('sinfo -h -p '+partition).find(partition)==-1:        
        error_log('Partition: {} existiert nicht'.format(str(partition)),locals())
        #os.system('echo Partition: {} existiert nicht >> {}/install.err'.format(str(partition),LOC),locals())
        return 
        
    slurm=''
    specs=''  
    
    #Slurmparameter für die Installation
    slurm='#!/bin/bash\n' \
    +'#SBATCH --nodes='+node+'\n' \
    +'#SBATCH --ntasks='+task+'\n' \
    +'#SBATCH --cpus-per-task='+cpus+'\n' \
    +'#SBATCH --partition='+partition+'\n' \
    +'#SBATCH --output={}/install.out\n'.format(LOC) \
    +'#SBATCH --error={}/install.err\n\n'.format(LOC) \
    +'source {}/share/spack/setup-env.sh\n'.format(meta[4])
    
    for e in expr:
        #Prüft ob identische spec installiert werden soll
        if specs.find(e[0])==-1:            
            #Prüft ob jeweils die einzelnen Komponenten der spec existieren
            if check_expr(e[0],e[1])==True:                   
                specs=specs+'srun spack install '+e[0]+'\n'
    """            
    if len(specs)==0:
        menutxt+='\n'
        error_log('everything already installed',locals())
        #return os.system('echo bereits alles installiert >> {}/install.err'.format(str(e),LOC))                
    """          
    return str(slurm+specs)

def main():
    #Write install.sh
    with open('{}/install.sh'.format(LOC),'w') as f:
        f.write(install_spec(expr))
    print(menutxt)
    sys.exit(menutxt)
    
if __name__ == "__main__":
    main()



    
    