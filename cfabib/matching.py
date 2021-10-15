#!/usr/bin/python

import csv
import sys

import time
import codecs

from datetime import datetime

timestamp = datetime.now().strftime("%Y_%m%d_%H%M")

# fileout = codecs.open('matchingtest'+timestamp+'.csv','w', encoding='utf-8') #will create or overwrite this file name
# wr = csv.writer(fileout,lineterminator='\n', delimiter=',', dialect='excel',quoting=csv.QUOTE_ALL)

# wr.writerow(["Bibcode"]+["Property"]+["Citations"]+["Publication"])

# biblist = (open('allsaobibs.txt','r')).read()
# bib_list = biblist.splitlines()

# for x in bib_list:

#     csv_file = csv.reader(open('bibcodeinfo.csv', "r"), delimiter=",")
#     #loop through the csv list
#     for row in csv_file:
#         if x == row[0]:
#             wr.writerow(row)
#         else:
#             pass

# fileout.close()



fileout = codecs.open('matchingtest'+timestamp+'.csv','w', encoding='utf-8') #will create or overwrite this file name
wr = csv.writer(fileout,lineterminator='\n', delimiter=',', dialect='excel',quoting=csv.QUOTE_ALL)

wr.writerow(["Bibcode"]+["Property"]+["Citations"]+["Publication"])

biblist = (open('2019auth.txt','r')).read()
bib_list = biblist.splitlines()

for x in bib_list:
    print(x)

    csv_file = csv.reader(open('SAO2019.csv', "r"), delimiter=",")
    #loop through the csv list
    total = 0
    for row in csv_file:
        if x == row[1]:
            total=+1
        else:
            pass

    wr.writerow([x]+[total])
fileout.close()