# standard lib packages
import sys
import os
import requests
import json
import urllib.parse
import time
import codecs
import csv

from datetime import datetime

timestamp = datetime.now().strftime("%Y_%m%d_%H%M")

fileout = codecs.open('uat_doubelcheck'+timestamp+'.csv','w', encoding='utf-8') #will create or overwrite this file name
wr = csv.writer(fileout,lineterminator='\n', delimiter=',', dialect='excel',quoting=csv.QUOTE_ALL)

wr.writerow(["Bibcode"]+["Author"]+["Afiliation"]+["Citations"])


start = input("Query Start Date (YYYY or YYYY-MM): ")
end = input("Query End Date (YYYY or YYYY-MM): ")

######### Variables to Edit #########

#pubdate format  YYYY-MM-DD TO YYYY-MM-DD
#month and day optional
#examples:  2018-09 TO 2018-11
#           2018 TO 2019-03
#           2018-03 TO 2019
# pubdate = "2019-01 TO 2019-08"
pubdate = str(start)+" TO "+str(end)

#exclude all results that area already this bibgroup
bibgroup = "CfA"

devkey = (open('dev_key.txt','r')).read()

# author query list
authorlist = (open('sao_missed.txt','r')).read()
auth_list = authorlist.splitlines()

# do not SEARCH on the broad or simple aff list, but use to narrow down author name results
#broadafflist = (open('broad_aff_list.txt','r')).read()
#broad_aff_list = broadafflist.splitlines()

#simpleafflist = (open('simple_aff_list.txt','r')).read()
#simple_aff_list = simpleafflist.splitlines()

url = 'https://api.adsabs.harvard.edu/v1/search/query/?q='

def getloop(qtype,query,daterange,devkey):
    q = qtype+':%22'+ urllib.parse.quote(query) + '%22%20pubdate:%5B' + daterange + '%5D' + '%20bibgroup:%22' + bibgroup + '%22'
    headers = {'Authorization': 'Bearer '+devkey}
    content = requests.get(url + q, headers=headers)
    results = content.json()
    #print (results)
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

        q = qtype+':%22'+ urllib.parse.quote(query) + '%22%20pubdate:%5B' + daterange + '%5D' + '%20bibgroup:%22' + bibgroup + '%22&fl=bibcode,author,aff,bibgroup,title,property,citation_count,pub&rows='+str(rows)+'&start='+str(startnum)

        #print (url + q)
        print (query)

        headers = {'Authorization': 'Bearer '+devkey}
        content = requests.get(url + q, headers=headers)

        #print(content.headers["X-RateLimit-Remaining"])
        
        results = content.json()
        docs = results['response']['docs']
        
        for x in docs:
            bibcode = x['bibcode']

            try:
                auth = x['author']
                num_auth = str(len(auth))

            except KeyError:
                auth = []
                num_auth = "-"

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


            try:
                citations = int(x['citation_count'])
            except KeyError:
                citations = 0

            flname = query.split(',')
            namei = flname[0]+", "+flname[1][1]

            for y in range(0,len(auth)):
                if namei.lower() in auth[y].lower():
                    affs = aff[y].lower()

                    wr.writerow([bibcode]+[query]+[affs]+[citations])                            


        startnum += rows
    time.sleep(1)


if __name__ == "__main__":

    # for x in inc_aff_list:
    #     newadsquery("aff",x,pubdate,devkey)

    for x in auth_list:
        newadsquery("author",x,pubdate,devkey)

    print ("finished!")


    fileout.close()