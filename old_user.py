import numpy as np
import math

#old_user

resource_blocks_lte = {     # Nmbr of RBs for a given bandwidth
1.4: 6,
3: 15,
5: 25,
10: 50,
15: 75,
20: 100,
}


def init_user (type):
    if type == 0:
        print("LTE user is being created")
    elif type == 1:
        print("5GNR user is being created")
    else:
        print("Invalid Type. Type 0 -> LTE || Type 1 -> 5GNR")
        return -1


def bandwidth_to_RBs_enb(bwd):
    if(bwd <= 0 or bwd>20 or (not(bwd==1.4) and not(bwd==3) and not(bwd==5) and not(bwd==10) and not(bwd==15) and not(bwd==20))):
        print("Invalid bandwidth value")
        return -1
    else:
        return resource_blocks_lte[bwd]
    

def riv_lte (type,rbStart,NRb,bwd):
    if(type!=0):
        print("Not a LTE user")
        return -1
    else:
        RB = bandwidth_to_RBs_enb(bwd)
        if((NRb-1)<=(RB/2)):
            return RB*(NRb-1)+rbStart
        else:
            return RB*(RB-NRb+1)+(RB-1-rbStart)
