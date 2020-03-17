# standard lib packages
import sys
import os
import csv

os.environ.setdefault('DJANGO_SETTINGS_MODULE','cfabib.settings')

import django
django.setup()

from bibtool.models import Article

def add_Article(data1, data2, data3, data4, data5, data6, data7, data8):
    d, created = Article.objects.get_or_create(bibcode=data1, guess_id=data2, query=data3, affils=data4, adminbibgroup_id=data5, authnum=data6, status_id=data7, inst_id=data8)

    return d


with open('check.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    for row in csv_reader:
        print(row)

        
        add_Article(row[0],2,row[3],row[4],1,row[6],3,4)


"""
# STATUS
CfA
Not CfA
maybe
doubtful


#AFFIL
HCO
SAO
Both
unknown
neither
either

# GUESS
likely
review
review-visit
review-nonsao
revire-noncfa
doubful

# bibgroup
CfA

"""





# devkey = (open('dev_key.txt','r')).read()

# matches = (open('dev_key.txt','r')).read()

# falsepos = (open('dev_key.txt','r')).read()




# inc_aff_list = incafflist.splitlines()