from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render
from django.conf import settings
from datetime import datetime
from django.db.models import Count, DateTimeField
from django.db.models.functions import TruncDate, TruncMonth, TruncDay, TruncHour, TruncMinute

import urllib.parse
import requests
import time

from .models import Status, Affil, Article


def index(request):
    #if they are NOT loggedin...
    if not request.user.is_authenticated:
        context = {
            "state": "home"
            }
        return render(request, "bibtool/index.html", context)

    #otherwise, if they are logged in...
    username = request.user
    userid = username.id

    context = {
        "state": "loggedin",
        "first": username.first_name
        }

    return render(request, "bibtool/index.html", context)

#send user to login form
def login_form(request):
    context = {
            "state": "login",
            "error": ""
        }
    return render(request, "bibtool/index.html", context)


#log user in
def login_view(request):
    username = request.POST["inputUsername"]
    password = request.POST["inputPassword"]

    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        context = {
            "state": "login",
            "error": "Invalid credentials, try again."
            }
        return render(request, "bibtool/index.html", context)


#log user out
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))

def batch(request):

    #if they are NOT loggedin...
    if not request.user.is_authenticated:
        context = {
            "state": "home"
            }
        return render(request, "bibtool/index.html", context)

    username = request.user
    bibgroup = username.bibgroup

    dates = Article.objects.filter(adminbibgroup=bibgroup).annotate(month=TruncMonth('created')).values('month').annotate(c=Count('id'))

    notmod = Article.objects.filter(status_id=3,adminbibgroup=bibgroup).annotate(month=TruncMonth('created')).values('month').annotate(c=Count('id'))

    notknown = Article.objects.filter(inst_id=4,adminbibgroup=bibgroup).annotate(month=TruncMonth('created')).values('month').annotate(c=Count('id'))

    batchlist = []

    for y in range(0,len(dates)):
        batches = {}

        batches["month"] = (dates[y]["month"])

        try:
            batches["notmod"] = (notmod[y]["c"])
        except IndexError:
            batches["notmod"] = 0
        try:            
            batches["notknown"] = (notknown[y]["c"])
        except IndexError:
            batches["notknown"] = 0

        batches["total"] = (dates[y]["c"])

        batchlist.append(batches)


    context = {
        "batches": batchlist
        }

    return render(request, "bibtool/batch.html", context)

def massupdate(request,year,month):

    #if they are NOT loggedin...
    if not request.user.is_authenticated:
        context = {
            "state": "home"
            }
        return render(request, "bibtool/index.html", context)

    username = request.user
    bibgroup = username.bibgroup

    articles = Article.objects.filter(created__year=year,created__month=month,adminbibgroup=bibgroup)
    allmod = []
    allnot = []
    
    for y in articles:
        if y.created.strftime('%Y %m %d %H %M') == y.modified.strftime('%Y %m %d %H %M'):
            allnot.append(y)
        else:
            allmod.append(y)

    numod = len(allmod)
    numnot = len(allnot)
        
    context = {
        "articles": articles,
        "numod": numod,
        "numnot": numnot
        }

    return render(request, "bibtool/massupdate.html", context)

def update(request,year, month):

    #if they are NOT loggedin...
    if not request.user.is_authenticated:
        context = {
            "state": "home"
            }
        return render(request, "bibtool/index.html", context)

    username = request.user
    bibgroup = username.bibgroup

    articles = Article.objects.filter(created__year=year,created__month=month,adminbibgroup=bibgroup)
    allmod = []
    allnot = []
    
    for y in articles:
        if y.created.strftime('%Y %m %d %H %M') == y.modified.strftime('%Y %m %d %H %M'):
            allnot.append(y)
        else:
            allmod.append(y)

    numod = len(allmod)
    numnot = len(allnot)
        
    context = {
        "articles": articles,
        "numod": numod,
        "numnot": numnot
        }

    return render(request, "bibtool/update.html", context)


def unknown(request,year, month):

    #if they are NOT loggedin...
    if not request.user.is_authenticated:
        context = {
            "state": "home"
            }
        return render(request, "bibtool/index.html", context)

    username = request.user
    bibgroup = username.bibgroup
    
    articles = Article.objects.filter(created__year=year,created__month=month,inst_id=4,adminbibgroup=bibgroup)
    numunknown = len(articles)

    totart = Article.objects.filter(created__year=year,created__month=month,adminbibgroup=bibgroup)

    numtotal = len(totart)

    #print (numunknown)
    #print (numtotal)
    numknown = numtotal-numunknown

    context = {
        "articles": articles,
        "numunknown": numunknown,
        "numknown": numknown
    }
    return render(request, "bibtool/unknown.html", context)

def post_massupdate(request):

    updatelist = request.POST.getlist('bibcode')
    cfastatus = request.POST["cfastatus"]

    # if the cfastatus is 5, that means this is NOT a CfA record
    if int(cfastatus) == 5:
        bibstatus = 2
    elif int(cfastatus) == 4:
        bibstatus = 3
    # every other status means that this is a CfA record
    else:
        bibstatus = 1

    for y in updatelist:

        new = Article.objects.get(id=y)
        new.status_id = bibstatus
        new.inst_id = cfastatus
        new.save()

    return HttpResponseRedirect(reverse("batch"))


def post_update(request):

    upbib = request.POST["bibcode"]

    cfastatus = request.POST["cfastatus"]
    span_val = request.POST["span_value"]

    if span_val == "unknown":
        #print ("unknown")
        bibstatus = 2
        cfastatus = 4
    else:

        # if the cfastatus is 5, that means this is NOT a CfA record
        if int(cfastatus) == 5:
            #print ("not cfa")
            bibstatus = 2
        elif int(cfastatus) == 4:
            bibstatus = 1
        # every other status means that this is a CfA record
        else:
            #print ("yes cfa")
            bibstatus = 1

    new = Article.objects.get(id=upbib)

    new.status_id = bibstatus
    new.inst_id = cfastatus
    new.save()

    return HttpResponseRedirect(reverse("batch"))