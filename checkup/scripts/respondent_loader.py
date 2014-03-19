"""
routine for loading respondents from mylawmaker data
works from a json dump of the mylawmaker person data
"""
# first build a dict of respondents in mylawmaker
import datetime
import json

from django.core import serializers
from represent.people.models import *
from represent.location.models import *

SESS = Session.objects.get(session_name="Regular Session 2014")
SEN = Job.objects.get(name='Senator')
REP = Job.objects.get(name='Representative')

bigd = { 'house': {}, 'senate': {} }
x=Person.objects.filter(session=SESS)
reps = x.filter(job=REP)
sens = x.filter(job=SEN)

fields = (
    'email',
    'first_name',
    'home_city',
    'last_name',
    'name_suffix',
    'occupation',
    'pf_page',
    'phone',
    'pk',
    # 'state_id',
    'title',
    'twitter_name',
    'web_site'
)
"""
relations, dates and methods to add:
    'birth_date',
    'district',
    'get_mug',#map to headshot
    'job',#map to title
    'party',
    'tallahassee_office',##map values to office_phone, address, address2, city, state, zip
"""
# MISSING GENDER! values: 'M', 'F'
for rep in reps:
    bigd['house'][rep.person_slug]={}
    repp = bigd['house'][rep.person_slug]
    for field in fields:
        repp[field] = getattr(rep, field) 
    repp['birth_date'] = datetime.datetime.strftime(rep.birth_date, "%Y-%m-%d")
    repp['district'] = rep.district.district_name
    repp['headshot'] = rep.get_mug()       
    repp['title'] = rep.job.job_short_name
    repp['party'] = rep.party.name
    if rep.tallahassee_office:
        repp['office_phone'] = rep.tallahassee_office.phone
        repp['address'] = rep.tallahassee_office.address
        repp['city'] = rep.tallahassee_office.city
        repp['state'] = rep.tallahassee_office.state
        repp['zip'] = rep.tallahassee_office.zip

for sen in sens:
    bigd['senate'][sen.person_slug]={}
    senn = bigd['senate'][sen.person_slug]
    for field in fields:
        senn[field] = getattr(sen, field) 
    senn['birth_date'] = datetime.datetime.strftime(sen.birth_date, "%Y-%m-%d")
    senn['district'] = sen.district.district_name     
    senn['headshot'] = sen.get_mug()       
    senn['title'] = sen.job.job_short_name
    senn['party'] = sen.party.name
    if sen.tallahassee_office:
        senn['office_phone'] = sen.tallahassee_office.phone
        senn['address'] = sen.tallahassee_office.address
        senn['city'] = sen.tallahassee_office.city
        senn['state'] = sen.tallahassee_office.state
        senn['zip'] = sen.tallahassee_office.zip


jfile = 'mylawdata.json'
with open(jfile, 'w') as f:
    f.write(json.dumps(bigd))

# move json file to news-crime server and fire up answers shell

import json
import datetime
from checkup.models import *

jfile = 'mylawdata.json'
with open(jfile, 'r') as f:
    pjson = json.loads(f.read())

PARTIES = {'Democrat': 'D', 'Republican': 'R'}

housd = pjson['house']
send = pjson['senate']

header = housd[housd.keys()[0]].keys()
exclude = [
    'party',
    'pk',
    'occupation',
    'birth_date',
    'home_city',
    'web_site',
    'name_suffix',
    'phone',
    'twitter_name',
    'zip',
    'title'
    ]
for val in exclude:
    header.pop(header.index(val))

grouph = Group.objects.get(name='Florida House')
groups = Group.objects.get(name='Florida Senate')
titleh, c = Title.objects.get_or_create(long="Florida Representative", short="Rep.")
titles, c = Title.objects.get_or_create(long="Florida Senator", short="Sen.")

def load_respondents(dfile, group, title):
    for key, pdict in dfile.items():
        if pdict['twitter_name']==None:
            pdict['twitter_name']=''
        resp = Respondent(
            gender='M', 
            zip=pdict['zip'][:5],
            city=pdict['home_city'],
            office_phone=pdict['phone'], 
            group=group, 
            title=title, 
            myslug=key, 
            party=PARTIES[pdict['party']], 
            website=pdict['web_site'], 
            birth_date=datetime.datetime.strptime(pdict['birth_date'], "%Y-%m-%d").date(),
            twitter=pdict['twitter_name'])
        for each in header:
            setattr(resp, each, pdict[each])
        resp.save()
        print "saved %s" % resp

load_respondents(housd, grouph, titleh)
load_respondents(send, groups, titles)
#fixed gender manually for women



    