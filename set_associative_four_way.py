# -*- coding: utf-8 -*-
"""
Created on Mon Mar  9 16:17:40 2015

@author: scottdicksondagondon
"""
import math
import numpy as np

def update_lru(set_current, clock_hand_index_old):
    lru_bit_array[set_current][clock_hand_index_old] = 1
    #move hand
    #if hand is in the last index, set it back to zero
    clock_hand_index_new = 0
    if clock_hand_index_old == (len(lru_bit_array[set_current])-1):
        clock_hand_index_new = 0
    else:
        clock_hand_index_new = clock_hand_index_old + 1
    hand_moved = False
    #print(lru_hand_array[set_current])
    #print("----")
    #print(lru_hand_array[0])
    while (not hand_moved):
        while clock_hand_index_new < len(lru_bit_array[set_current]):
            #print ("clock_hand_index_new",clock_hand_index_new)
            #print ("lru_bit[set_current]",lru_bit[set_current][clock_hand_index_new])
            if lru_bit_array[set_current][clock_hand_index_new] == 1:
                #print("continue finding an index to settle hand into")
                pass
                #continue finding an index to settle hand into
            else:
                #move hand
                lru_hand_array[set_current][clock_hand_index_new] = 1
                clock_hand_index_new_prev = clock_hand_index_new - 1
                if clock_hand_index_new_prev == -1:
                    clock_hand_index_new_prev = len(lru_bit_array[set_current])-1
                lru_hand_array[set_current][clock_hand_index_new_prev] = 0
                hand_moved = True
                #print ("new clock_hand_index", clock_hand_index_new)
                #print ("clock_bit should be zero:",lru_bit_array[set_current][clock_hand_index_new])
                break
            clock_hand_index_new = clock_hand_index_new + 1
        #if search completed and hand was not moved, set all bits to zero and start to hand index 0 
        if (not hand_moved):
            row_i = 0
            while row_i < len(lru_hand_array[set_current]):
                lru_bit_array[set_current][row_i] = 0
                lru_hand_array[set_current][row_i] = 0                
                row_i = row_i + 1
            clock_hand_index_new = 0
            lru_hand_array[set_current][clock_hand_index_new] = 1
    print ("end of lru")

input_file = open("full_input.txt", "r")
input_set = []
for line in input_file:
    input_word = line.strip()
    input_set.append(input_word)
input_file.close()

cache_size = 1024 #blocks
input_length = 32 #bits
set_associative_count = 4 #way 
set_length = (int)(math.log(set_associative_count, 2))
tag_length = 22 #bits
index_length = 8 #bits
offset_length = 2 #bits

cache_vbit = []
cache_tag = []
cache_data = []
#number of sets = set_associative_count
#each cache index or row will have "set_associative_count" number of arrays or sets
cache_vbit_set = [] #number of sets in the cache
cache_tag_set = []
cache_data_set = []
tag_str_default = ""
char = 0
while char < tag_length:
    tag_str_default = tag_str_default + " "
    char = char + 1
data_str_default = ""
char = 0
while char < input_length:
    data_str_default = data_str_default + " "
    char = char + 1
row = 0
while row < (cache_size/set_associative_count):
    #print ("cache append",row)
    cache_vbit_set.append(0) #append row
    cache_tag_set.append(tag_str_default)
    cache_data_set.append(data_str_default)
    row = row + 1
cache_set_i = 0
while cache_set_i < set_associative_count:
    cache_vbit.append(cache_vbit_set)#valid bit, tag, data
    cache_tag.append(cache_tag_set)
    cache_data.append(cache_data_set)
    cache_set_i = cache_set_i + 1
cache_vbit_array = np.array(cache_vbit)
cache_tag_array = np.array(cache_tag)
cache_data_array = np.array(cache_data)


#---------------------------------
#cache format
#block = 0
#while block < cache_size:
#    block_binary = "{0:010b}".format(block)
#    index_binary = block_binary[0:len(block_binary)-set_length]
#    index_int =int(index_binary,2)
#    set_binary = block_binary[(len(block_binary)-set_length):len(block_binary)]
#    set_int = int(set_binary, 2)
#    print ("block",block,"- index",index_int,"; set",set_int)    
#    block = block + 1
#---------------------------------

#implement least recenlty used using 1-bit clock hand
lru_hand = []
lru_bit = []
set_lru_hand = []
set_lru_bit = []
row = 0
while row < (cache_size/set_associative_count):
    set_lru_hand.append(0)
    set_lru_bit.append(0)
    row = row + 1
set_i = 0
while set_i < set_associative_count:
    lru_hand.append(set_lru_hand)
    lru_bit.append(set_lru_bit)
    set_i = set_i + 1
set_i = 0
lru_hand_array = np.array(lru_hand)
lru_bit_array = np.array(lru_bit)
while set_i < set_associative_count: 
    lru_hand_array[set_i][0] = 1 #set hand to first row in all sets
    set_i = set_i + 1


            

input_count = 1
hit = 0
miss = 0
for input_word in input_set:
    print ("input",input_count,": ",input_word)
    set_binary = input_word[len(input_word)-(offset_length+set_length):len(input_word)-offset_length]
    set_int = int(set_binary, 2)
    print ("set:",set_binary,"(dec :",set_int,")")
    data = input_word
    tag = input_word[0:tag_length]
    #print ("data:",data)
    #print ("tag :",tag)
    #search
    match_found = False
    row_i = 0 
    while row_i < len(cache_tag_array[set_int]):
        row_tag = cache_tag_array[set_int][row_i]
        valid_bit = cache_vbit_array[set_int][row_i]
        if (valid_bit==1) and (row_tag == tag):#tag is saved in index 1 of each row in a set
            match_found = True
            #print ("set_int, row_i, valid_bit",set_int, row_i, valid_bit)
            break
        row_i = row_i + 1
    if match_found:
        hit = hit + 1
        print ("cache hit! (hit rate:",float(hit/input_count)*100,"%)")
        #print ("match:",cache_data_array[set_int][row_i])
        #lower two bits are ignored - byte offset; we are not using byte transfers        
        #print ("match len",len())
        #set clock_bit to 1 
        lru_bit_array[set_int][row_i] = 1
        #no need to move hand as hand moving is only for storing and eviction
    else: #no match found
        #store data to where hand is pointed
        print ("cache miss! (hit rate:",float(hit/input_count)*100,"%)")
        print ("saving data to cache...")
        miss = miss + 1
        clock_hand_index = 0 
        for clock_hand_entry in lru_hand_array[set_int]:
            if clock_hand_entry == 1:
                break
            clock_hand_index = clock_hand_index + 1
        print ("clock_hand_index:",clock_hand_index)
        #check valid bit is irrelevant because this is store not search
        #set tag and data
        cache_vbit_array[set_int][clock_hand_index] = 1
        cache_tag_array[set_int][clock_hand_index] = tag
        cache_data_array[set_int][clock_hand_index] = data
        print ("[set_int][clock_hand_index]=",set_int, clock_hand_index)
        #print ("vbit:",cache_vbit[set_int][clock_hand_index],"size:",len(cache_vbit[set_int][clock_hand_index]))        
        #print ("tag :",cache_tag[set_int][clock_hand_index],"size:",len(cache_tag[set_int][clock_hand_index]))
        #print ("data:",cache_data[set_int][clock_hand_index],"size:",len(cache_data[set_int][clock_hand_index]))
        #set clock bit and move hand 
        update_lru(set_int, clock_hand_index)
    input_count = input_count + 1
unique_set = set(input_set)
input_distribution = "uniform"
print ("---------------")
print ("input size        :",len(input_set))
print ("input distribution:", input_distribution)
print ("---------------")
print ("total # of hits   :",hit, "(",round((hit/len(input_set))*100,3),"%)")
print ("total # of miss   :",miss)
