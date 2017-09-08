from django.conf.urls import include, url
from django.views.generic import TemplateView
from django.contrib.auth import views as auth_views

import views
from views import (
    DoctorView,
    AppointmentView,
)


urlpatterns = [
    url(r'^$', TemplateView.as_view(template_name='login.html'), name='home'),
    url(r'^login/$', TemplateView.as_view(template_name='login.html'), name='home'),

    url(r'', include('social.apps.django_app.urls', namespace='social')),
    url(r'^doctor/$', DoctorView.as_view(), name='index'),
    url(r'^doctor/appointments$', AppointmentView.as_view(), name='appts'),
    url(r'^kiosk/', include('kiosk.urls')),
    url(r'^logout/$', auth_views.logout, {'next_page': '/login/'}, name='logout'),
    url(r'^error$', TemplateView.as_view(template_name='error.html'), name='error'),
]
