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

from django.conf import settings

from bibtool.models import Article, Author, NewArticle

print (settings.DATABASES)

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
excluded_bibstems = ["arXiv","ATel1","ATel.","yCat.","MPEC.","sptz.","Cosp.","DPS..","IAUC.","SPD..","AGUFM","AGUSM","APS..","IAUFM","AAS..","HEAD.","DDA..","zndo."]
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

# included affiliations
incafflist = (open('inc_aff_list.txt','r')).read()
inc_aff_list = incafflist.splitlines()

# author query list
#authorlist = (open('author_list.txt','r')).read()
#auth_list = authorlist.splitlines()

# author query list
#authorlist = (open('author_list_2022_08_02.txt','r')).read()
authorlist = (open('author_list_started_2022_2023.txt','r')).read()
#authorlist = (open('author_extras.txt','r')).read()
auth_list = authorlist.splitlines()

# do not SEARCH on the broad or simple aff list, but use to narrow down author name results
broadafflist = (open('broad_aff_list.txt','r')).read()
broad_aff_list = broadafflist.splitlines()

simpleafflist = (open('simple_aff_list.txt','r')).read()
simple_aff_list = simpleafflist.splitlines()

url = 'https://api.adsabs.harvard.edu/v1/search/query/?q='


def add_NewArticle(data1, data2, data3, data4):
    try:
        d, created = NewArticle.objects.get_or_create(bibcode=data1, title=data2, adminbibgroup_id=data3, authnum=data4)
        return d

    except django.db.utils.IntegrityError:
        print ("DID YOU SET UP THE DATABSES??")
        print("something went wrong, new article")
        return

def add_Author(data1, data2, data3, data4, data5, data6, data7, data8, data9):
    try:
        d, created = Author.objects.get_or_create(bibcode_id=data1, name=data2, affil=data3, guess_id=data4, query=data5, inst_id=data6, adminbibgroup_id=data7, status_id=data8, autoclass=data9)
        return d

    except django.db.utils.IntegrityError:
        print("something went wrong, author")
        return

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

        q = qtype+':%22'+ urllib.parse.quote(query) + '%22%20pubdate:%5B' + daterange + '%5D' + '&fl=bibcode,author,aff,bibgroup,database,title&rows='+str(rows)+'&start='+str(startnum)    
        
        #print (url + q)
        print (query)

        headers = {'Authorization': 'Bearer '+devkey}
        content = requests.get(url + q, headers=headers)
        results = content.json()
        #print (results)
        docs = results['response']['docs']
        
        for x in docs:
            bibcode = x['bibcode']
            bibstem = bibcode[4:9]
            volume = bibcode[9:13]

            # if bibstem or volume are in an excluded set,
            # skip the rest of the function
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

                # if the bibgroup is in the list of bibgroups,
                # skip the rest of the function
                if bibgroup in bibgroupclean:
                    pass

                # otherwise! it is time to get to work
                else:
                    # print (x["database"])

                    # if "astronomy" or "physics" in x["database"]:
                    #     print ("yes")
                    # else:
                    #     print("no")

                    try:
                        test = Article.objects.get(bibcode=bibcode)
                        print (bibcode+" already in old system")
                        
                    except Article.DoesNotExist:

                        try:
                            auth = x['author']
                            num_auth = str(len(auth))

                        except KeyError:
                            auth = []
                            num_auth = "-"

                        try:
                            title = x['title']
                            title1 = (('|').join(title)).encode("utf-8", "strict").decode("utf-8").encode('unicode_escape')
                            if len(title1) > 100:
                                titleclean = (title1[0:100])
                            else:
                                titleclean = title1
                        except KeyError:
                            titleclean = ''

                        print (titleclean)


                        try:
                            aff = x['aff']
                            affclean = (' | ').join(aff)
                        except KeyError:
                            aff = []
                            affclean = ''

                        try:
                            NewArticle.objects.get(bibcode=bibcode)
                            #print (bibcode+" already in")
                            
                        except NewArticle.DoesNotExist:
                            print ("adding "+bibcode)
                            add_NewArticle(bibcode, titleclean, 1, num_auth)

                        bibsc = NewArticle.objects.get(bibcode=bibcode)
                        guess = 2 # review
                        
                        if qtype == "aff":
                            for y in range(0,len(auth)):
                                if query in aff[y].lower():
                                    
                                    if Author.objects.filter(bibcode=bibsc.id, name=auth[y], affil=aff[y],adminbibgroup_id=1).exists():
                                        #print("author already in, step 1")
                                        pass
                                    else:
                                        #print("adding author")

                                        guess = 1 # likely

                                        if "visiting" in aff[y].lower():
                                            guess = 3 # review-visiting

                                        elif "visit" in aff[y].lower():
                                            guess = 3 # review-visiting

                                        elif "retired" in aff[y].lower():
                                            guess = 2 # review-visiting
            
                                        if guess == 1 and query == "cfa":
                                            if "irfu" in aff[y].lower():
                                                guess = 5 # review-nonCfA
                                            elif "cfa-italia" in aff[y].lower():
                                                guess = 5 # review-nonCfA
                                            elif "cfai" in aff[y].lower():
                                                guess = 5 # review-nonCfA
                                            else:
                                                guess = 2 #review

                                        elif guess == 1 and query == "hco":
                                            if "Northcott" in aff[y].lower():
                                                guess = 5 # review-nonCfA


                                        if guess == 1:
                                            autoclass = True
                                            status = 1
                                            inst = 6
                                        else:
                                            autoclass = False
                                            status = 3
                                            inst = 4

                                        add_Author(bibsc.id, auth[y], aff[y], guess, query, inst, 1, status, autoclass)


                        elif qtype == "author":
                            flname = query.split(',')
                            namei = flname[0]+", "+flname[1][1]

                            for y in range(0,len(auth)):
                                if namei.lower() in auth[y].lower():
                                    affs = aff[y].lower()

                                    guess = 6
                                    autoclass = True
                                    status = 2
                                    inst = 5

                                    # if something from the broad list is in
                                    # the affiliation than consider
                                    for z in broad_aff_list:
                                        if z in affs:
                                            guess = 1 # likely

                                    if guess == 1:
                                        autoclass = True
                                        status = 1
                                        inst = 6
                                    else:

                                        if affs == '-':
                                            guess = 2
                                        else: 
                                            for z in simple_aff_list:
                                                if z in affs:
                                                    guess = 2
                                        
                                        if guess == 2:
                                            autoclass = False
                                            status = 3
                                            inst = 4

                                    if Author.objects.filter(bibcode=bibsc.id, name=auth[y], affil=aff[y],adminbibgroup_id=1).exists():
                                            #print("author already in, step 2")
                                            pass
                                    else:
                                        # if guess != 0:
                                        #     print("adding author")
                                        #     add_Author(bibsc.id, auth[y], aff[y], guess, query, inst, 1, status, autoclass)
                                        # else:
                                            

                                        print("adding author")
                                        add_Author(bibsc.id, auth[y], aff[y], guess, query, inst, 1, status, autoclass)
                                        # add_Author(bibsc.id, auth[y], aff[y], guess, query, 4, 1, 3)

        startnum += rows
    time.sleep(1)


if __name__ == "__main__":

    for x in inc_aff_list:
       newadsquery("aff",x,pubdate,devkey)

    for x in auth_list:
       newadsquery("author",x,pubdate,devkey)

    print ("finished!")