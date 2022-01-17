def FRtoPed(rawdata,out,sep='\t',allele_type='Top'):
    readfrom1=True
    readfrom2=False
    global inf
    inf = {}
    start_n = 0
    for en,a in enumerate(open(rawdata)):
        start_n = start_n+1
        line=a.strip().split(sep)
        if readfrom1:
            if '[Data]' in a:
                readfrom1 = False
                readfrom2 = True
                continue
            else:
                tmp_list = [i for i in line if i!='']
                if len(tmp_list)>1:
                    inf[tmp_list[0]] = tmp_list[1]
                    
        if readfrom2:
            if 'Allele1' in a:
                snp_type = 'row'
                global alle_pos1,alle_pos2,SNPid_pos,INDid_pos
                alle_pos1 = line.index('Allele1 - '+allele_type)
                alle_pos2 = alle_pos1+1
                SNPid_pos = line.index('SNP '+'Name')
                INDid_pos = line.index('Sample '+'ID')
            elif int(inf['Num Samples']) == len(line):
                snp_type = 'matrix'
                global id_sample
                id_sample = line
            else:
                print(int(inf['Num Samples']))
                print(len(line))
                print("ERROR: The format of Finalreport is not standard!")
                sys.exit()
            readfrom2 = False
        if not (readfrom1 or readfrom2):
            break
    #if snp_type == 'row':
    #    return inf,snp_type,alle_pos1,alle_pos2,start_n,SNPid_pos,INDid_pos
    #elif snp_type == 'matrix':
    #    return inf,snp_type,id_sample,start_n
    
    out_ped = out+'.ped'
    out_map = out+'.map'
    outped = open(out_ped,'w+')
    outmap = open(out_map,'w+')
    global SNPname,conv
    SNPname = []
    anim = -1
    snp = 0
    n = 0
    
    conv={}
    for a in open(snpmap_all,'r'):
        chro,snpid,mol,pos=a.strip().split(sep,4)
        conv[snpid]=(chro,pos)    
    ###writing output ped file
    if snp_type == 'row':
        switch1 = True
        for en,a in enumerate(open(rawdata)):
            n+=1
            if switch1:
                if n < start_n:
                    continue
                else:
                    switch1 = False
                    continue
            line=a.strip().split(sep)
            snp_name=line[SNPid_pos]
            id_sample=line[INDid_pos]
            alle1=line[alle_pos1]
            alle2=line[alle_pos2]
            if alle1=='-':alle1='0'
            if alle2=='-':alle2='0'
            if n == start_n+1:
                snp=-1
                geno=[]
                name=[]
                name.append(id_sample)
            if id_sample in name:
                geno.append(alle1+' '+alle2)
                snp+=1
                if len(name)==1:
                    SNPname.append(snp_name)
                else:
                    if snp_name!=SNPname[snp]:
                        print("The order of the SNPs in the different individuals is consistent. Check "+snp_name+" and "+SNPname[snp])
                        sys.exit()
            else:
                snp=0
                anim+=1
                outped.write('1 %s 0 0 0 -9 %s\n' % (name[anim],' '.join(geno)))
                print('Finshed processing individual:',name[anim],' - Total SNPs:',len(geno))
                geno=[]
                geno.append(alle1+' '+alle2)
                name.append(id_sample)
        outped.write('1 %s 0 0 0 -9 %s\n' % (id_sample,' '.join(geno)))
        anim+=2
        ###writing output map file   
        for x in SNPname:
            if x not in conv: print("SNP: "+x+" in FinalReport is not present in SNP map!!!")
            outmap.write('%s\t%s\t0\t%s\n' % (conv[x][0],x,conv[x][1]))  

    if snp_type == 'matrix':
        switch1 = True
        global anims,genos
        anims=[]
        genos=[]
        for en,a in enumerate(open(rawdata)):
            n+=1
            line=a.strip().split(sep)
            if switch1:
                if n < start_n:
                    continue
                elif n == start_n:
                    switch1 = False
                    for i in range(len(line)):
                        anims.append(line[i])
                        genos.append([])
                    continue
            
            snp,geno=a.strip().split(sep,1)
            outmap.write('%s\t%s\t0\t%s\n' % (conv[snp][0],snp,conv[snp][1]))
            geno=geno.replace('-','0').strip().split(sep)
            for x in range(len(geno)):genos[x].append(geno[x])
                
        for x in range(len(anims)):
            gty=[genos[x][i][0]+' '+genos[x][i][1] for i in range(len(genos[x]))]
            outped.write('1 %s 0 0 0 0 %s\n' % (anims[x],' '.join(gty)))
    outped.close()
    outmap.close()
