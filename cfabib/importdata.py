# standard lib packages
import sys
import os
import requests
import json
import urllib.parse
import time

os.environ.setdefault('DJANGO_SETTINGS_MODULE','cfabib.settings')

import django
django.setup()

from bibtool.models import Article


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


######### Excluded Strings, Edit with Caution #########

# exclude the following bibstems, each must be exactly 5 characters long
excluded_bibstems = ["arXiv","ATel1","ATel.","yCat.","MPEC.","sptz.","Cosp.","DPS..","IAUC.","SPD..","AGUFM","AGUSM","APS..","IAUFM","AAS..","HEAD.","DDA.."]
# Verified bibstem codes to INCLUDE
# (i.e. do NOT write these into the above list)
# CBET.

#Always Include?
#ChNew  -- Chandra News?

# exclude the following volume codes, must be 4 characters long
excluded_volumes = ["prop",".tmp"]
# Verified volume codes to INCLUDE
# (i.e. do NOT write these into the above list)
# conf
# book


devkey = (open('dev_key.txt','r')).read()

authorlist = (open('author_list.txt','r')).read()
#authorlist3 = (open('author_list-3.txt','r')).read()
incafflist = (open('inc_aff_list.txt','r')).read()


inc_aff_list = incafflist.splitlines()
auth_list = authorlist.splitlines()
#auth_list3 = authorlist3.splitlines()

url = 'https://api.adsabs.harvard.edu/v1/search/query/?q='


def add_Article(data1, data2, data3, data4, data5, data6, data7, data8):
    try:
        d, created = Article.objects.get_or_create(bibcode=data1, guess_id=data2, query=data3, affils=data4, adminbibgroup_id=data5, authnum=data6, status_id=data7, inst_id=data8)
        return d

    except django.db.utils.IntegrityError:
        print("already in database")
        return

def getloop(qtype,query,daterange,devkey):
    q = qtype+':%22'+ urllib.parse.quote(query) + '%22%20pubdate:%5B' + daterange + '%5D'
    headers = {'Authorization': 'Bearer '+devkey}
    content = requests.get(url + q, headers=headers)
    results = content.json()
    #print (results)
    num = results['response']['numFound']
    return num

def adsquery(qtype,query,daterange,devkey):

    #rows max value is 200
    rows = 100

    total = getloop(qtype,query,pubdate,devkey)
    loop = total/rows
    print ("Looping script "+str(int(loop+1))+" times.")
    startnum = 0
    for i in range (0,int(loop+1)):

        q = qtype+':%22'+ urllib.parse.quote(query) + '%22%20pubdate:%5B' + daterange + '%5D' + '&fl=bibcode,author,aff,bibgroup&rows='+str(rows)+'&start='+str(startnum)    
        
        print (url + q)

        headers = {'Authorization': 'Bearer '+devkey}
        content = requests.get(url + q, headers=headers)
        results = content.json()
        docs = results['response']['docs']
        
        for x in docs:
            bibcode = x['bibcode']
            bibstem = bibcode[4:9]
            volume = bibcode[9:13]

            if bibstem in excluded_bibstems:
                pass

            elif volume in excluded_volumes:
                pass

            else:
                try:
                    bibgroup1 = x['bibgroup']
                    bibgroupclean = ('|').join(bibgroup1)
                except KeyError:
                    bibgroupclean = ''

                if bibgroup in bibgroupclean:
                    pass

                else:

                    try:
                        Article.objects.get(bibcode=bibcode)
                        print (bibcode+" already in")
                        
                    except Article.DoesNotExist:
                        print ("adding "+bibcode)

                        try:
                            auth = x['author']
                            num_auth = str(len(auth))

                        except KeyError:
                            auth = []
                            num_auth = "0"

                        try:
                            aff = x['aff']
                            affclean = (' | ').join(aff)
                        except KeyError:
                            aff = []
                            affclean = ''

                        pairedaff_list = []

                        guess = 2 # review
                        
                        if qtype == "aff":
                            for y in range(0,len(auth)):
                                if query in aff[y].lower():
                                    guess = 1
                                    pairedaff_list.append(aff[y])
                                    aff_list = (" | ").join(pairedaff_list)
                                else:
                                    pass

                            if "Visiting" in affclean:
                                guess = 3 # review-visiting
                            else:
                                pass

                            if guess == 2: #review
                                aff_list = affclean

                            # if guess == likely
                            if guess == 1 and aff == "smithsonian":
                                if "observatory" not in aff_list.lower():
                                    guess = 4 # review-nonSAO
                                else:
                                    pass

                            elif guess == "Keep" and aff == "cfa":
                                if "irfu" in aff_list.lower():
                                    guess = 5 # review-nonCfA
                                elif "cfa-italia" in aff_list.lower():
                                    guess = 5 # review-nonCfA
                                else:
                                    pass                        

                            elif guess == 1: # likely
                                pass

                            else:
                                pass       

                        elif qtype == "author":

                            boo = 0

                            for w in inc_aff_list:
                                if w in affclean.lower():
                                    boo = 1

                            if boo == 0:
                                guess = 6 # doubtful

                            elif boo == 1:
                                guess = 1 #likely

                            aff_list = affclean

                        add_Article(bibcode, guess, query, aff_list, 1, num_auth, 3, 4)
                        # status 3 = maybe
                        # inst 4 = unknown

        startnum += rows
    time.sleep(1)


if __name__ == "__main__":

    for x in inc_aff_list:
        adsquery("aff",x,pubdate,devkey)

    # for x in auth_list:
    #     adsquery("author",x,pubdate,devkey)


    print ("finished!")