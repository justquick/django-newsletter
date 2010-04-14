from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.template import RequestContext
from django.http import *
from django.conf import settings
from django.template.loader import render_to_string
from django.db.models import get_model

from newsletter.models import Subscription
from newsletter.forms import SubscriptionForm
from newsletter.core import csv

import datetime
import re

from django.contrib.admin.views.decorators import staff_member_required

@staff_member_required
def generate_csv(request, model_str="newsletter.subscription", data=None):
    '''
    TODO:
    
    '''

    if not data:
        model = get_model(*model_str.split('.'))
        data = model._default_manager.filter(subscribed=True)
    
    if len(data) == 0:
        data = [["no subscriptions"],]
    return csv.ExcelResponse(data)

def subscribe_detail(request, form_class=SubscriptionForm, 
        template_name='newsletter/subscribe.html',  
        subscribe_success_url=None, unsubscribe_success_url=None,
        extra_context={}, model_str="newsletter.subscription"):

    if request.POST:   
        try:
            model = get_model(*model_str.split('.')) 
            instance = model._default_manager.get(email=request.POST['email'])
        except model.DoesNotExist: 
            instance = None
        form = form_class(request.POST, instance = instance)
        if form.is_valid():
            subscription = form.save()
            if subscription.subscribed:
                return subscribe_success_url or \
                    redirect('newsletter-subscribe-complete')
            return unsubscribe_success_url or \
                redirect('newsletter-unsubscribe-complete')
    else:
        form = form_class()
    
    extra = {
        'form': form,
    }
    extra.update(extra_context)
    
    return render_to_response(template_name, extra, RequestContext(request))

