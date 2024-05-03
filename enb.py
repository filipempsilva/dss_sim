import numpy as np
import math
import config

resource_blocks_lte = {     # Nmbr of RBs for a given bandwidth
1.4: 6,
3: 15,
5: 25,
10: 50,
15: 75,
20: 100,
}



        
class eNB:
    def __init__(self,bdw):
        self.RB_av = [bandwidth_to_RBs_enb(bdw)]*config.nmbr_samples    # eNB RBs available in a given tti


def bandwidth_to_RBs_enb(bwd):
        if(bwd <= 0 or bwd>20 or (not(bwd==1.4) and not(bwd==3) and not(bwd==5) and not(bwd==10) and not(bwd==15) and not(bwd==20))):
            print("Invalid bandwidth value")
            return -1
        else:
            return resource_blocks_lte[bwd]
    


