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


LTE_UEs = [user.UEs]*config.N_users_LTE_max
NR_UEs = [user.UEs]*config.N_users_5g_max

for i in range(len(LTE_UEs)):
    LTE_UEs[i] = user.UEs(0)

for i in range(len(NR_UEs)):
    NR_UEs[i] = user.UEs(1) 


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


for i in range(len(LTE_UEs)):    # loops LTE users 
    for j in range(config.nmbr_samples):   # loops for every tti in the simulation
        LTE_UEs[i].traffic[j] = LTE_UEs[i].getNrbs(LTE_UEs[i].trafic_generator(LTE_UEs[i].type),config.mcs_lte)


for i in range(len(NR_UEs)):    # loops 5g users 
    for j in range(config.nmbr_samples):   # loops for every tti in the simulation
        NR_UEs[i].traffic[j] = NR_UEs[i].getNrbs(NR_UEs[i].trafic_generator(NR_UEs[i].type),config.mcs_5g)


##################       Assignment of RBs      ##################


for i in range(config.nmbr_samples):
    if(i==8000):
        cur_UE_lte = cur_UE_lte+1       # Adding users at different timestamps. 
    if(i==10000):                       # t=8s; t=10; t=15; t=18; t=24. 
        cur_UE_5g = cur_UE_5g+1              
    if(i==15000):
        cur_UE_lte = cur_UE_lte+1
    if(i==18000):
        cur_UE_5g = cur_UE_5g+1
    if(i==24000):
        cur_UE_5g = cur_UE_5g+1


##################      Debug      ##################

"""
print(np.size(RB_av_gnb.RB_av))
print(RB_av_gnb.RB_av)


for i in range(len(LTE_UEs)):
    print(LTE_UEs[i].traffic)
    
for i in range(len(NR_UEs)):
    print(NR_UEs[i].traffic)
"""