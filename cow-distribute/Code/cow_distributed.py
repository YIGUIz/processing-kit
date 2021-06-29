#########################################################################################################################################
# author:zq time:2021/06/15

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
PARAMFILE_OPEN=open(r'E:\Postgraduate_project\github\id\cow_distribute.param','r',encoding='UTF-8').readlines() #Need to check
PARAMETERS=[ind.strip().replace("'","").replace('"','').replace(';',',') for ind in PARAMFILE_OPEN if not '#' in ind[0]]
PARAM=[]
for i in PARAMETERS:
    if not i: continue
    PARAM.append(i.strip().split('=')[1].strip())
if PARAM[-1]=='\\t':PARAM[-1]='\t'

if len(PARAM)!=6:bomb('Wrong number of parameters found in peddam.param. Please check it!') #Need to check
else:input_file,col_id,out_file,error_file,Pro_path,Farm_path =PARAM #Need to check

###Run check of parameters
check_file(input_file,'input_file')
print("#Parameters check:OK")

#########################################################################################################################################

###Core DEF
def cow_distribution(input_file, out_file, error_file):
    ###Read the standby file
    Pro_dic = {}
    Farm_dic = {}
    for iline in open(Pro_path,'r',encoding = 'utf-8'):
        i = iline.strip().split()
        Pro_dic[i[0]] = i[1]
    for iline in open(Farm_path,'r',encoding = 'utf-8'):
        i = iline.strip().split()
        Farm_dic[i[0]] = i[1]

    col = int(col_id) - 1
    kfile = open(out_file, 'w+')
    efile = open(error_file, 'w+')
    for iline in open(input_file, 'r'):
        i = iline.strip().split()
        if len(i[col]) in [8, 12]:
            if len(i[col]) == 12:
                Province = i[col][0:2]
                Farm = i[col][0:6]
                #year_birth = i[col][6:8]
                #birth_order = i[col][8:12]
                Sex = 'F'
            else:
                Province = i[col][0:2]
                Farm = i[col][0:3]
                #year_birth = i[col][3:5]
                #birth_order = i[col][5:8]
                Sex = 'M'
            kfile.write(str(i[col]) + '\t' + str(Province) + '\t' + str(Farm) + '\t' + str(Sex) + '\n')
            #kfile.write(str(i[col]) + '\t' + str(Province) + '\t' + str(Farm) + '\t' + str(year_birth) + '\t' + str(
                #birth_order) + '\t' + str(sex) + '\n')
        else:
            efile.write(str(i[col]) + '\n')

    efile.close()
    kfile.close()

    data = pd.read_csv(out_file, sep='\s+', header=None, dtype=str)
    data.columns = ['ID', 'Province', 'Farm', 'Sex']
    #data.columns = ['ID', 'Province', 'Farm', 'Birth_year', 'Brith_order', 'Sex']
    data['Province'] = data['Province'].astype('str')
    data['Pro-cn'] = data['Province'].map(Pro_dic)
    data['Farm'] = data['Farm'].astype('str')
    data['Far-cn'] = data['Farm'].map(Farm_dic)
    kfile = open(out_file, 'w+',newline='')
    data.to_csv(kfile, sep='\t', index=None, header=True)

cow_distribution(input_file,out_file,error_file)