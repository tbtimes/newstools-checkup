from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required
from django.conf import settings
from checkup import views

urlpatterns = patterns('',
    # Survey-side
    url(r'^answers/forms/(?P<assignment_id>\d+-\w+)/$', views.surveyform, name='surveyform'),
    url(r'^answers/thanks/(?P<assignment_id>\d+-\w+)/$', views.thanks, name='thanks'),
    
    # Display-side
    url(r'^answers/(?P<survey_slug>[\w-]+)/(?P<slug>[\d]+-[\w-]+)/$',
        login_required(views.AssignmentDetail.as_view()),
        name='assignment_detail'),
    url(r'^answers/(?P<slug>[\w-]+)/$', 
        login_required(views.SurveyDetail.as_view()),
        name='survey_detail'),
    url(r'^answers/(?P<slug>[\w-]+)/feed.json$', 
        views.survey_feed,
        name='survey_feed'),
    url(r'^answers/(?P<slug>[\w-]+)/overview_feed.json$', 
        login_required(views.overview_feed),
        name='overview_feed'),
    url(r'^answers/dash/$', 'checkup.views.dash'),

)