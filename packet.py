##Trial File


import sys
from math import *

file = input("Enter file name:")
pr = int(input("Enter packet rate:"))
file_open = open(file,'r').readlines()

some_list = []
for i in file_open:
    x = i.rstrip()
    list_unknown = x.split(" ")
    number_of_packets = floor(float(list_unknown[3])*pr)
    for j in range(number_of_packets):
        list_unknown[0] = round(float(list_unknown[0]),2)
        final_time = list_unknown[0] + round(1/pr,2)
        list_unknown[3] = final_time
        some_list.append(tuple(list_unknown))
        list_unknown[0] = final_time
print(some_list)        
        
