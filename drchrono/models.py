import datetime

from django.contrib.auth.models import User
from django.db import models
from collections import defaultdict
from drchrono.utils import d2o


# Create your models here.
class UserExtension(models.Model):

    id = models.AutoField(primary_key=True)
    created_time = models.DateTimeField(auto_now_add=True)
    user = models.OneToOneField(User, related_name='extension')
    is_deleted = models.BooleanField(default=False)


class AppointmentStatus(models.Model):
    '''
        One of "", "Arrived", "Checked In", \
               "In Room", "Cancelled", "Complete", "Confirmed", "In Session", "No Show", "Not Confirmed", or "Rescheduled"
    '''

    Status = d2o(dict(
        # no_show: No Show
        ('_'.join(name.lower().split()), name)
        for name in (
            "",
            "Arrived",
            "Checked In",
            # "In Room",
            # "Cancelled",
            "Complete",
            "Confirmed",
            "In Session",
            "No Show",
            # "Not Confirmed",
            # "Rescheduled",
        )
    ))

    created_at = models.DateTimeField(auto_now_add=True)
    appointment = models.IntegerField(db_index=True)
    patient = models.IntegerField(db_index=True)
    status = models.CharField(max_length=20)

    @classmethod
    def get_name(cls, status):
        '''
            in_session_at
        '''
        for key, v in cls.Status._entries.iteritems():
            if v == status:
                return "{}_at".format(key)

    @classmethod
    def get_average_wait_times(cls, today=False):
        # [{appointment: 1, status:"Arrived"}, {appointment: 1, status:"In Session"}]
        groups = cls.objects.all()
        if today:
            groups = groups.filter(created_at__startswith=datetime.date.today())

        groups = groups.values('appointment', 'status', 'created_at')
        appointments = defaultdict(dict)
        # wait times for patients
        _wait_times = []
        for group in groups:
            appointments[group['appointment']][group['status']] = group['created_at']
            if (
                cls.Status.arrived in appointments[group['appointment']] and
                cls.Status.in_session in appointments[group['appointment']]
            ):
                arrived_at = appointments[group['appointment']][cls.Status.arrived]
                in_session_at = appointments[group['appointment']][cls.Status.in_session]
                _wait_times.append(in_session_at - arrived_at)

        if len(_wait_times) > 0:
            return sum(_wait_times, datetime.timedelta()) / len(_wait_times)
