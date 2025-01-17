# HPC-Benchmarks
# Copyright (C) 2022 Jessica Lafontaine, Tomas Cirkov
#
# Changes made for HPC-Benchmarks-2
# Copyright (C) 2023 Fabian Schröder
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import sys
import os
import subprocess
import re

from sb import shell, check_expr_syn, error_log, LOC, FCOL, FEND, info_feed

#debugging
import traceback

slurm='#!/'+sys.argv[1].replace('$','\n').replace('_',' ')
expr=[_.split('$') for _ in sys.argv[2].split('#')]
menutxt=''
no_hint = True

def give_hint():
    global menutxt, no_hint
    if no_hint and info_feed:
        menutxt+=FCOL[7]+'<info>    '+FEND+'new error entries for install.py in log.txt'
        no_hint = False

#Überprüft ob ein einzelner spec (Name + Version) existiert
def check_spec(name,version=-1):       
    out = shell('spack info '+str(name))
###NEW ADDITION###
    ###Some software is bundled together in a package of a different name
    ###like in the case of the intel compilers, and thus can not be found
    ###via spack find
    exceptions=["intel","oneapi"]
    if name.replace(" ","") in exceptions:
        return True
###/NEW ADDITION###




    #Falls keine Version vorhanden
    if version == -1:
        if out.find('Error')== -1:
            return True 
    elif out.find(version) != -1:
        return True         
    return False


#Prüft ob Installationsausdruck gültig ist (alle Specs)
def check_expr(expr,name):
    try:
        global menutxt   
        check_syn=check_expr_syn(expr,name)        
        if check_syn=='True':
            arr = expr.split('^')       
            
            for spec in arr:
                s=spec.split('%')
                
                #Untersuchung von einzelnem Package und Version
                for _ in s:            
                    """ Wird in check_expr_syn rausgefiltert
                    if _[0][:0]=='@' or _[0]=='':                    
                        menutxt+='\n'+FCOL[6]+'<warning> '+FEND+'profile: '+FCOL[6]+name+FEND+' was deselected! <spec error>: packagename is missing\n'+expr+FCOL[8]+'\n'+'^'.rjust(shift+2)+'^'.rjust(expr.find('^',shift+2,len(expr))-1)+FEND+'\n'
                        error_log('<spec error> at {}: packagename is missing\n'.format(name)+expr+'\n'+'^'.rjust(shift+2)+'^'.rjust(expr.find('^',shift+2,len(expr))-1)+'^'.rjust(expr.find('^',shift+2,len(expr))-1)+'\n',locals())
                        return False               
                    """
                    _=_.split('@')                
                    if len(_) > 1:
                        ###NEW ADDITION to fix the "package doesn't exist" problem caused by the flags
                        if not check_spec(_[0],_[1].split(" ")[0]):
                            #Version existiert nicht
                            menutxt+='\n'+FCOL[6]+'<warning> '+FEND+'profile: '+FCOL[6]+name+FEND+' was deselected!\n          reason: {} doesn\'t exist!\n'.format(_[0]+'@'+_[1])+expr+FCOL[8]+'\n'+'^'.rjust(expr.find(_[0]+'@'+_[1])+1)+FEND+'\n'
                            error_log('can\'t install {}: package {} doesn\'t not exist!\n'.format(name,_[0]+'@'+_[1])+expr+'\n'+'^'.rjust(expr.find(_[0]+'@'+_[1])+1)+'\n')                        
                            give_hint()
                            return False
                    else:
                        if not check_spec(_[0]):
                            #Package existiert nicht
                            menutxt+='\n'+FCOL[6]+'<warning> '+FEND+'profile: '+FCOL[6]+name+FEND+' was deselected!\n          reason: {} doesn\'t exist!\n'.format(_[0])+expr+FCOL[8]+'\n'+'^'.rjust(expr.find(_[0])+1)+FEND+'\n'
                            error_log('can\'t install {}: package {} doesn\'t exist!\n'.format(name,_[0])+expr+'\n'+'^'.rjust(expr.find(_[0])+1)+'\n')
                            give_hint()
                            return False
            return True
        #Syntaxfehler im Ausdruck  
        menutxt+=check_syn
        give_hint()
        return False
    except Exception as exc:     
        error_log('', locals(), traceback.format_exc())
        give_hint()
        sys.exit(menutxt)
              
#Schreibt Script zum installieren der specs 
def install_spec(expr):
    try:
        global menutxt
        global slurm
        specs=''

        for e in expr:
            #Prüft ob identische spec installiert werden soll
            if specs.find(e[0])==-1:            
                #Prüft ob jeweils die einzelnen Komponenten der spec existieren
                if check_expr(e[0],e[1])==True:                   
                    specs=specs+'srun spack install '+e[0]+'\n'                
        
        if len(specs)==0:        
            error_log('there is nothing to install')
            return ''             
                  
        return str(slurm+specs)
    except Exception as exc:     
        error_log('', locals(), traceback.format_exc()) 
        give_hint()
        sys.exit(menutxt)    

def main():
    try:
        #Write install.sh
        global menutxt       
        script_txt=install_spec(expr)
        if script_txt!='':
            with open('{}/install.sh'.format(LOC),'w') as f:
                f.write(script_txt)   
        sys.exit(menutxt)
        
    except Exception as exc:     
        error_log('', locals(), traceback.format_exc())
        give_hint()
        sys.exit(menutxt)
    
if __name__ == "__main__":
    main()



    
    