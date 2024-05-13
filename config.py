

##################      Global Vars     ##################


tti = 1 # smallest time granularity (1ms)
sim_time = 30000  # 30s simulation time 
step = 1    # 1 ms step in sim
nmbr_samples = int(sim_time/tti)
numerology = 0

bandwidth = 40
N_users_LTE_min = 2
N_users_LTE_max = 4
N_users_5g_min = 3
N_users_5g_max = 6
mcs_lte = 24
mcs_5g = 26
priority_default = 5