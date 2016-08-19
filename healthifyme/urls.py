from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.auth.views import login
from pollmanagement import views

# Urls. Common Urls are given here while the urls related to polling will be imported from pollmanagement.urls
urlpatterns = [
    url(r'^$', views.homepage),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^polls/', include('pollmanagement.urls', namespace="polls")),
    url(r'^accounts/login/$',  login),
    url(r'^accounts/logout/$', views.logout_view),
    url(r'^accounts/profile/$', views.profile),
    url(r'^registration/register/$', views.register),
    url(r'^contact/$', views.contact),
    url(r'^about/$', views.about),
    url(r'^showresults/$', views.showresults),
    url(r'^addPoll/$', views.addPoll),
    url(r'^savedsuccessfully/$', views.commitPoll),
]
