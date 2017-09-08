from django import template
from dateutil import parser


register = template.Library()


@register.filter(name='naturaldelta')
def naturaldelta(delta):
    '''
        timedelta(10) : 10 seconds
    '''
    if not delta:
        return 'N/A'

    days = delta.days
    hours = delta.seconds / 3600
    minutes = delta.seconds % 3600 / 60
    seconds = delta.seconds % 3600 % 60

    str = ""
    tStr = ""
    if days > 0:
        if days == 1:
            tStr = "day"
        else:
            tStr = "days"

        return str + "%s %s" % (days, tStr)
    elif hours > 0:
        if hours == 1:
            tStr = "hour"
        else:
            tStr = "hours"
        str = str + "%s %s" % (hours, tStr)
        return str
    elif minutes > 0:
        if minutes == 1:
            tStr = "min"
        else:
            tStr = "mins"
        str = str + "%s %s" % (minutes, tStr)
        return str
    elif seconds > 0:
        if seconds == 1:
            tStr = "sec"
        else:
            tStr = "secs"
        str = str + "%s %s" % (seconds, tStr)
        return str
    else:
        return 'a moment ago'


@register.filter(name='strtodate')
def strtodate(isostring):
    return parser.parse(isostring)
