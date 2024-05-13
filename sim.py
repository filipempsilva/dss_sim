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

RbNotAlooc_eNB = np.zeros(config.nmbr_samples)  # Number of RBs that the eNB coudnt allocate at a given tti
RbNotAlooc_gNB = np.zeros(config.nmbr_samples)  # Number of RBs that the gNB coudnt allocate at a given tti

time = np.arange(0,config.nmbr_samples,config.step)

LTE_UEs = [user.UEs]*config.N_users_LTE_max # Array of LTE UEs
NR_UEs = [user.UEs]*config.N_users_5g_max   # Array of 5G UEs

for i in range(len(LTE_UEs)):
    LTE_UEs[i] = user.UEs(0,i+1,config.priority_default)    # Init each element of the array

for i in range(len(NR_UEs)):
    NR_UEs[i] = user.UEs(1,i+1,config.priority_default)     # Init each element of the array


cur_UE_lte = config.N_users_LTE_min  # Starting and Current number of LTE UEs
cur_UE_5g = config.N_users_5g_min   # Starting and Current number of 5G UEs
rb_need_5g = [0]*config.nmbr_samples    # Rbs that are needed at a given instant by the lte UEs
rb_need_lte = [0]*config.nmbr_samples   # Rbs that are needed at a given instant by the 5G UEs

##################      Initial Bandwidth      ##################


bdw_enb = split_bdw(config.bandwidth)
bdw_gnb = split_bdw(config.bandwidth)
RB_av_eNB = enb.eNB(bdw_enb)    # Array of RBs available in the eNB
RB_av_gNB = gnb.gNB(bdw_gnb,config.numerology)  # Array of RBs available in the gNB


##################      Generating Traffic      ##################


for i in range(len(LTE_UEs)):    # loops LTE users 
    for j in range(config.nmbr_samples):   # loops for every tti in the simulation
        LTE_UEs[i].traffic[j] = LTE_UEs[i].getNrbs(LTE_UEs[i].trafic_generator(LTE_UEs[i].type),config.mcs_lte)


for i in range(len(NR_UEs)):    # loops 5g users 
    for j in range(config.nmbr_samples):   # loops for every tti in the simulation
        NR_UEs[i].traffic[j] = NR_UEs[i].getNrbs(NR_UEs[i].trafic_generator(NR_UEs[i].type),config.mcs_5g)


##################       Assignment of RBs      ##################


open('logs.txt', 'w').close()   # Cleaning log file before assignment loop
print("\n\n                 Running Simulation\n                  ")
with open("logs.txt", "a") as log:
    print("\n\n                 Running Simulation\n                  ", file=log)


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

    for k in range(cur_UE_lte):
        rb_need_lte[i] = rb_need_lte[i] + LTE_UEs[k].traffic[i] # Rbs needed to fufil the LTE_UEs traffic at a given time 

    for k in range(cur_UE_5g):
        rb_need_5g[i] = rb_need_5g[i] + NR_UEs[k].traffic[i]    # Rbs needed to fufil the NR_UEs traffic at a given time 


    if(rb_need_lte[i] <= RB_av_eNB.RB_av[i]):   #   Case where there are sufficient resources in the eNB
        RB_av_eNB.RB_av[i] = RB_av_eNB.RB_av[i] - rb_need_lte[i]
        RbNotAlooc_eNB[i] = 0
    else:   #   Case where there aren't sufficient resources in the eNB
        print("Insufficent resources at the eNB, allocating all the possible RBs")
        RbNotAlooc_eNB[i] = -(RB_av_eNB.RB_av[i]-rb_need_lte)       # Number of RBs that can't be allocated
        for j in range(cur_UE_lte):     # Now we iterate every 4G_UE to assign RBs if possible
            if(LTE_UEs[j].traffic[i]>RB_av_eNB.RB_av[i]):     # Case where it is not possible to assign all RBs for this UE
                for ii in range(j,cur_UE_lte):  # Since not possible, will assign what is possible. If not possible will add that traffic to the next time_slot 
                    LTE_UEs[ii].traffic[i]-=RB_av_eNB.RB_av[i]  
                    RB_av_eNB.RB_av[i]=0  # All the RBs were assigned    
                    LTE_UEs[ii].traffic[i+1]+=LTE_UEs[ii].traffic[i]    #   The RBs that were not assigned, pass to the next instant
                    if(LTE_UEs[ii].prio != 1):
                        LTE_UEs[ii].prio -= 1   # Lowering the priority so this UE is first in line next           
                break
            else:   # Case where it is still possible to assign RBs for this UE
                RB_av_eNB.RB_av[i]-=LTE_UEs[j].traffic[i]    

    if(rb_need_5g[i] <= RB_av_gNB.RB_av[i]):    #   Case where there are sufficient resources in the gNB
        RB_av_gNB.RB_av[i] = RB_av_gNB.RB_av[i] - rb_need_5g[i]
        RbNotAlooc_gNB[i] = 0
    else:        #   Case where there aren't sufficient resources in the gNB
        print("Insufficent resources at the gNB, allocating all the possible RBs")
        RbNotAlooc_gNB[i] = -(RB_av_gNB.RB_av[i]-rb_need_5g)
        for j in range(cur_UE_5g):      # Now we iterate every 4G_UE to assign RBs if possible
            if(NR_UEs[j].traffic[i]>RB_av_gNB.RB_av[i]):      # Case where it is not possible to assign all RBs for this UE
                for ii in range(j,cur_UE_5g):       # Since not possible, will assign what is possible. If not possible will add that traffic to the next time_slot 
                    NR_UEs[ii].traffic[i]-=RB_av_gNB.RB_av[i]  
                    RB_av_gNB.RB_av[i]=0      # All the RBs were assigned    
                    NR_UEs[ii].traffic[i+1]+=NR_UEs[ii].traffic[i]      #   The RBs that were not assigned, pass to the next instant
                    if(NR_UEs[ii].prio != 1):
                        NR_UEs[ii].prio -= 1        # Lowering the priority so this UE is first in line next         
                break       #   If there aren't more resources, we go to the next frame (tti)
            else:   # Case where it is still possible to assign RBs for this UE
                RB_av_gNB.RB_av[i]-=LTE_UEs[j].traffic[i]

    with open("logs.txt", "a") as log:
        print("t=",i, file=log)
        print(RB_av_eNB.RB_av[i]," || ",rb_need_lte[i], file=log)
        print(RB_av_gNB.RB_av[i]," || ",rb_need_5g[i],"\n", file=log)


    print("t=",i,"ms",end='\r')  #   Prints the time
    #print(RB_av_eNB.RB_av[i]," || ",rb_need_lte[i])
    #print(RB_av_gNB.RB_av[i]," || ",rb_need_5g[i],"\n")
    

##################       Plots to visualize data      ##################


plt.figure()
plt.title("Time Vs Available RBs")
plt.plot(time, RB_av_eNB.RB_av)
plt.plot(time, RB_av_gNB.RB_av)

plt.legend(["RBs Available in eNB", "RBs Available in gNB"])
plt.savefig('RBs_av_OT.png',bbox_inches='tight')
plt.show()


##################      Debug      ##################


"""
print(np.size(RB_av_gnb.RB_av))
print(RB_av_gnb.RB_av)


for i in range(len(LTE_UEs)):
    print(LTE_UEs[i].traffic)
    
for i in range(len(NR_UEs)):
    print(NR_UEs[i].traffic)
"""