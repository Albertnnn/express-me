#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Michael Liao (askxuefeng@gmail.com)'

'''
Runtime functions.
'''

import datetime

UTC_NAME = '(UTC) Coordinated Universal Time'

class UserTimeZone(datetime.tzinfo):
    '''
    User time zone that used to display datetime.
    '''

    def __init__(self, name, utc_hour_offset, utc_min_offset, dst):
        self._name = name
        self._utcoffset = datetime.timedelta(hours=utc_hour_offset, minutes=utc_min_offset)
        self._dst = datetime.timedelta(hours=dst)

    def utcoffset(self, dt):
        return self._utcoffset + self.dst(dt)

    def dst(self, dt):
        return self._dst

    def tzname(self):
        return self._name

# UTC time zone instance:
_UTC_TZ = UserTimeZone(UTC_NAME, 0, 0, 0)

def get_timezone_list():
    '''
    Return timezone list that contains tuples (utc_hour_offset, utc_minute_offset, dst_hour, timezone name).
    '''
    return [
            (-12, 0, 0, '(UTC-12:00) International Date Line West',),
            (-11, 0, 0, '(UTC-11:00) Coordinated Universal Time-11',),
            (-11, 0, 0, '(UTC-11:00) Samoa',),
            (-10, 0, 0, '(UTC-10:00) Hawaii',),
            (-9, 0, 0, '(UTC-09:00) Alaska',),
            (-8, 0, 0, '(UTC-08:00) Baja California',),
            (-8, 0, 0, '(UTC-08:00) Pacific Time (US & Canada)',),
            (-7, 0, 0, '(UTC-07:00) Arizona',),
            (-7, 0, 0, '(UTC-07:00) Chihuahua, La Paz, Mazatlan',),
            (-6, 0, 0, '(UTC-07:00) Mountain Time (US & Canada)',),
            (-6, 0, 0, '(UTC-06:00) Central America',),
            (-6, 0, 0, '(UTC-06:00) Central Time (US & Canada)',),
            (-6, 0, 0, '(UTC-06:00) Guadalajara, Mexico City, Monterrey',),
            (-6, 0, 0, '(UTC-06:00) Saskatchewan',),
            (-5, 0, 0, '(UTC-05:00) Bogota, Lima, Quito',),
            (-5, 0, 0, '(UTC-05:00) Eastern Time (US & Canada)',),
            (-5, 0, 0, '(UTC-05:00) Indiana (East)',),
            (-4, 30, 0, '(UTC-04:30) Caracas',),
            (-4, 0, 0, '(UTC-04:00) Asuncion',),
            (-4, 0, 0, '(UTC-04:00) Atlantic Time (Canada)',),
            (-4, 0, 0, '(UTC-04:00) Cuiaba',),
            (-4, 0, 0, '(UTC-04:00) Georgetown, La Paz, Manaus, San Juan',),
            (-4, 0, 0, '(UTC-04:00) Santiago',),
            (-3, 30, 0, '(UTC-03:30) Newfoundland',),
            (-3, 0, 0, '(UTC-03:00) Brasilia',),
            (-3, 0, 0, '(UTC-03:00) Buenos Aires',),
            (-3, 0, 0, '(UTC-03:00) Cayenne, Fortaleza',),
            (-3, 0, 0, '(UTC-03:00) Greenland',),
            (-3, 0, 0, '(UTC-03:00) Montevideo',),
            (-2, 0, 0, '(UTC-02:00) Coordinated Universal Time-02',),
            (-2, 0, 0, '(UTC-02:00) Mid-Atlantic',),
            (-1, 0, 0, '(UTC-01:00) Azores',),
            (-1, 0, 0, '(UTC-01:00) Cape Verde Is.',),
            (0, 0, 0, '(UTC) Casablanca',),
            (0, 0, 0, UTC_NAME,),
            (0, 0, 0, '(UTC) Dublin, Edinburgh, Lisbon, London',),
            (0, 0, 0, '(UTC) Monrovia, Reykjavik',),
            (1, 0, 0, '(UTC+01:00) Amsterdam, Berlin, Bern, Rome, Stockholm, Vienna',),
            (1, 0, 0, '(UTC+01:00) Belgrade, Bratislava, Budapest, Ljubljana, Prague',),
            (1, 0, 0, '(UTC+01:00) Brussels, Copenhagen, Madrid, Paris'),
            (1, 0, 0, '(UTC+01:00) Sarajevo, Skopje, Warsaw, Zagreb',),
            (1, 0, 0, '(UTC+01:00) West Central Africa',),
            (1, 0, 0, '(UTC+01:00) Windhoek',),
            (2, 0, 0, '(UTC+02:00) Amman',),
            (2, 0, 0, '(UTC+02:00) Athens, Bucharest, Istanbul',),
            (2, 0, 0, '(UTC+02:00) Beirut',),
            (2, 0, 0, '(UTC+02:00) Cairo',),
            (2, 0, 0, '(UTC+02:00) Damascus',),
            (2, 0, 0, '(UTC+02:00) Harare, Pretoria',),
            (2, 0, 0, '(UTC+02:00) Helsinki, Kyiv, Riga, Sofia, Tallinn, Vilnius',),
            (2, 0, 0, '(UTC+02:00) Jerusalem',),
            (2, 0, 0, '(UTC+02:00) Minsk',),
            (3, 0, 0, '(UTC+03:00) Baghdad',),
            (3, 0, 0, '(UTC+03:00) Kuwait, Riyadh',),
            (3, 0, 0, '(UTC+03:00) Moscow, St. Petersburg, Volgograd',),
            (3, 0, 0, '(UTC+03:00) Nairobi',),
            (3, 30, 0, '(UTC+03:30) Tehran',),
            (4, 0, 0, '(UTC+04:00) Abu Dhabi, Muscat',),
            (4, 0, 0, '(UTC+04:00) Baku',),
            (4, 0, 0, '(UTC+04:00) Port Louis',),
            (4, 0, 0, '(UTC+04:00) Tbilisi',),
            (4, 0, 0, '(UTC+04:00) Yerevan',),
            (4, 30, 0, '(UTC+04:30) Kabul',),
            (5, 0, 0, '(UTC+05:00) Ekaterinburg',),
            (5, 0, 0, '(UTC+05:00) Islamabad, Karachi',),
            (5, 0, 0, '(UTC+05:00) Tashkent',),
            (5, 30, 0, '(UTC+05:30) Chennai, Kolkata, Mumbai, New Delhi',),
            (5, 30, 0, '(UTC+05:30) Sri Jayawardenepura',),
            (5, 45, 0, '(UTC+05:45) Kathmandu',),
            (6, 0, 0, '(UTC+06:00) Astana',),
            (6, 0, 0, '(UTC+06:00) Dhaka',),
            (6, 0, 0, '(UTC+06:00) Novosibirsk',),
            (6, 30, 0, '(UTC+06:30) Yangon (Rangoon)',),
            (7, 0, 0, '(UTC+07:00) Bangkok, Hanoi, Jakarta',),
            (7, 0, 0, '(UTC+07:00) Krasnoyarsk',),
            (8, 0, 0, '(UTC+08:00) Beijing, Chongqing, Hong Kong, Urumqi',),
            (8, 0, 0, '(UTC+08:00) Irkutsk',),
            (8, 0, 0, '(UTC+08:00) Kuala Lumpur, Singapore',),
            (8, 0, 0, '(UTC+08:00) Perth',),
            (8, 0, 0, '(UTC+08:00) Taipei',),
            (8, 0, 0, '(UTC+08:00) Ulaanbaatar',),
            (9, 0, 0, '(UTC+09:00) Osaka, Sapporo, Tokyo',),
            (9, 0, 0, '(UTC+09:00) Seoul',),
            (9, 0, 0, '(UTC+09:00) Yakutsk',),
            (9, 30, 0, '(UTC+09:30) Adelaide',),
            (9, 30, 0, '(UTC+09:30) Darwin',),
            (10, 0, 0, '(UTC+10:00) Brisbane',),
            (10, 0, 0, '(UTC+10:00) Canberra, Melbourne, Sydney',),
            (10, 0, 0, '(UTC+10:00) Guam, Port Moresby',),
            (10, 0, 0, '(UTC+10:00) Hobart',),
            (10, 0, 0, '(UTC+10:00) Vladivostok',),
            (11, 0, 0, '(UTC+11:00) Magadan, Solomon Is., New Caledonia',),
            (12, 0, 0, '(UTC+12:00) Auckland, Wellington',),
            (12, 0, 0, '(UTC+12:00) Coordinated Universal Time+12',),
            (12, 0, 0, '(UTC+12:00) Fiji'),
            (13, 0, 0, '(UTC+13:00) Nuku\'alofa'),
    ]

def convert_datetime(naive_datetime, tzinfo):
    return naive_datetime.replace(tzinfo=_UTC_TZ).astimezone(tzinfo)

def format_datetime(naive_dt, tzinfo, format=None):
    '''
    Format datetime.
    '''
    new_dt = naive_dt.replace(tzinfo=_UTC_TZ).astimezone(tzinfo)
    return new_dt.strftime(format is None and '%Y-%m-%d %H:%M:%S' or format)

def format_date(naive_dt, tzinfo, format=None):
    '''
    Format date.
    '''
    new_dt = naive_dt.replace(tzinfo=_UTC_TZ).astimezone(tzinfo)
    return new_dt.strftime(format is None and '%Y-%m-%d' or format)

def format_time(naive_dt, tzinfo, format=None):
    '''
    Format time.
    '''
    new_dt = naive_dt.replace(tzinfo=_UTC_TZ).astimezone(tzinfo)
    return new_dt.strftime(format is None and '%H:%M:%S' or format)

def get_runtime_utils(tzinfo, format=None):
    return {
            'format_datetime' : lambda dt : format_datetime(dt, tzinfo, format),
            'format_date' : lambda dt : format_date(dt, tzinfo, format),
            'format_time' : lambda dt : format_time(dt, tzinfo, format),
    }
