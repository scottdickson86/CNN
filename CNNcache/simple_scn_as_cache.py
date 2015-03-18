# -*- coding: utf-8 -*-
import math
import numpy as np
import copy
from random import randint

#input characteristics
message_len = 64*8
clusters = 4 #must be at least 2 
input_distribution_type = 1 #uniformly distributed
#input_distribution_type = 2 #non-uniform; concentrated on certain areas
input_distribution = ""
if input_distribution_type == 1:
    input_distribution = "uniform"
elif input_distribution_type == 2:
    input_distribution = "non-uniform"

bits_per_cluster =  int(message_len/clusters)
neurons_per_cluster = int(math.pow(2, bits_per_cluster))
storage_blocks = clusters*(clusters-1)
storage_blocks_indexing = []
full_message = []

def show_network_config():
    print ("-------------------------------------------------------------------")
    print ("input                 : ", message_len, " bits.")
    print ("input distribution    : ",input_distribution)
    #print (" -set of inputs       : ", int(math.pow(2, message_len)), " messages.")
    print ("num of clusters       : ", clusters)    
    print (" -bits/clusters       : (", message_len, "bits/", clusters, "clusters) = ", bits_per_cluster)    
    print (" -neurons/clusters    :  2^(", bits_per_cluster, "bits/cluster) = ", neurons_per_cluster)
    print ("num of neurons total  : ", neurons_per_cluster*clusters)    
    print ("num of storage blocks : ", storage_blocks)
    print (" -size of each block  : ", neurons_per_cluster, "bits x", neurons_per_cluster, "bits")
    print ("link storage matrix   : ",clusters*(clusters-1)*neurons_per_cluster, "x" ,message_len)
    print ("-------------------------------------------------------------------")

#storage matrix is made up of these dimensions:
# -rows = storage blocks * neurons per cluster 
# -colums = neurons per cluster
#create each storage block first -> square matrix
# -rows = number of neurons per cluster
# -columns = rows 
def initialize_link_storage_module ():
    row = []
    col_i = 0
    while col_i < neurons_per_cluster:
        row.append(0)
        col_i = col_i + 1
    #row[] is an array with zeroes 
    block = []
    row_i = 0
    while row_i < neurons_per_cluster:
        block.append(row)
        row_i = row_i + 1
    #block is now a square matrix
    #next create storage matrix = num of storage blocks stiched vertically
    link_storage_mod = []
    block_i = 0
    while block_i < storage_blocks:
        link_storage_mod.append(block)
        block_i = block_i+ 1
    #link_storage_mod is now a 3-dimensional matrix
    link_storage_mod_array = np.array(link_storage_mod)
    #map which storage blocks store which neuron-cluster pairs
    block_i = 0
    while block_i < storage_blocks:
        cluster1 = 0
        while cluster1 < clusters:
            cluster2 = 0
            while cluster2 < clusters:
                if cluster1 != cluster2:
                    row = cluster1
                    col = cluster2
                    storage_blocks_indexing.append([row, col])
                    block_i = block_i + 1
                cluster2 = cluster2 +1
            cluster1 = cluster1 + 1
    return link_storage_mod_array
    #print (storage_blocks_indexing)

#input random data
def create_input_set(input_range, input_size_total):
    #input_file = open("full_input.txt", "w")
    input_i = 0
    input_set_array = []
    unifrom_dist = np.random.uniform(low=0, high=input_range, size=input_size_total)
    while input_i < input_size_total:
        bit_i = 0
        input_m = ""
        if input_distribution_type == 1:
            while bit_i < message_len:
                input_m = input_m + str(randint(0,1))
                bit_i = bit_i + 1
        elif input_distribution_type == 2:
            input_m = ("{0:0"+str(message_len)+"b}").format(int(unifrom_dist[input_i]))
        print ("random input", input_i+1, ": ", input_m)
        #print ("mapping:")
        activated_neurons = []
        subm_i = 0
        full_message_str = ""
        full_message_array = []
        while subm_i < clusters:
            start_i = (subm_i*bits_per_cluster)
            end_i = start_i + bits_per_cluster
            cluster_bits = input_m[start_i:end_i]
            full_message_array.append(cluster_bits)
            cluster_int_index = int(cluster_bits, 2)
            activated_neurons.append(cluster_int_index)     
            cluster_int_index_str = str(cluster_int_index)
            if len(cluster_int_index_str) == 1:
                cluster_int_index_str = " "+cluster_int_index_str
            #print ("sub-message ", subm_i, ": ", cluster_bits, "---> neuron ", cluster_int_index_str, "(cluster",subm_i,")")
            full_message_str = full_message_str + cluster_bits
            subm_i = subm_i + 1
        input_set_array.append(full_message_array)
        #input_file.write(full_message_str+"\n")
        #print ("--------------")
        input_i = input_i + 1 
    #input_file.close()
    return input_set_array

def write_data(link_storage_mod_array, full_message_array):
    #store
    #print ("link storage module:")
    storage_block_i = 0
    for row_col_pair in storage_blocks_indexing:
        subm1_int = int(full_message_array[row_col_pair[0]],2)#row
        subm2_int = int(full_message_array[row_col_pair[1]],2)#col
        storage_block_i_str = str(storage_block_i)
        if len(storage_block_i_str) ==1:
            storage_block_i_str = " "+storage_block_i_str
        subm1_int_str = str(subm1_int)
        if len(subm1_int_str)==1:
            subm1_int_str = " "+subm1_int_str
        subm2_int_str = str(subm2_int)
        if len(subm2_int_str)==1:
            subm2_int_str = " "+subm2_int_str
        #print ("storage block",storage_block_i_str,":neuron",subm1_int_str,"cluster(",row_col_pair[0],")-->nueron",subm2_int_str,"cluster(",row_col_pair[1],")")       
        link_storage_mod_array[storage_block_i][subm1_int][subm2_int]=1      
        storage_block_i = storage_block_i + 1
    #print ("--------------")
    #end of data storage

#search data
#first create partial input messages
#print ("search ")
def erase_input_bits(input_size_total, input_set_array):
    #erase bits - can be removed for cache simulation
    partial_input_set = [] #contains the partial input to be searched
    input_i = 0
    while input_i < input_size_total:
        full_message_array = []    
        sub_m_i = 0
        while sub_m_i < clusters:
            full_message_array.append(input_set_array[input_i][sub_m_i])
            sub_m_i = sub_m_i + 1
        #randomly generate the number of bits to remove
        #bits_erase_total = randint(0,(message_len/2)) #can't remove all; at least one sub-message must remain 
        bits_erase_total = 0 # no erased bits for cache
        #randomly generate the indexes of the submessages to remove
        erase_i = 0
        while erase_i < bits_erase_total:
            index_remove = randint(0,clusters-1)
            bit_remove = randint(0, bits_per_cluster-1)
            if full_message_array[index_remove][bit_remove] == "x": #already removed; 
                pass #try again
            else:
               full_message_array[index_remove]  = full_message_array[index_remove][0:bit_remove]+"x"+full_message_array[index_remove][bit_remove+1:bits_per_cluster]
               erase_i = erase_i + 1
        partial_input_set.append(full_message_array)
        input_i = input_i + 1
    return partial_input_set

def search_data(partial_input_set, link_storage_mod_array):
    #end of erase bits - can be removed for cache simulation
    input_i = 0 
    total_iterations = 0
    successful_match_count = 0
    iterations_success = 0
    errors_count = 0
    miss_count = 0
    iterations_error = 0
    full_message_array = []
    for entry in partial_input_set:
        full_message_array = entry
        iteration_count = 0
        print ("search input",input_i+1,":",entry)
        sub_m_i = 0
        neuron_candidates = []#2d array; internal arrays are arrays for candidate nuerons 1 array per submessage 
        for sub_m in entry:
            #print ("//sub-message",sub_m_i,":", entry[sub_m_i],"")
            neuron_candidates.append([])
            bit_i_sub_m = 0
            missing_bits = 0
            for char in sub_m:
                if char == "x":
                    #print ("                  bit",bit_i_sub_m,"is missing.")
                    missing_bits = missing_bits + 1
                bit_i_sub_m = bit_i_sub_m + 1
            if missing_bits==0:
                #print ("sub-message",sub_m_i,"has no missing bits.")
                pass
            #check possible matches
            score_candidate = bits_per_cluster - missing_bits
            neuron_i = 0
            while neuron_i < neurons_per_cluster:
                neuron_score = 0
                #format: '{0:08b}'.format(6) --> convert integer 6 to 8-bit binary
                neuron_i_bin_str = ("{0:0"+str(bits_per_cluster)+"b}").format(neuron_i)
                neuron_i_int_str = str(neuron_i)
                if len(neuron_i_int_str) == 1:
                    neuron_i_int_str = " "+neuron_i_int_str
                #print ("neuron_i_str",neuron_i_str)
                bit_i = 0
                for bit in neuron_i_bin_str:
                    if bit == sub_m[bit_i]:
                        neuron_score = neuron_score + 1
                    bit_i = bit_i + 1
                if neuron_score == score_candidate:
                    #print ("neuron", neuron_i_int_str, "(",neuron_i_bin_str,") in cluster",sub_m_i,"is a candidate.")
                    neuron_candidates[sub_m_i].append(neuron_i)
                neuron_i = neuron_i + 1
            sub_m_i = sub_m_i + 1
        #deactivate candidate neurons that do not have a link to at least one candidate neuron in ALL the clusters
        #print ("candidate neurons:")
        candidate_cluster_i = 0
        for candidate_cluster in neuron_candidates:
            #print (" cluster",candidate_cluster_i,":",candidate_cluster)
            candidate_cluster_i = candidate_cluster_i + 1
        #print ("activating fully linked candidates...")
        active_neurons_cluster_linked = [] #neurons per cluster with links to at least one candidate neuron in all clusters
        cluster_i = 0
        iteration_count = iteration_count + 1
        for cluster in neuron_candidates:
            active_neurons_cluster_linked.append([])
            for candidate_n in cluster:     
                candidate_n_active = True
                storage_block_i = 0
                for row_col_pair in storage_blocks_indexing:
                    cluster1 = row_col_pair[0]
                    cluster2 = row_col_pair[1] #index to array inside candidate_neurons to compare against
                    if cluster_i == cluster1:#compare
                        #is there a link between candidate_n and the nuerons in cluster2?
                        link_found = False
                        for candidate_n_second in neuron_candidates[cluster2]:
                            if link_storage_mod_array[storage_block_i][candidate_n][candidate_n_second]==1:
                                #print ("link between neuron",candidate_n,"(cluster(",cluster1,") and neuron",candidate_n_second,"(cluster(",cluster2,") found.")
                                link_found = True #continue as long as candidate_n has links to pair cluster
                                break #at least one active link is needed to keep neuron activated
                        if not link_found: #seaarch finished one cluster and no link is found
                            candidate_n_active = False
                            break # no need to continue comparing against other clusters if at least one missing link is found 
                    storage_block_i = storage_block_i + 1
                if candidate_n_active:
                    active_neurons_cluster_linked[cluster_i].append(candidate_n)
                    candidate_n_str = str(candidate_n)
                    if len(candidate_n_str)==1:
                        candidate_n_str = " "+candidate_n_str
                    #print ("neuron", candidate_n_str, "in cluster",cluster_i,"has links to all other clusters.")
            cluster_i = cluster_i + 1
    
        #generate match
        cluster_i = 0
        match_str = ""
        unique_match_found = True
        store_data = False
        multiple_activated_neurons = []
        #print ("active_neurons:")
        active_neurons_cluster_i = 0
        multiple_active_neurons_count = 0
        for active_neurons_cluster in active_neurons_cluster_linked:
            #print (" cluster",active_neurons_cluster_i,":",active_neurons_cluster)
            multiple_active_neurons_count = multiple_active_neurons_count + len(active_neurons_cluster)
            active_neurons_cluster_i = active_neurons_cluster_i + 1
        #print ("number of active neurons:",multiple_active_neurons_count)
        for cluster in active_neurons_cluster_linked:
            multiple_activated_neurons.append([])
            if len(cluster)>1:
                print ("...multiple activated neurons",cluster,"in cluster",cluster_i)
                for n_i in cluster:
                    multiple_activated_neurons[cluster_i].append(n_i)
                unique_match_found = False
                store_data = False
            elif len(cluster)==1:
                match_str = match_str + ("{0:0"+str(bits_per_cluster)+"b}").format(cluster[0]) + " "
                unique_match_found = True
                store_data = False
            elif len(cluster)==0:
                #cache functionality addition - no match found; needs to be stored    
                unique_match_found = False
                store_data = True
                print("...cache miss! storing data to CNN...")
                #print ("full_message_array",full_message_array)
                write_data(link_storage_mod_array, full_message_array)
                miss_count = miss_count + 1
                break
            cluster_i = cluster_i + 1
        if unique_match_found and (not store_data):
            successful_match_count = successful_match_count + 1
            iterations_success = iterations_success + iteration_count
            print ("...cache hit (hit rate:",round((successful_match_count/(input_i+1))*100,3),"%): ",match_str)
            print (".....in 1 iteration.")
        elif (not unique_match_found) and (not store_data):
            print ("...attempting to eliminate multiple activated neurons...")
            pass 
        if (not unique_match_found) and (not store_data):
            continue_deactiving = True
            while continue_deactiving:
                active_neurons = []
                cluster_i = 0
                multiple_active_neurons_count_prev = 0
                iteration_count = iteration_count + 1
                for cluster in active_neurons_cluster_linked:
                    multiple_active_neurons_count_prev = multiple_active_neurons_count_prev + len(cluster)
                    active_neurons.append([])
                    for candidate_n in cluster:     
                        candidate_n_active = True
                        storage_block_i = 0
                        for row_col_pair in storage_blocks_indexing:
                            cluster1 = row_col_pair[0]
                            cluster2 = row_col_pair[1] #index to array inside candidate_neurons to compare against
                            if cluster_i == cluster1:#compare
                                #is there a link between candidate_n and the nuerons in cluster2?
                                link_found = False
                                for candidate_n_second in active_neurons_cluster_linked[cluster2]:
                                    if link_storage_mod_array[storage_block_i][candidate_n][candidate_n_second]==1:
                                        #print ("link between neuron",candidate_n,"(cluster(",cluster1,") and neuron",candidate_n_second,"(cluster(",cluster2,") found.")
                                        link_found = True #continue as long as candidate_n has links to pair cluster
                                        break #at least one active link is needed to keep neuron activated
                                if not link_found: #seaarch finished one cluster and no link is found
                                    candidate_n_active = False
                                    break # no need to continue comparing against other clusters if at least one missing link is found 
                            storage_block_i = storage_block_i + 1
                        if candidate_n_active:
                            active_neurons[cluster_i].append(candidate_n)
                            candidate_n_str = str(candidate_n)
                            if len(candidate_n_str)==1:
                                candidate_n_str = " "+candidate_n_str
                            #print ("neuron", candidate_n_str, "in cluster",cluster_i,"has links to active neurons.")
                    cluster_i = cluster_i + 1
                #print ("active_neurons:")
                active_neurons_cluster_i = 0
                multiple_active_neurons_count = 0
                for active_neurons_cluster_elimination in active_neurons:
                    #print (" cluster",active_neurons_cluster_i,":",active_neurons_cluster_elimination)
                    multiple_active_neurons_count = multiple_active_neurons_count + len(active_neurons_cluster_elimination)
                    active_neurons_cluster_i = active_neurons_cluster_i + 1
                #print ("number of active neurons:",multiple_active_neurons_count)
                active_neurons_cluster_linked = []
                active_neurons_cluster_linked = copy.deepcopy(active_neurons)
                if multiple_active_neurons_count == clusters:
                    match_str = ""
                    for cluster in active_neurons:
                        match_str = match_str + ("{0:0"+str(bits_per_cluster)+"b}").format(cluster[0]) + " "
                    print ("...cache hit!:",match_str)
                    print ("......after ",iteration_count,"iterations.")
                    successful_match_count = successful_match_count + 1
                    iterations_success = iterations_success + iteration_count
                    continue_deactiving = False
                elif multiple_active_neurons_count<multiple_active_neurons_count_prev:
                    print ("...continue iteration to eliminate multiple active neurons")
                    continue_deactiving = True
                else:
                    print ("...error: end iteration. number of active nuerons hasn't changed.")
                    continue_deactiving = False
                    errors_count = errors_count + 1
                    iterations_error = iterations_error + iteration_count
        input_i = input_i + 1
        print ("--------------")
        total_iterations = total_iterations + iteration_count
    #show network performance
    print ("input size        :",len(partial_input_set))
    print ("input distribution:", input_distribution)
    print ("total # iterations:",total_iterations," (iterations to process all",len(partial_input_set),"input)")
    print ("avgerage iteration:",round(total_iterations/len(partial_input_set), 3), "iternations/input")
    print ("---------------")
    print ("total # of hits   :",successful_match_count, "(",round((successful_match_count/len(input_set))*100,3),"%)")
    if successful_match_count>0:
        print ("--avg iter/hit    :",round(iterations_success/successful_match_count, 3), "iterations to generate a match"), 
    print ("total # of miss   :",miss_count)
    print ("total # of errors :",errors_count)
    if errors_count>0:
        print ("--avg iter/error  :",round(iterations_error/errors_count, 3), "iterations to declare an error"), 

        
def create_input_redundancy(input_set_array, base_2_num_limit):
    input_set_array_copy = copy.deepcopy(input_set_array)
    total_input_to_repeat = 4
    input_for_repeat_index = []
    count = 0
    while count < total_input_to_repeat:
        index = randint(0,len(input_set_array)-1) #index to repeat
        if not(index in input_for_repeat_index): #make sure index is not already generated
            input_for_repeat_index.append(index)
            count = count + 1
    input_for_repeat = []
    for index in input_for_repeat_index:
        input_for_repeat.append(input_set_array[index])
    max_repeat = int(len(input_set_array)/total_input_to_repeat) #equal opportunity
    #print ("total_input_to_repeat",total_input_to_repeat)
    #print ("max_repeat external",max_repeat)
    remaining_repeat_slots = len(input_set_array)-total_input_to_repeat
    input_repeat_count = []
    count = 0
    while count < len(input_for_repeat):
        repeat_count = randint(2,max_repeat) #repeat once (2) or at max repeat
        input_repeat_count.append(repeat_count)
        remaining_repeat_slots = remaining_repeat_slots - repeat_count
        count = count + 1
        #max_repeat = remaining_repeat_slots - 2*(len(input_for_repeat)-count) #remove equal opportunity; the current input index can be repeated at any number as long as the the the remaining indexes can be repeated at least once 
        if total_input_to_repeat!=count:
            max_repeat = int(remaining_repeat_slots/(total_input_to_repeat-count))
        else:
            max_repeat = remaining_repeat_slots
    repeat_index_status = []
    for item in input_set_array:
        repeat_index_status.append(0)
    index = 0
    for repeat_limit in input_repeat_count:
        count = 0
        while count < repeat_limit:
            valid_slot_generated = False    
            index_to_replace = 0
            while not valid_slot_generated:
                index_to_replace = randint(0,len(input_set_array)-1)
                if repeat_index_status[index_to_replace]==0:
                    repeat_index_status[index_to_replace]=1
                    valid_slot_generated = True
            input_set_array_copy[index_to_replace] = input_for_repeat[index]
            count = count + 1
        index = index + 1
    #write to file
    input_file = open("full_input.txt", "w")
    for message_input in input_set_array_copy:
        message_input_str = ""
        for sub_message in message_input:
            message_input_str = message_input_str + sub_message
        input_file.write(message_input_str+"\n")
    input_file.close()
    return input_set_array_copy

show_network_config()
link_storage_mod_arr = initialize_link_storage_module()
base_2_num = 12
range_input = math.pow(2,base_2_num)-1
total_input_size = math.pow(2,base_2_num)
input_set = create_input_set(range_input, total_input_size)
input_set_redundant = create_input_redundancy(input_set, base_2_num)#random - to allow hits
#partial_input_set_array = erase_input_bits(total_input_size, input_set)
search_data(input_set_redundant, link_storage_mod_arr)
