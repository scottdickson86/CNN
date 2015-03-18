# -*- coding: utf-8 -*-
"""
Created on Tue Mar 10 01:42:36 2015

@author: scottdicksondagondon
"""
from random import randint
import math

word_len = 32
byte_len = 2
cache_size = math.pow(2,12)
#block index lower bits - the lower 2 bits represent the byte!
block_index_length = math.log2(cache_size)
#tag - remaining upper bits
tag_lenth = word_len - block_index_length


random_address = ""
word_char_count = 0
while word_char_count < word_len:
    random_address = random_address +str(randint(0,1))
    word_char_count = word_char_count + 1
print ("------------")
print ("input (binary): ",random_address)
#print ("input (int)   : ",int(random_address,2))
print ("------------")
input_block_index = random_address[int(len(random_address)-block_index_length):len(random_address)]
print ("index (binary): ",input_block_index)
print ("index (dec)   : ",int(input_block_index,2))
print ("...ignorning lower two bits (for byte selection)")
input_block_index_wo_byte = random_address[int(len(random_address)-block_index_length):len(random_address)-byte_len]
print ("index (binary): ",input_block_index_wo_byte)
print ("index (dec)   : ",int(input_block_index_wo_byte,2))
input_tag = random_address[0:int(tag_lenth)]
print ("tag   (binary): ",input_tag, "(lenght =",len(input_tag),")")
#print ("tag   (int)   : ",int(input_tag,2))