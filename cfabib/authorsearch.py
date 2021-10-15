# standard lib packages
import sys
import os
import requests
import json
import codecs
import csv
import urllib.parse
from datetime import datetime

devkey = (open('dev_key.txt','r')).read()

#you need to start with a text file containing a list of bibcodes
bib = open('christines_query.txt').read()

timestamp = datetime.now().strftime("%Y_%m%d_%H%M")

incafflist = (open('inc_aff_list.txt','r')).read()
inc_aff_list = incafflist.splitlines()

fileout = codecs.open('uat_doubelcheck'+timestamp+'.csv','w', encoding='utf-8') #will create or overwrite this file name
wr = csv.writer(fileout,lineterminator='\n', delimiter=',', dialect='excel',quoting=csv.QUOTE_ALL)

url = 'https://api.adsabs.harvard.edu/v1/search/query/?q='

wr.writerow(["Bibcodes"]+["Guess"]+["Afiils"])

bib1 = bib.splitlines()
bib_lines = [x.strip() for x in bib1]

#bib_lines = ["2020JNCS..531k9855M"]

for i in bib_lines:
    print (i)

    url = 'https://api.adsabs.harvard.edu/v1/search/query/?q=bibcode:'+urllib.parse.quote(i)+'&fl=bibcode,keyword,aff,database'

    headers = {'Authorization': 'Bearer '+devkey}
    content = requests.get(url, headers=headers)
    results = content.json()
    print (results)
    if results['response']['numFound'] > 0:

        docs = results['response']['docs'][0]
        #print (docs)
        afflower = []
        try:
            aff = docs['aff']
            affclean = (' | ').join(aff)
            for y in aff:
                afflower.append(y.lower())
        except KeyError:
            aff = []
            affclean = ''
        
        #print(afflower)

        guess = "check"
        if aff != []:
            for x in inc_aff_list:
                #print(x.lower())
                if x.lower() in affclean.lower():
                    guess = "likely"
                else:
                    pass

        print("ok")
        wr.writerow([i]+[guess]+[affclean])
    else:
        print(i+" not found")
        wr.writerow([i]+["not found"])


fileout.close()

