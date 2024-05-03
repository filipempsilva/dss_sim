import numpy as np
import math
import gnb
import enb
import user
import matplotlib.pyplot as plt
import config




def split_bdw(bdw):
    return bdw/2    # Returns half the bandwidth to do an equal split between gNB and eNB


##################      Init Var      ##################


LTE_UEs = user.UEs(0)
NR_UEs = user.UEs(1)
cur_UE_lte = config.N_users_5g_min
cur_UE_5g = config.N_users_5g_min
rb_need_5g = 0
rb_need_lte = 0


##################      Initial Bandwidth      ##################


bdw_enb = split_bdw(config.bandwidth)
bdw_gnb = split_bdw(config.bandwidth)
RB_av_enb = enb.eNB(bdw_enb)
RB_av_gnb = gnb.gNB(bdw_gnb,config.numerology)


##################      Generating Traffic      ##################


for i in range(config.N_users_LTE_max):    # loops LTE users 
    for j in range(config.nmbr_samples):   # loops for every tti in the simulation
        LTE_UEs.traffic[i][j] = LTE_UEs.getNrbs(LTE_UEs.trafic_generator(LTE_UEs.type),config.mcs_lte)


for i in range(config.N_users_5g_max):    # loops 5g users 
    for j in range(config.nmbr_samples):   # loops for every tti in the simulation
        NR_UEs.traffic[i][j] = NR_UEs.getNrbs(NR_UEs.trafic_generator(NR_UEs.type),config.mcs_5g)


##################       Assignment of RBs      ##################


for i in range(config.nmbr_samples):
    if(i==8000):
        cur_UE_lte = cur_UE_lte+1
    if(i==10000):
        cur_UE_5g = cur_UE_5g+1
    if(i==15000):
        cur_UE_lte = cur_UE_lte+1
    if(i==18000):
        cur_UE_5g = cur_UE_5g+1
    if(i==24000):
        cur_UE_5g = cur_UE_5g+1



##################      Debug      ##################


#print(np.size(RB_av_gnb.RB_av))
#print(RB_av_gnb.RB_av)

"""
aux1=0
for i in LTE_UEs.traffic:
    print('\t'.join(map(str, i)))
    print("||")
    aux1=aux1+1
    print(aux1)


aux1 = 0
for i in NR_UEs.traffic:
    print('\t'.join(map(str, i)))
    print("||")    
    aux1=aux1+1
    print(aux1)
"""