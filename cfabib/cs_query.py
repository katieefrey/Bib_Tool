# standard lib packages
import sys
import os
import requests
import json
import codecs
import csv
import urllib.parse
import time
from datetime import datetime

devkey = (open('dev_key.txt','r')).read()

timestamp = datetime.now().strftime("%Y_%m%d_%H%M")

incafflist = (open('inc_aff_list.txt','r')).read()
inc_aff_list = incafflist.splitlines()


fileout = open('christines_info'+timestamp+'.csv','w', encoding='utf-8-sig', newline='')

wr = csv.writer(fileout,quoting=csv.QUOTE_ALL)

# author query list
authorlist = (open('christines_query_status.txt','r', encoding="utf8")).read()
a_list = authorlist.splitlines()

auth_list = []
auth_dict = {}
for y in a_list:
    #print (y)
    x = y.split("  ")
    print (x[1])
    auth_list.append(x[1])
    auth_dict[x[1]]=x[0]

print (auth_list)

# do not SEARCH on the broad or simple aff list, but use to narrow down author name results
broadafflist = (open('broad_aff_list.txt','r')).read()
broad_aff_list = broadafflist.splitlines()

url = 'https://api.adsabs.harvard.edu/v1/search/query/?q='

pubdate = str(2020)+" TO "+str(2021)

wr.writerow(["Query"]+["person type"]+["Associated Affiliation"]+["Bibcode"]+["Guess"]+["status"]+["Title"])

def getloop(qtype,query,daterange,devkey):
    q = qtype+':%22'+ urllib.parse.quote(query) + '%22%20pubdate:%5B' + daterange + '%5D'
    headers = {'Authorization': 'Bearer '+devkey}
    content = requests.get(url + q, headers=headers)
    results = content.json()
    print (results)
    num = results['response']['numFound']
    return num


def newadsquery(qtype,query,daterange,devkey):

    #rows max value is 200
    rows = 100

    total = getloop(qtype,query,pubdate,devkey)
    loop = total/rows
    print ("Looping script "+str(int(loop+1))+" times.")
    startnum = 0
    for i in range (0,int(loop+1)):

        q = qtype+':%22'+ urllib.parse.quote(query) + '%22%20pubdate:%5B' + daterange + '%5D' + '%20bibgroup:cfa&fl=bibcode,author,aff,bibgroup,database,property,title&rows='+str(rows)+'&start='+str(startnum)    
        
        #print (url + q)
        print (query)

        persontype = auth_dict[query]

        headers = {'Authorization': 'Bearer '+devkey}
        content = requests.get(url + q, headers=headers)
        results = content.json()
        
        docs = results['response']['docs']
        
        for x in docs:
            bibcode = x['bibcode']
            bibstem = bibcode[4:9]
            volume = bibcode[9:13]

            try:
                auth = x['author']

            except KeyError:
                auth = []

            try:
                prop = x['property']

            except KeyError:
                prop = []

            try:
                title = x['title']
                title1 = (('|').join(title))
                if len(title1) > 249:
                    titleclean = title1[0:249]
                else:
                    titleclean = title1
            except KeyError:
                titleclean = ''


            try:
                aff = x['aff']
                affclean = (' | ').join(aff)
            except KeyError:
                aff = []
                affclean = ''

            guess = "review" # review


            flname = query.split(',')
            namei = flname[0]+", "+flname[1][1]
            #print(namei)

            for y in range(0,len(auth)):
                if namei.lower() in auth[y].lower():
                    affs = aff[y].lower()
                    #print (affs)
                    guess = "doubtful"

                    # if something from the broad list is in
                    # the affiliation than consider
                    for z in broad_aff_list:
                        if z in affs:
                            guess = "likely" # likely

                            

                    #print("adding author")
                    #add_Author(bibsc.id, auth[y], aff[y], guess, query, inst, 1, status, autoclass)
                    # add_Author(bibsc.id, auth[y], aff[y], guess, query, 4, 1, 3)

                    wr.writerow([query]+[persontype]+[aff[y]]+[bibcode]+[guess]+[prop]+[titleclean])

        startnum += rows
    time.sleep(1)


if __name__ == "__main__":

    for x in auth_list:
       newadsquery("author",x,pubdate,devkey)

    print ("finished!")
    fileout.close()
