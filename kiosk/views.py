#
#
#


from django.shortcuts import render
from django.http import (
    HttpResponse,
    HttpResponseRedirect,
)
from django.views.generic import TemplateView, View
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils.decorators import method_decorator
from kiosk.forms import (
    VerifyForm,
    DemoForm as DemographForm,
)
from drchrono.drchrono_api import (
    PatientApi as Api,
    AppointmentApi,
    urllib,
)
from drchrono.models import AppointmentStatus
from drchrono.utils import d2o


# Create your views here.
class CheckinView(View):
    template_name = 'kiosk.html',
    form = VerifyForm

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        # patients checkin
        form = self.form()
        return render(
            request,
            self.template_name,
            {'form': form}
        )

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        # patients checkin
        api = Api(request)
        form = self.form(request.POST)
        if form.is_valid():
            data = form.data
            patient = api.identify_patient(data['first_name'], data['last_name'], data['ssn'])
            if patient:
                patient, appt = patient
                AppointmentApi(request).update_appointment(appt['id'], status=AppointmentStatus.Status.checked_in)
                AppointmentStatus(appointment=appt['id'], patient=patient['id'], status=AppointmentStatus.Status.checked_in).save()
                return HttpResponseRedirect('/kiosk/patient/{}?{}'.format(patient['id'], urllib.urlencode(dict(appointment=appt['id']))))
            messages.error(request, 'Please make an appointment')
        return render(
            request,
            self.template_name,
            {'form': form}
        )


class DemoGraphView(View):
    template_name = 'demograph.html',
    form = DemographForm

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        data = Api(request).get_patient(kwargs.pop('patient'))
        form = self.form(initial=data)
        return render(
            request,
            self.template_name,
            {'form': form}
        )

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        # demograph update
        api = Api(request)
        form = self.form(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            patient, appointment = kwargs['patient'], form.data['appointment']
            AppointmentApi(request).update_appointment(appointment, status=AppointmentStatus.Status.arrived)
            AppointmentStatus(appointment=appointment, patient=patient, status=AppointmentStatus.Status.arrived).save()
            api.update_patient(patient, data)
            messages.success(request, 'Please be seated, Dr will see you shortly.')
            return HttpResponseRedirect('/kiosk/checkin')
        return render(request, self.template_name, dict(form=form))
