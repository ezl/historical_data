import time
import datetime

seconds_per_day = 24 * 3600.
seconds_per_year = seconds_per_day * 365.

def datetime2epoch(input):
   return time.mktime(input.timetuple())

def epoch2datetime(epoch):
    return datetime.datetime.fromtimestamp(epoch)

def date2datetime(date):
   return datetime.datetime(date.year, date.month, date.day)

def datetime2date(datetime):
   return datetime.date(datetime.year, datetime.month, datetime.day)

def timedelta2seconds(timedelta):
   return seconds_per_day * timedelta.days + timedelta.seconds

def timedelta2years(timedelta):
   return tdelta2seconds(timedelta) / seconds_per_year
