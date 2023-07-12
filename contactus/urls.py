from __future__ import unicode_literals
from django.conf.urls import url
from django.views.generic import TemplateView
from django.urls import path
from .views import ContactUsView

app_name = 'contactus'

urlpatterns = [
    path('contact/', ContactUsView.as_view(), {}, 'contactus'),
    path('contact/success/', TemplateView.as_view(
        template_name='contactus/contact_success.html'),
        {}, 'contactus-success'),
]
