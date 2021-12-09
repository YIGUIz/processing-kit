#########################################################################################################################################
# author:zq time:2021/12/09

# -*- coding:utf-8 -*-
import sys,os

###USEFUL DEFs
def bomb(message):
    print("ERROR:%s" %message )
    sys.exit()

def check_file(value,name):
    try:os.path.exists(value)
    except:bomb('The file provided in parameter %s was not found!' %name)
 

###IMPORT parameter file
PARAMFILE_OPEN=open(r'*\imputation-accuracy.param','r',encoding='UTF-8').readlines() #Need to check
PARAMETERS=[ind.strip().replace("'","").replace('"','').replace(';',',') for ind in PARAMFILE_OPEN if not '#' in ind[0]]
PARAM=[]
for i in PARAMETERS:
    if not i: continue
    PARAM.append(i.strip().split('=')[1].strip())
if PARAM[-1]=='\\t':PARAM[-1]='\t'

if len(PARAM)!=6:bomb('Wrong number of parameters found in peddam.param. Please check it!') #Need to check
else:true_ped,true_map,phased_ped,phased_map,result_statistic,result_snp =PARAM #Need to check

###Run check of parameters
check_file(true_ped,'true_ped')
print("#Parameters check:OK")

#########################################################################################################################################
def imputation_accuracy(true_ped,true_map,phased_ped,phased_map,result_statistic,result_snp): #phased_map = Used_snp.txt
    '''The aim of the program is calculating the accurcy of imputation.'''
    ### Read the data
    phased_ped_dic = {}
    true_snp = []
    phased_snp = []
    out_file1 = open(result_statistic,'w+')
    out_file2 = open(result_snp,'w+')
        
    for jline in open(phased_ped,'r'):
        j = jline.strip().split()
        phased_ped_dic[j[1]] = j[:]
    
    for kline in open(true_map,'r'):
        k = kline.strip().split()
        true_snp.append(k[1])
        
    for line in open(phased_map,'r'):
        l = line.strip().split()
        phased_snp.append(l[1])
        #phased_snp.append(l[0]) #notice!! the phased_map's format is unormal.
    
    common_snp = list(set(true_snp).intersection(phased_snp))
    
    ### The main Program
    for mline in open(true_ped,'r'):
        m = mline.strip().split()
        ind = m[1]
        correct = 0
        miss_num = 0
        all_common = len(common_snp)
        ind_phased_ped = phased_ped_dic[ind] #the phased ped is benchmark
        for n in range(6,len(ind_phased_ped),2):
            pos = int((n-6)/2)
            snp_name = phased_snp[pos]
            cor_pos = true_snp.index(snp_name)
            cor_n = cor_pos*2+6
            if snp_name in common_snp:
                gen1 = '%s%s'%(m[cor_n],m[cor_n+1]) #true_geno
                gen2 = '%s%s'%(ind_phased_ped[n],ind_phased_ped[n+1]) #the step aim to distinguish AG and GA.
                gen3 = '%s%s'%(ind_phased_ped[n+1],ind_phased_ped[n])                
                if (gen1 == gen2) or (gen1 == gen3):
                    correct += 1
                else:
                    diff = [ind,snp_name,gen1,gen2]
                    out_file2.write('\t'.join('%s'%h for h in diff)+'\n')
                if (gen1 == '00')or(gen2 == '00')or(gen3 == '00'):
                    miss_num += 1
        output = [ind,all_common,miss_num,correct]
        out_file1.write('\t'.join('%s'%p for p in output)+'\n')
    out_file1.close()
    out_file2.close()
imputation_accuracy(true_ped,true_map,phased_ped,phased_map,result_statistic,result_snp)
