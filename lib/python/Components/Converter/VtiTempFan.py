from __future__ import absolute_import
from Components.Converter.Converter import Converter
from Components.Element import cached
from Components.Converter.Poll import Poll
import six

SIGN = ' °' if six.PY3 else str(' \xc2\xb0')


class VtiTempFan(Poll, Converter, object):
    TEMPINFO = 1
    FANINFO = 2
    ALL = 5

    def __init__(self, type):
        Poll.__init__(self)
        Converter.__init__(self, type)
        self.type = type
        self.poll_interval = 30000
        self.poll_enabled = True
        if type == 'TempInfo':
            self.type = self.TEMPINFO
        elif type == 'FanInfo':
            self.type = self.FANINFO
        else:
            self.type = self.ALL

    @cached
    def getText(self):
        textvalue = ''
        if self.type == self.TEMPINFO:
            textvalue = self.tempfile()
        elif self.type == self.FANINFO:
            textvalue = self.fanfile()
        return textvalue

    text = property(getText)

    def tempfile(self):
        temp = ''
        unit = ''
        try:
            f = open('/proc/stb/sensors/temp0/value', 'rb')
            temp = f.readline().strip()
            f.close()
            f = open('/proc/stb/sensors/temp0/unit', 'rb')
            unit = f.readline().strip()
            f.close()
            tempinfo = 'TEMP: ' + str(temp) + SIGN + str(unit)
            return tempinfo
        except:
            pass

    def fanfile(self):
        fan = ''
        try:
            f = open('/proc/stb/fp/fan_speed', 'rb')
            fan = f.readline().strip()
            f.close()
            faninfo = 'FAN: ' + str(fan)
            return faninfo
        except:
            pass

    def changed(self, what):
        if what[0] == self.CHANGED_POLL:
            Converter.changed(self, what)
