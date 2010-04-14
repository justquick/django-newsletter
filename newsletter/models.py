from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
import warnings

class SubscriptionManager(models.Manager):
    """
    Newsletter subscription manager
    """
    def is_email_subscribed(self, email):
        try:
            return self.get_query_set().get(email=email).subscribed
        except Subscription.DoesNotExist:
            return False


class SubscriptionBase(models.Model):
    """
    A newsletter subscription base.
    """

    subscribed = models.BooleanField(_('subscribed'), default=True)
    email = models.EmailField(_('email'), unique=True)
    created_on = models.DateTimeField(_("created on"), auto_now_add=True)
    updated_on = models.DateTimeField(_("updated on"), auto_now_add=True,
            auto_now=True)

    objects = SubscriptionManager()
    
    class Meta:
        abstract = True
    
    @classmethod
    def is_subscribed(cls, email):
        """
        Concept inspired by Satchmo. Thanks guys!
        But this is a bad idea. Use manager to check subscription:
        >>> Subscription.objects.is_email_subscribed(email)
        """
        warnings.warn('will be removed in future', DeprecationWarning)
        return cls.objects.is_email_subscribed(email)
    
    def __unicode__(self):
        return u'%s' % (self.email)
        

class Subscription(SubscriptionBase):
    """
    Generic subscription
    """
    pass
        
