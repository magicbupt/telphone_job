#!/usr/bin/env python
#encoding:utf-8

def binarySearch(ilist = [1], k = 0):
    
    length = len(ilist)
    begin = 0
    end = length -1
    
    while begin < end :
        
        it = (begin+end)/2
        if ilist[it] == k:
            return it
        
        if ilist[it] > k:
            if list[it - 1] <= k :
                return it-1 
            end = it-1
        
        if ilist[it] < k:
            if ilist[it+1] > k:
                return it 
            begin = it + 1
