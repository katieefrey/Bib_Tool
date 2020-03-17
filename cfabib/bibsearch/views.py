from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect

from bibmanage.models import Bibgroup

import urllib.parse
import requests
import time

# Create your views here.




def bsindex(request):

    bibgroups = Bibgroup.objects.all();

    context = {
        "err" : "",
        "bibgroups": bibgroups
        }

    return render(request, "bibsearch/search.html", context)


def results(request):

    context = {
        "err" : ""
        }

    namelist = request.POST["authorlist"]
    startdate = request.POST["startdate"]
    enddate = request.POST["enddate"]
    bibgroup = request.POST["bibgroups"]

    print (bibgroup)

    #print ("start date--> "+startdate"
    if namelist == "":
        error = "Please provide a name to search!"
        context ["err"] = error
        return render(request, "bibsearch/search.html", context)

    elif startdate == "" or enddate == "":
        error = "Please provide valid dates!"
        context["err"] = error
        return render(request, "bibsearch/search.html", context)

    else:
        
        daterange = startdate+" TO "+enddate
        authorlist = namelist.splitlines()

        devkey = (open('dev_key.txt','r')).read()
        url = 'https://api.adsabs.harvard.edu/v1/search/query/?q='

        def getloop(query,daterange,devkey):
            q = 'author:%22'+ urllib.parse.quote(query) + '%22%20pubdate:%5B' + daterange + '%5D%20bibgroup:'+bibgroup
            headers = {'Authorization': 'Bearer '+devkey}
            content = requests.get(url + q, headers=headers)
            results = content.json()
            num = results['response']['numFound']
            return num


        def adsquery(query,daterange,devkey):
            #rows max value is 200
            rows = 200

            total = getloop(query,daterange,devkey)
            loop = total/rows
            #print ("Looping script "+str(int(loop+1))+" times.")
            startnum = 0    

            total_cite = 0
            ref_cite = 0
            nonref_cite = 0

            total_art = 0
            ref_art = 0
            nonref_art = 0

            firstauth_ref = 0
            firstauth_nonref = 0

            for i in range (0,int(loop+1)):

                q = 'author:%22'+urllib.parse.quote(query)+'%22%20pubdate:%5B'+daterange+'%5D%20bibgroup:'+bibgroup+'&fl=bibcode,property,citation_count,pub&rows='+str(rows)+'&start='+str(startnum)

                #print (url + q)

                headers = {'Authorization': 'Bearer '+devkey}
                content = requests.get(url + q, headers=headers)
                results = content.json()
                docs = results['response']['docs']

                for x in docs:
                    bibcode = x['bibcode']

                    if bibcode in bibcodelist:
                        pass
                    else:
                        bibcodelist.append(bibcode)
                        journal = str(x['pub'])
                        journallist.append(journal)

                    try:
                        prop = x['property']
                        propclean = (' | ').join(prop)
                    except KeyError:
                        propclean = ''

                    try:
                        citations = int(x['citation_count'])
                    except KeyError:
                        citations = 0

                    total_cite += citations
                    total_art += 1

                    if "not refereed" in propclean.lower():
                        nonref_cite += citations
                        nonref_art += 1
                        
                    elif "refereed" in propclean.lower():
                        ref_cite += citations
                        ref_art += 1

                    else:
                        print ("what?")
                        pass



                qf = 'first_author:%22'+urllib.parse.quote(query)+'%22%20pubdate:%5B'+daterange+'%5D%20bibgroup:'+bibgroup+'&fl=property&rows='+str(rows)+'&start='+str(startnum)
                
                contentf = requests.get(url + qf, headers=headers)
                resultsf = contentf.json()
                docsf = resultsf['response']['docs']

                for y in docsf:

                    try:
                        propf = y['property']
                        propcleanf = (' | ').join(propf)
                    except KeyError:
                        propcleanf = ''

                    if "not refereed" in propcleanf.lower():
                        #print ("no")
                        firstauth_nonref += 1
                        
                    elif "refereed" in propcleanf.lower():
                        #print ("yes")
                        firstauth_ref += 1

                    else:
                        print ("what?")
                        pass

                startnum += rows
            #time.sleep(1)
            return total_art, ref_art, nonref_art, total_cite, ref_cite, nonref_cite, firstauth_ref, firstauth_nonref


        bibcodelist = []
        journallist = []

        alist = []

        galist = []

        for x in authorlist:
            authors = {}
            graph_authors = {}

            #num = getloop(x,daterange,devkey)
            authors["name"] = x

            total_art, ref_art, nonref_art, total_cite, ref_cite, nonref_cite, firstauth_ref, firstauth_nonref = adsquery(x,daterange,devkey)

            #print (total_art)

            if total_art == 0:
                pass

            else:
                graph_authors["name"] = x
                graph_authors["total_art"] = total_art
                graph_authors["gref_art"] = ref_art - firstauth_ref
                graph_authors["gnonref_art"] = nonref_art - firstauth_nonref
                graph_authors["firstauth_ref"] = firstauth_ref
                graph_authors["firstauth_nonref"] = firstauth_nonref

                galist.append(graph_authors)
            
            authors["total_art"] = total_art
            authors["ref_art"] = ref_art
            authors["nonref_art"] = nonref_art

            authors["total_cite"] = total_cite
            authors["ref_cite"] = ref_cite
            authors["nonref_cite"] = nonref_cite

            authors["firstauth_ref"] = firstauth_ref
            authors["firstauth_nonref"] = firstauth_nonref

            authors["fauth"] = firstauth_nonref + firstauth_ref

            alist.append(authors)

        authnum = (len(alist))
        gauthnum1 = len(galist)

        if gauthnum1*40 <= 300:
            gauthnum = 350
        else:
            gauthnum = gauthnum1*40

        uniquej = set(journallist)
        
        jlist = []
        for y in uniquej:
            jours = {}
            total_art = journallist.count(y)

            jours["journal"] = y
            jours["total_art"] = total_art

            jlist.append(jours)

        jnum = len(jlist)

        newlist = sorted(alist, key=lambda k: k['total_art']) 
        gnewlist = sorted(galist, key=lambda k: k['total_art']) 

        jnewlist = sorted(jlist, key=lambda k: k['total_art']) 

        context["journals"] = jnewlist
        context["authors"] = newlist
        context["gauthors"] = gnewlist
        context["daterange"] = daterange
        context["authnum"] = authnum
        context["gauthnum"] = gauthnum
        context["jnum"] = jnum
        context["ratio"] = (100/authnum)/100

    context["authorlist"] = authorlist

    # plotly graph stuff
    # https://stackoverflow.com/questions/36846395/embedding-a-plotly-chart-in-a-django-template

    return render(request, "bibsearch/results.html", context)
