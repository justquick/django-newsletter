from django.conf.urls.defaults import *
from django.contrib import admin
from django.views.generic.simple import direct_to_template
from django.conf import settings

admin.autodiscover()

urlpatterns = patterns('newsletter.views',

    url (r'^admin/newsletter/subscription/download/csv/$', 
        view='generate_csv',
        name='download_csv',
    ),
    
    url (r'^$', 
        view='subscribe_detail',
        name='subscribe_detail',
    ),

    url (r'^$',
        view='subscribe_detail',
        name='newlsetter-subscribe',
    ),

    url (r'^subscribed/$', view=direct_to_template, 
        name='newsletter-subscribe-complete', 
        kwargs=dict(template='newsletter/subscribe_complete.html')
    ),
    url (r'^unsubscribed/$', view=direct_to_template, 
        name='newsletter-unsubscribe-complete', 
        kwargs=dict(template='newsletter/unsubscribe_complete.html')
    ),

)
