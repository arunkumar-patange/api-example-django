#
#
#

import requests
import datetime
import urllib
from datetime import datetime as dt
from dateutil import parser


class API(object):

    url = 'https://drchrono.com'

    @classmethod
    def _url(cls, endpoint, **kwargs):
        url = kwargs.setdefault('url', cls.url)
        return "{}{}?{}".format(kwargs.pop('url'), endpoint, urllib.urlencode(kwargs))

    def __init__(self, request):
        self._r = request
        token = request.user.social_auth.get(provider='drchrono').extra_data.get("access_token")
        self.bearer_token = {'Authorization': 'Bearer {}'.format(token)}

    def get(self, endpoint, **kwargs):
        return requests.get(self._url(endpoint, **kwargs), headers=self.bearer_token)

    def put(self, endpoint, data, **kwargs):
        return requests.put(self._url(endpoint, **kwargs), data=data, headers=self.bearer_token)


class AppointmentApi(API):
    endpoint = "/api/appointments"

    def get_appointments(self, **filters):
        filters = filters or {}
        filters.setdefault('verbose', False)
        filters.setdefault('date', datetime.date.today().isoformat())

        verbose = filters.pop('verbose')
        appts = self.get(self.endpoint, **filters).json()['results']
        if verbose:
            for appt in appts:
                appt['patient'] = PatientApi(self._r).get_patient(appt['patient'])
        return appts

    def get_appointment(self, id):
        '''
            chrono api to get appointment
        '''
        return self.get("{}/{}".format(self.endpoint, id)).json()

    def update_appointment(self, id, **kwargs):
        ''' required fields for the api
            doctor
            duration
            exam_room
            office  integer
            patient integer
            scheduled_time
        '''
        endpoint = "{}/{}".format(self.endpoint, id)
        appt = self.get_appointment(id)
        appt.update(**kwargs)
        r = self.put(endpoint, appt)
        return {'status': 'success'}


class PatientApi(API):
    endpoint = "/api/patients"

    def get_patient(self, id):
        endpoint = "{}/{}".format(self.endpoint, id)
        return self.get(endpoint).json()

    def identify_patient(self, first_name, last_name, ssn=None):
        ssn = ssn and ssn.strip()
        params = dict(
            first_name=first_name.strip(),
            last_name=last_name.strip(),
            # doctor=doctor.id, # 154308
        )
        appts = self.appt().get_appointments()
        time_now = dt.now()
        in_patients = dict()
        for appt in appts:
            if True or parser.parse(appt['scheduled_time']) >= time_now:
                in_patients.setdefault(appt['patient'], []).append(appt)

        patients = self.get(self.endpoint, **params).json()['results']
        for patient in patients:
            if (ssn in (None, '') or
                patient['social_security_number'] == ssn.strip()):
                if patient['id'] in in_patients:
                    _appts = in_patients[patient['id']]
                    return (patient, _appts[0])

    def appt(self):
        return AppointmentApi(self._r)

    def update_patient(self, id, patient_data):
        endpoint = "{}/{}".format(self.endpoint, id)
        self.put(endpoint, patient_data)
        return {'status': 'success'}
