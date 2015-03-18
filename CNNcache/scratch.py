# -*- coding: utf-8 -*-
"""
Created on Tue Mar 10 01:42:36 2015

@author: scottdicksondagondon
"""

bits = [32*8, 64*8, 128*8]
for entry in bits:
    cluster_size = []
    
    divisor = (entry/16) + 1
    
    while (entry/divisor) > 1:
        if (entry%divisor) == 0:
            cluster_size.append(int(divisor))
        divisor = divisor + 1
    print ("# of clusters for",int(entry/8),"bytes:")
    print (" ",cluster_size)