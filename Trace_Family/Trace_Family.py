#########################################################################################################################################
# author:zq time:2021/06/29

# -*- coding:utf-8 -*-
import sys,os
import pandas as pd

###USEFUL DEFs
def bomb(message):
    print("ERROR:%s" %message )
    sys.exit()

def check_file(value,name):
    try:os.path.exists(value)
    except:bomb('The file provided in parameter %s was not found!' %name)

def ig_capital(ingonre_c,dir1,dic):
    global tmp1
    global tmp2
    if ingonre_c:
        tmp1 = (dir1.upper() in dic)
        tmp2 = (dir1.lower() in dic)
    else:
        tmp_result = (dir1 in dic)
    tmp_result = tmp1 or tmp2
    return tmp_result


###IMPORT parameter file
PARAMFILE_OPEN=open(r'E:\Postgraduate_project\github\Trace-Family\Code\Trace-Family.param','r',encoding='UTF-8').readlines() #Need to check
PARAMETERS=[ind.strip().replace("'","").replace('"','').replace(';',',') for ind in PARAMFILE_OPEN if not '#' in ind[0]]
PARAM=[]
for i in PARAMETERS:
    if not i: continue
    PARAM.append(i.strip().split('=')[1].strip())
if PARAM[-1]=='\\t':PARAM[-1]='\t'

if len(PARAM)!=5:bomb('Wrong number of parameters found in peddam.param. Please check it!') #Need to check
else:cow_file,col_id,ped_file,ped_tree,ancestor =PARAM #Need to check

###Run check of parameters
check_file(cow_file,'cow_file')
print("#Parameters check:OK")

#########################################################################################################################################

###Core DEF
def trace_family(cow_file,col_id,ped_file,ped_tree,ancestor):
    '''Trace the ancestor of the cattle'''
    
    ped = {}
    col = int(col_id)-1
    out_file1 = open(ped_tree,'w+')
    out_file2 = open(ancestor,'w+')
    for jline in open(ped_file,'r'): #the formate of ped:ID、Sire、Dam
        j = jline.strip().split()
        ped[j[0]] = j[1]
    
    for iline in open(cow_file,'r'):
        i = iline.strip().split() 
        ind = i[col]
        out_file1.write(ind+'\t')
        while ig_capital(True,ind,ped):
            if tmp1:
                ind_sire = ped[ind.upper()]
            else:
                ind_sire = ped[ind.lower()]
                
            if ind_sire == '0':
                pass
            else:
                out_file1.write(ind_sire+'\t')
            ind = ind_sire
        out_file1.write('\n')

        for jline in open(ped_tree,'r'):
            j = jline.strip().split()
        if j[len(j)-1] =='0':
            out_file2.write(j[0]+'\t'+j[len(j)-2]+'\n')
        else:
            out_file2.write(j[0]+'\t'+j[len(j)-1]+'\n')
    out_file1.close()    
    out_file2.close()
    
trace_family(cow_file,col_id,ped_file,ped_tree,ancestor)
