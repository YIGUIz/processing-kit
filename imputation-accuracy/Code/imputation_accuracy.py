#########################################################################################################################################
# author:zq time:2021/08/20

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
 

###IMPORT parameter file
PARAMFILE_OPEN=open(r'C:\Users\Administrator\Desktop\imputation-accuracy.param','r',encoding='gb18030').readlines() #Need to check
PARAMETERS=[ind.strip().replace("'","").replace('"','').replace(';',',') for ind in PARAMFILE_OPEN if not '#' in ind[0]]
PARAM=[]
for i in PARAMETERS:
    if not i: continue
    PARAM.append(i.strip().split('=')[1].strip())
if PARAM[-1]=='\\t':PARAM[-1]='\t'

if len(PARAM)!=4:bomb('Wrong number of parameters found in peddam.param. Please check it!') #Need to check
else:ture_ped,imputated_ped,result,common =PARAM #Need to check

###Run check of parameters
check_file(ture_ped,'ture_ped')
print("#Parameters check:OK")

#########################################################################################################################################

###Core DEF
def imputation_accuracy(ture_ped,imputated_ped,result,common):
    '''The aim of the program is calculating the accurcy of imputation.'''
    ### Read the data
    ture_ped_dic = {}
    common = int(common)
    out_file = open(result,'w+')
    out_file.write('id'+'\t'+'identical'+'\t'+'accuracy'+'\n') #cols name
    for iline in open(ture_ped,'r'):
        i = iline.strip().split()
        ture_ped_dic[i[1]] = i[:]
    
    ### The main Program
    for jline in open(imputated_ped,'r'):
        j = jline.strip().split()
        ind_ped = ture_ped_dic[j[1]]
        correct = 0
        for k in range(6,len(ind_ped)):
            if j[k] == ind[k]:
                correct += 1
        identical = correct/(len(ind_ped)-6)
        accuracy = (correct-common)/(len(ind_ped)-6-common)
        out_file.write(j[1]+'\t'+str(identical)+'\t'+str(accuracy)+'\n')
    out_file.close()

imputation_accuracy(ture_ped,imputated_ped,result,common)
