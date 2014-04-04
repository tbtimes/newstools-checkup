#!/usr/bin/env python
'''
Created April 3, 2014
@author: Bill Higgins
'''

import sys, os
from subprocess import call
sys.path.append('/opt/django-projects/.virtualenvs/trauma-answers/answers/')
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")
from settings import AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, S3CMD_BASE, S3_BUCKET
import time
import datetime
import boto
from boto.s3.key import Key
from django.core.mail import send_mail
from django.http import HttpResponse, HttpRequest
from checkup.models import Assignment, Respondent
from checkup import views
from django.template.defaultfilters import slugify

sname = os.path.basename(__file__)
starter = datetime.datetime.now()
tstamp = slugify(starter)

s3=boto.connect_s3(AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY)
bucket = s3.create_bucket(S3_BUCKET)
k=Key(bucket)
x = HttpRequest()
def bake_json():
    """bakes json feeds to s3"""
    o_content = views.overview_feed(x, 'trauma-fee-survey')
    k.key = "answers/checkup/trauma-fee-survey/overview_feed.json"
    k.content_type='application/json'
    k.set_contents_from_string(o_content.content)
    k.set_acl('public-read')
    print "overview_feed.json baked" 
    o_content2 = views.survey_feed(x, 'trauma-fee-survey')
    k.key = "answers/checkup/trauma-fee-survey/feed.json"
    k.content_type='application/json'
    k.set_contents_from_string(o_content2.content)
    k.set_acl('public-read')
    print "feed.json baked" 

if __name__ == "__main__":
    print "%s is in the kitchen, baking breakfast for the queen" % sname
    backup, param = False, False
    try:
        param = sys.argv[1]
    except:
        pass
    else:
        if param and param=='backup':
            backup=True
    print "rendering site to local flat files"
    bake_json()
    call(['python', '/opt/django-projects/.virtualenvs/trauma-answers/answers/manage.py', 'build'])
    if backup:
        print "storing backup"
        call(['sudo', 's3cmd', 'sync', '--acl-public', '/opt/django-projects/.virtualenvs/trauma-answers/answers/build/', 's3://tbtrauma/tstamp/'])
    print "pushing site to s3"
    call(['sudo', 's3cmd', 'sync', '--acl-public', '/opt/django-projects/.virtualenvs/trauma-answers/answers/build/', 's3://tbtrauma'])
    print "bake.py took %s to bake the site to s3" % (datetime.datetime.now()-starter)

