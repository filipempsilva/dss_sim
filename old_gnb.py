import numpy as np
import math

# old_gNB

resource_blocks_15scs = {
5: 25,
10: 52,
15: 79,
20: 106,
25: 133,
30: 160,
40: 216,
50: 270,
}

resource_blocks_30scs = {
5: 11,
10: 24,
15: 38,
20: 51,
25: 65,
30: 78,
40: 106,
50: 133,
60: 162,
70: 189,
80: 217,
90: 245,
100:273,
}

resource_blocks_60scs = {
10: 11,
15: 18,
20: 24,
25: 31,
30: 38,
40: 51,
50: 65,
60: 79,
70: 93,
80: 107,
90: 121,
100: 135,
}

def bandwidth_to_RBs_gnb(bwd, num):
    if(bwd <= 0 or not(bwd%5==0) or bwd>100):
        print("Invalid bandwidth value")
        return 0
    else:
        if num == 0:
            return resource_blocks_15scs[bwd]
        elif num == 1:
            return resource_blocks_30scs[bwd]
        elif num == 2:
            return resource_blocks_60scs[bwd]
        else:   
            print("Invalid Numerology")
            return 0


def RB_alloc_gnb(rb_gnb,rb_user_gnb):
    if(rb_gnb < rb_user_gnb):
        print("Can't allocate requested RBs in the gNB")
        return -1    
    rb_gnb = rb_gnb-rb_user_gnb
    return rb_gnb






print(bandwidth_to_RBs_gnb(40,0))
print(bandwidth_to_RBs_gnb(400,0))
print(bandwidth_to_RBs_gnb(40.3,1))
print(bandwidth_to_RBs_gnb(0,0))
print(bandwidth_to_RBs_gnb(40,1))

            
