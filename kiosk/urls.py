from django.conf.urls import url, include

from kiosk import views

urlpatterns = [
    url(r'^checkin/$', views.CheckinView.as_view(), name='kiosk'),
    url(r'^patient/(?P<patient>[0-9]+)/$', views.DemoGraphView.as_view(), name='demographics'),
    url(r'^$', views.CheckinView.as_view(), name='index'),
]
