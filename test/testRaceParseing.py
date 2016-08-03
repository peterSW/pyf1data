import pyf1data
import datetime
import unittest


class Race():

    def __init__(self):
        self.driversRaces = {}

    def numDrivers(self):
        return len(self.driversRaces)

    def of(self, driver):
        return self.driversRaces[driver]

    def addDriver(self, driver):
        self.driversRaces[driver] = DriversRace()


class DriversRace:
    pass

def parse_as_race(text):
    race = Race()
    for line in text.splitlines():
        driver = pyf1data.parse_as_driver(line)
        if driver:
             race.addDriver(driver)

    return race


class TestSingleDriverRace(unittest.TestCase):
    data = '''
3 D. RICCIARDO
1
2
3
14:04:36
1:21.599
1:21.346
'''

    def test_num_drivers_is_one(self):
        race = parse_as_race(self.data)
        self.assertEqual(race.numDrivers(), 1)


    def test_ricciardo_has_A_race(self):
        race = parse_as_race(self.data)
        self.assertIsNotNone(race.of(pyf1data.Driver(3, "D. RICCIARDO")))