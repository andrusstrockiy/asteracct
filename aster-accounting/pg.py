#!/usr/bin/env python
__author__ = 'andruss'

import datetime, time

timetz = time.tzname[1]


def timestamp(atime=''):
    """Function which generates timestamps according
    the following format
    :rtype : object
    10:11:09.000 UTC Tue Mar 31 2015 if no argument is given
    and convert timedate from 2015-04-14 17:25:37
    to 10:11:09.000 UTC Tue Mar 31 2015
    """
    global timetz
    if atime == '':
        timehms = datetime.datetime.now().strftime("%H:%M:%S")
        # Microseconds
        timemcrs = datetime.datetime.now().strftime("%f")
        timedate = datetime.datetime.now().strftime("%Z %a %b %d %Y")
        return str(timehms + '.' + timemcrs[:3] + ' ' + timetz + timedate)
    else:
        timehms = atime[-8:]
        timemcrs = datetime.datetime.now().strftime("%f")
        mydate = datetime.date(int(atime[0:4]), int(atime[5:7]), int(atime[8:11]))
        timedate = mydate.strftime("%Z %a %b %d %Y")
        return str(timehms + '.' + timemcrs[:3] + ' ' + timetz + timedate)


def main():
    StartTime = '2015-04-15 13:54:52'
    print(timestamp(StartTime))
    print(timestamp())


if __name__ == '__main__':
    main()



