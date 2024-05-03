import numpy as np
import math

# old_eNB

resource_blocks_lte = {     # Nmbr of RBs for a given bandwidth
1.4: 6,
3: 15,
5: 25,
10: 50,
15: 75,
20: 100,
}


resource_block_grp_lte = {  # Nmbr of RBs in a RBG (RBGroup) for a given bandwidth [type 0 allocation]
1.4: 1,
3: 2,
5: 2,
10: 3,
15: 4,
20: 4,
}

def bandwidth_to_RBs_enb(bwd):
    if(bwd <= 0 or bwd>20 or (not(bwd==1.4) and not(bwd==3) and not(bwd==5) and not(bwd==10) and not(bwd==15) and not(bwd==20))):
        print("Invalid bandwidth value")
        return -1
    else:
        return resource_blocks_lte[bwd]
    

def bandwidth_to_RBGsize(bwd):  # For type 0 allocation, but won't be used probably (less granularity than type2)
    if(bwd <= 0 or bwd>20 or (not(bwd==1.4) and not(bwd==3) and not(bwd==5) and not(bwd==10) and not(bwd==15) and not(bwd==20))):
        print("Invalid bandwidth value")
        return -1
    else:
        return resource_block_grp_lte[bwd]


def build_bitmap_enb(bwd):
    rb=bandwidth_to_RBs_enb(bwd)
    rbg=bandwidth_to_RBGsize(bwd)
    bitmap_enb = [0]*math.floor(rb/rbg)
    return bitmap_enb


def alloc_type2(riv,bwd,bitmap_enb):
    print("Allocation type 2")
    rb=bandwidth_to_RBs_enb(bwd)
    rbnmbr = math.floor(riv/rb)+1
    rbstart = riv%rb
    if(rbnmbr<0 or rbnmbr>rb or rbstart < 0 or rbstart > rb+1):
        print("Invalid riv")
        return -1
    for i in range(rbstart,rbstart+rbnmbr):
        if(bitmap_enb[i]==0):
            bitmap_enb[i]=1
        else:
            print("Couldnt allocate RBs")
            return -1
    print(rbnmbr,"RBs allocated")
    return bitmap_enb


def alloc_type0(bitmap_enb,RBs,bwd):
    NRbg=RBs/math.ceil(bandwidth_to_RBGsize(bwd))
    
    # allocation algorithm (next-fit?)


"""
def alloc_type0(bitmap_user,bitmap_enb):  
    print("Allocation type 0")
    for i in bitmap_user:
        if(bitmap_user[i]==1 and bitmap_enb[i]==0):
            bitmap_enb[i] = 1
            print("Resources allocated")
            return bitmap_enb
        else:
            print("Couldnt allocate RBs")
            return -1 
"""


"""
def RB_alloc_enb(rb_enb,rb_user_enb):
    if(rb_enb < rb_user_enb):
        print("Can't allocate requested RBs in the eNB")
        return 0    
    else:
        rb_enb = rb_enb-rb_user_enb
        return rb_enb
"""
print(build_bitmap_enb(1.4))

#print(alloc_type2(259,1.4,build_bitmap_enb(1.4)))