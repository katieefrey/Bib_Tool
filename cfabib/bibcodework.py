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

wr.writerow(["Bibcode"]+["Property"]+["Citations"]+["Publication"])


#start = input("Query Start Date (YYYY or YYYY-MM): ")
#end = input("Query End Date (YYYY or YYYY-MM): ")

######### Variables to Edit #########

#pubdate format  YYYY-MM-DD TO YYYY-MM-DD
#month and day optional
#examples:  2018-09 TO 2018-11
#           2018 TO 2019-03
#           2018-03 TO 2019
# pubdate = "2019-01 TO 2019-08"
#pubdate = str(start)+" TO "+str(end)

#exclude all results that area already this bibgroup
bibgroup = "CfA"

devkey = (open('dev_key.txt','r')).read()

# author query list
# authorlist = (open('sao_missed.txt','r')).read()
# auth_list = authorlist.splitlines()

biblist = (open('bibcodessao.txt','r')).read()
bib_list = biblist.splitlines()

# do not SEARCH on the broad or simple aff list, but use to narrow down author name results
#broadafflist = (open('broad_aff_list.txt','r')).read()
#broad_aff_list = broadafflist.splitlines()

#simpleafflist = (open('simple_aff_list.txt','r')).read()
#simple_aff_list = simpleafflist.splitlines()

url = 'https://api.adsabs.harvard.edu/v1/search/query/?q='


def newadsquery(query,devkey):
    #print (query)
    q = 'bibcode:%22'+ urllib.parse.quote(query) + '%22&fl=bibcode,property,citation_count,pub'

    #print (url + q)
    

    headers = {'Authorization': 'Bearer '+devkey}
    content = requests.get(url + q, headers=headers)

    #print(content.headers["X-RateLimit-Remaining"])
    
    results = content.json()

    print (results)
    docs = results['response']['docs']
    
    for x in docs:
        bibcode = x['bibcode']

        try:
            props = x['property']

            if "NOT REFEREED" in props:
                prop1 = "NOT REFEREED"
            elif "REFEREED" in props:
                prop1 = "REFEREED"
            else:
                prop1 = "None"


        except KeyError:
            props = 0

        try:
            pub = x['pub']
        except KeyError:
            pub = "none"

        try:
            citations = int(x['citation_count'])
        except KeyError:
            citations = 0


        wr.writerow([bibcode]+[prop1]+[citations]+[pub])                            

    #time.sleep(1)


if __name__ == "__main__":

    # for x in inc_aff_list:
    #     newadsquery("aff",x,pubdate,devkey)

    # for x in auth_list:
    #     newadsquery("author",x,pubdate,devkey)

    for x in bib_list:
        print (x)
        newadsquery(x,devkey)


    print ("finished!")


    fileout.close()