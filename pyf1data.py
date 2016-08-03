import re
import datetime


class Driver:
    expression = re.compile('(\d+) ([^\W\d]. [^\W\d]+)')

    def __init__(self, number, name):
        self.number = number
        self.name = name

    def __eq__(self, other):
        return other.number == self.number and other.name == self.name

    def __hash__(self):
        return hash((self.number, self.name))


def parse_as_driver(text):
    match = Driver.expression.match(text)
    if match:
        return Driver(int(match.group(1)), match.group(2))
    else:
        return None


class LapNumber:
    simpleLapExpression = re.compile('(\d+)$')
    pitLapExpression = re.compile('(\d+) P$')

    def __init__(self, number, pit=False):
        self.number = number
        self.pit = pit


def parse_as_lap_number(text):
    match = LapNumber.pitLapExpression.match(text)
    if match:
        return LapNumber(int(match.group(1)), True)

    match = LapNumber.simpleLapExpression.match(text)
    if match:
        return LapNumber(int(match.group(1)))

    return None


class FirstLapTime:
    expression = re.compile('(\d+):(\d\d):(\d\d)')


def parse_as_first_lap_time(text):
    match = FirstLapTime.expression.match(text)
    if match:
        return datetime.time(
            int(match.group(1)), int(match.group(2)), int(match.group(3)))
    return None


class LapTime:
    expression = re.compile('(\d+):(\d\d).(\d\d\d)')


def parse_as_lap_time(text):
    match = LapTime.expression.match(text)
    if match:
        return datetime.timedelta(
            minutes=int(match.group(1)),
            seconds=int(match.group(2)),
            milliseconds=int(match.group(3)))
    return None
