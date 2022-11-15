from dateutil import relativedelta
from django import template
import datetime

import time as newtime
register = template.Library()


@register.filter('timestamp_to_time')
def convert_timestamp_to_time(timestamp):
    return datetime.datetime.fromtimestamp(int(timestamp))


@register.filter('time')
def custom_time(timestamp):
    date1 = datetime.date.fromtimestamp(int(timestamp))
    date2 = datetime.date.today()
    date = date2-date1
    delta = relativedelta.relativedelta(date2, date1)
    rounds = round(newtime.time()) - timestamp
    if(date.days > 365):
        time = delta.years
        time = str(time) + ' Year ago'
    elif(date.days > 31):
        time = delta.months
        time = str(time) + ' Month ago'
    elif(date.days > 7):
        time = delta.weeks
        time = str(time) + ' Week ago'
    elif(date.days >= 1):
        time = date.days
        time = str(time) + ' Days ago'
    elif(rounds/3600 > 1):
        time = round(rounds/3600)
        time = str(time) + ' hrs ago'
    elif(rounds/3600 < 1):
        time = str(round(rounds/60)) + ' min ago'
    return time
