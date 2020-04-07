from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse

from .models import Criteria, Batch
from bibtool.models import Article

import csv
import json
import requests
import urllib.parse
import time

# Create your views here.
def bmindex(request):
    #if they are NOT loggedin...
    if not request.user.is_authenticated:
        context = {
            "state": "home"
            }
        return render(request, "bibtool/index.html", context)
    
    context = {}
    return render(request, "bibmanage/index.html", context)

def batch(request):
    #if they are NOT loggedin...
    if not request.user.is_authenticated:
        context = {
            "state": "home"
            }
        return render(request, "bibtool/index.html", context)
    
    #otherwise, if they are logged in...
    username = request.user
    bibgroup = username.bibgroup

    # create new batch
    # number of all CfA verified bibcodes not in a batch
    # view all bibcodes?

    closed = Batch.objects.filter(bibgroup=bibgroup,closed=True)

    newbibs = Article.objects.filter(status_id=1,batch_id=None)
    
    context = {
        "closed":  closed,
        "newbibs" : newbibs,
        "numnew" : len(newbibs),
        "err" : "",
    }

    try:
        openbatch = Batch.objects.get(bibgroup=bibgroup,closed=False)
        
        openbatart = Article.objects.filter(batch_id=openbatch.id)
        

        context["openbatch"] = openbatch
        context["num"] = len(openbatart)


    except Batch.DoesNotExist:
        context["openbatch"] = None


    return render(request, "bibmanage/batch.html", context)


def viewbatch(request,batchid):

    #if they are NOT loggedin...
    if not request.user.is_authenticated:
        context = {
            "state": "home"
            }
        return render(request, "bibtool/index.html", context)
    
    #otherwise, if they are logged in...
    username = request.user
    bibgroup = username.bibgroup

    try:
        onebatch = Batch.objects.get(bibgroup=bibgroup,id=batchid)

        numbibs = Article.objects.filter(batch_id=batchid).count()

        context = {
            "err": "",
            "batch" : onebatch,
            "numbibs" : numbibs,
        }

        return render(request, "bibmanage/viewbatch.html", context)

    except Batch.DoesNotExist:

        return HttpResponseRedirect(reverse("batch"))


def export(request):
    batchid = request.POST["batchid"]
    bibs = Article.objects.filter(batch_id=batchid)

    # Create the HttpResponse object with the appropriate CSV header.
    response = HttpResponse(content_type='text/plain')
    response['Content-Disposition'] = 'attachment; filename="batch_'+batchid+'.txt"'

    writer = csv.writer(response)

    for x in bibs:
        writer.writerow([x.bibcode])

    return response


def close_batch(request):
    print("does this work?")

    batchid = request.POST["batchid"]

    curbatch = Batch.objects.get(id=batchid)

    curbatch.closed = True

    curbatch.save()

    #url = reverse('batch', kwargs={'batchid': batchid})
    #return HttpResponseRedirect(url)

    return HttpResponseRedirect('batch/%s' % batchid)
    #return HttpResponseRedirect(reverse("batch"))
    # http://127.0.0.1:8000/bibmanage/batch/2

def post_openbatch(request):

    #if they are NOT loggedin...
    if not request.user.is_authenticated:
        context = {
            "state": "home"
            }
        return render(request, "bibtool/index.html", context)
    
    #otherwise, if they are logged in...
    username = request.user
    bibgroup = username.bibgroup

    # try to get an existing open batch...
    try:
        curopen = Batch.objects.get(bibgroup=bibgroup, closed=False)

    # if none found, then create a new one
    except Batch.DoesNotExist:

        created = Batch.objects.create(bibgroup=bibgroup, closed=False)

    # go back to the batch page
    return HttpResponseRedirect(reverse("batch"))



def post_addtobatch(request):

    #if they are NOT loggedin...
    if not request.user.is_authenticated:
        context = {
            "state": "home"
            }
        return render(request, "bibtool/index.html", context)
    
    #otherwise, if they are logged in...
    username = request.user
    bibgroup = username.bibgroup

    newbibcodes = request.POST.getlist('bibcodes')
    batchid = request.POST["batchid"]

    for bibid in newbibcodes:
        curbib = Article.objects.get(id=bibid)
        curbib.batch_id = batchid
        curbib.save()

    # go back to the batch page
    return HttpResponseRedirect(reverse("batch"))

def add(request):
    #if they are NOT loggedin...
    if not request.user.is_authenticated:
        context = {
            "state": "home"
            }
        return render(request, "bibtool/index.html", context)

    #otherwise, if they are logged in...
    username = request.user
    bibgroup = username.bibgroup

    criteria = Criteria.objects.values_list('id', 'name', named=True).filter(bibgroup_id=bibgroup.id)

    context = {
        "bibgroup": bibgroup,
        "err": "",
        "criteria" : criteria
        }

    return render(request, "bibmanage/add.html", context)

def select_criteria(request):

    criteriaid = request.POST["criteriaid"]

    if criteriaid == "":
        data = {
            "instlist" : "",
            "authorlist" : "",
            "exclstem" : "",
            "exclvol" : "",
            "inclstem" : "",
            "inclvol" : "",
            }

    else:
        criteria = Criteria.objects.get(id=criteriaid)

        data = {
            "instlist" : criteria.instlist,
            "authorlist" : criteria.authorlist,
            "exclstem" : criteria.exclstem,
            "exclvol" : criteria.exclvol,
            "inclstem" : criteria.inclstem,
            "inclvol" : criteria.inclvol,
            }

    json_data = json.dumps(data)
    return HttpResponse(json_data, content_type="application/json")

def add_post(request):

    username = request.user
    devkey = username.devkey
    bibgroup = username.bibgroup
    print (bibgroup)

    criteriaid = request.POST["criteriaid"]
    startdate = request.POST["startdate"]
    enddate = request.POST["enddate"]

    if criteriaid == "":
        print ("nothing selected, should write an error thingy")
        pass

    else:
        criteria = Criteria.objects.get(id=criteriaid)
        print (criteria)
        aff_list =  (criteria.instlist).splitlines()
        print (aff_list)

        auth_list = (criteria.authorlist).splitlines()
        excluded_bibstems = (criteria.exclstem).splitlines()
        excluded_volumes = (criteria.exclvol).splitlines()

        pubdate = str(startdate)+" TO "+str(enddate)

        url = 'https://api.adsabs.harvard.edu/v1/search/query/?q='


        def add_Article(data1, data2, data3, data4, data5, data6, data7, data8):
            d, created = Article.objects.get_or_create(bibcode=data1, guess_id=data2, query=data3, affils=data4, authnum=data5, status_id=data6, inst_id=data7, adminbibgroup=data8)

            return d

        def getloop(qtype,query,daterange,devkey):
            q = qtype+':%22'+ urllib.parse.quote(query) + '%22%20pubdate:%5B' + daterange + '%5D'
            headers = {'Authorization': 'Bearer '+devkey}
            content = requests.get(url + q, headers=headers)
            results = content.json()
            num = results['response']['numFound']
            return num

        def adsquery(qtype,aff_list,query,daterange,devkey):

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

                        if bibgroup.bibgroup in bibgroupclean:
                            pass

                        else:

                            try:
                                check = Article.objects.get(bibcode=bibcode, adminbibgroup=bibgroup)
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

                                    #print (aff_list)
                                    for w in aff_list:
                                        if w in affclean.lower():
                                            boo = 1

                                    if boo == 0:
                                        guess = 6 # doubtful

                                    elif boo == 1:
                                        guess = 1 #likely

                                    aff_list = affclean

                                add_Article(bibcode, guess, query, aff_list, num_auth, 3, 4, bibgroup)
                                # status 3 = maybe
                                # inst 4 = unknown

                startnum += rows
            time.sleep(1)

        for x in aff_list:
            adsquery("aff",aff_list,x,pubdate,devkey)

        for x in auth_list:
            adsquery("author",aff_list,x,pubdate,devkey)


    context = {}


    #return render(request, "bibmanage/add.html", context)
    return render(request, "bibmanage/add_post.html", context)

def delete_post(request):

    #if they are NOT loggedin...
    if not request.user.is_authenticated:
        context = {
            "state": "home"
            }
        return render(request, "bibtool/index.html", context)

    #otherwise, if they are logged in...
    username = request.user
    bibgroup = username.bibgroup

    criteriaid = request.POST["criteriaid"]

    if criteriaid == "":
        print ("nothing selected, should write an error thingy")
        pass

        data = {}

    else:
        criteria_del = Criteria.objects.get(id=criteriaid)

        #must uncomment to actually delete the record
        criteria_del.delete()

        criteria = Criteria.objects.values_list('id', 'name', named=True).filter(bibgroup_id=bibgroup.id)

        print (criteria)

        crit_list = []
        for y in criteria:
            crit_dict = {}
            print (y)
            crit_dict["id"] = y.id
            crit_dict["name"] = y.name

            crit_list.append(crit_dict)

        data = {
                "critlist" : crit_list
                }

    json_data = json.dumps(data)
    return HttpResponse(json_data, content_type="application/json")


    #return render(request, "bibmanage/add_post.html", context)



def submitads(request):

    #if they are NOT loggedin...
    if not request.user.is_authenticated:
        context = {
            "state": "home"
            }
        return render(request, "bibtool/index.html", context)

    context = {
        "err" : ""
        }

    return render(request, "bibmanage/submitads.html", context)