# Create your views here.
import json
from django.shortcuts import render
from django.http import (
    HttpResponse,
    HttpResponseRedirect,
    JsonResponse,
    QueryDict,
)
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView, View
from django.contrib import messages
from drchrono.drchrono_api import AppointmentApi as Api
from drchrono.models import AppointmentStatus


class AppointmentView(View):
    template_name = 'appts.html'
    http_method_names = [u'get', u'post', u'put']

    def _appts(self, request, filter=None):
        '''
            get all Appointments

        '''
        api = Api(request)
        appts = api.get_appointments(verbose=True)
        for appt in appts:
            for status in AppointmentStatus.objects.filter(appointment=appt['id'], patient=appt['patient']['id']):
                appt[status.get_name(status.status)] = status.created_at
        return dict(
            appts=appts,
            statuses=AppointmentStatus.Status._entries.values()
        )

    def _status_update(self, request):
        data = QueryDict(request.body)
        api = Api(request)
        status_types = AppointmentStatus.Status
        patient, status = data['patient'], data['status']
        _appt = AppointmentStatus.objects.filter(appointment=data['id'], patient=patient, status=status).first()
        if _appt is None:
            AppointmentStatus(appointment=data['id'], patient=patient, status=status).save()
            if status in {status_types.complete, status_types.checked_in}:
                return dict(result="failed", message="Cannot update user not Checked In")
        else:
            _appt.status = status.strip()
            _appt.save()

        r = api.update_appointment(data['id'], patient=patient, status=status)
        return dict(result="success", message="success")

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        appts = self._appts(request)
        kwargs.update(appts)

        if request.GET.get('format', None) == "json":
            return JsonResponse(kwargs)
        kwargs.update(wait_times=AppointmentStatus.get_average_wait_times(today=True))
        kwargs.update(overall_wait_times=AppointmentStatus.get_average_wait_times())
        return render(request, self.template_name, kwargs)

    @method_decorator(login_required)
    def put(self, request, *args, **kwargs):
        return JsonResponse(self._status_update(request))


class DoctorView(TemplateView):
    template_name = 'doctor.html'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(DoctorView, self).dispatch(*args, **kwargs)
