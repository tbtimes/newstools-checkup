from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls import patterns, url, include
from django.contrib import admin
import settings
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^answers/accounts/login/', 'django.contrib.auth.views.login'),
    url(r'^answers/admin/', include(admin.site.urls)),
    url(r'^answers/dash/$', 'checkup.views.dash'),
    url(r'^answers/checkup/$', include('checkup.urls')),
)

urlpatterns += staticfiles_urlpatterns()


