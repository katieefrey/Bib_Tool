# standard lib packages
import sys
import os
import csv

import urllib.parse
import requests
import json

os.environ.setdefault('DJANGO_SETTINGS_MODULE','cfabib.settings')

import django
django.setup()

from bibtool.models import Article

# arts = Article.objects.filter(title=None, status_id=3)

# devkey = (open('dev_key.txt','r')).read()

# for x in arts:
#     print(x)

#     url = 'https://api.adsabs.harvard.edu/v1/search/query/?q=bibcode:'+urllib.parse.quote(x.bibcode)+'&fl=title'
#     print(url)
    
#     headers = {'Authorization': 'Bearer '+devkey}
#     content = requests.get(url, headers=headers)
#     results = content.json()
#     k = results['response']['docs'][0]

#     try:
#         title2 = k['title']
#         print(title2[0])
#         x.title = title2[0]
#         x.save()

#     except KeyError:
#         pass





def add_Article(data1, data2, data3, data4, data5, data6, data7, data8):
    try:
        d, created = Article.objects.get_or_create(bibcode=data1, guess_id=data2, query=data3, affils=data4, adminbibgroup_id=data5, authnum=data6, status_id=data7, inst_id=data8)

        return d

    except django.db.utils.IntegrityError:
        print("already in database")
        return


# with open('check.csv') as csv_file:
#     csv_reader = csv.reader(csv_file, delimiter=',')
#     for row in csv_reader:
#         print(row)

        
#         add_Article(row[0],2,row[3],row[4],1,row[6],3,4)



def add_bibcodes(data1, data2, data5, data7, data8):
    try:
        d, created = Article.objects.get_or_create(bibcode=data1, guess_id=data2, adminbibgroup_id=data5, status_id=data7, inst_id=data8)
        return d

    except django.db.utils.IntegrityError:
        print("already in database")
        return


def mod_falsepos(bibcode):

    mod = Article.objects.get(bibcode=bibcode)
    mod.status_id = 2
    mod.inst_id = 5
    mod.save()



def mod_pos(bibcode):

    mod = Article.objects.get(bibcode=bibcode)
    mod.status_id = 1
    mod.inst_id = 6
    mod.batch_id = 1
    mod.save()



# with open('newbibs_2020_03_16.txt') as csv_file:
#     biblist = csv_file.read()
#     biblist1 = biblist.splitlines()
#     for row in biblist1:
#         print(row)

        
#         add_bibcodes(row,2,1,3,4)
#         mod_pos(row)
