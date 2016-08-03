import pyf1data
import datetime
import unittest



class Race:
    def __init__(self):
        self.driversRaces = {}

    def num_drivers(self):
        return len(self.driversRaces)

    def of(self, driver):
        return self.driversRaces[driver]

    def add_driver(self, driver):
        drivers_race = DriversRace()
        self.driversRaces[driver] = drivers_race
        return drivers_race


class DriversRace:

    def __init__(self):
        self.laps = []
        self.lap_times = []

    def add_lap(self, lap):
        self.laps.append(lap)

    def num_laps(self):
        return len(self.laps)


class RaceParser:

    def __init__(self):
        self.race = Race()
        self.current_parse_method = self.read_driver

        self.drivers_race = []
        self.driver_index = 0

    def read_line(self, line):
        if len(line):
            self.current_parse_method(line)

    def read_driver(self, line):
        driver = pyf1data.parse_as_driver(line)
        if driver:
            self.drivers_race.append(
                self.race.add_driver(driver))
            return True
        elif self.read_lap(line):
            self.current_parse_method = self.read_lap

    def read_lap(self, line):
        lap = pyf1data.parse_as_lap_number(line)
        if lap:
            self.drivers_race[self.driver_index].add_lap(lap)
            return True
        elif self.current_parse_method == self.read_lap:
            if self.read_first_lap_time(line):
                self.current_parse_method = self.read_lap_time

    def read_first_lap_time(self, line):
        first_lap_time = pyf1data.parse_as_first_lap_time(line)
        if first_lap_time:
            self.drivers_race[self.driver_index].first_lap_time = first_lap_time
            return True

    def read_lap_time(self, line):
        lap_time = pyf1data.parse_as_lap_time(line)
        if lap_time:
            self.drivers_race[self.driver_index].lap_times.append(lap_time)
            return True
        elif self.current_parse_method == self.read_lap_time:
            lap_number = pyf1data.parse_as_lap_number(line)
            if lap_number:
                if lap_number.number == 1:
                    self.driver_index += 1

                self.current_parse_method = self.read_lap
                self.current_parse_method(line)

    def skip_rest(self, line):
        pass


def parse_as_race(text):
    parser = RaceParser()
    for line in text.splitlines():
        parser.read_line(line)
    return parser.race


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

    driver = pyf1data.Driver(3, "D. RICCIARDO")

    def test_num_drivers_is_one(self):
        race = parse_as_race(self.data)
        self.assertEqual(race.num_drivers(), 1)

    def test_ricciardo_has_A_race(self):
        race = parse_as_race(self.data)
        self.assertIsNotNone(race.of(self.driver))

    def test_ricciardos_race_has_three_laps(self):
        race = parse_as_race(self.data)
        self.assertEqual(race.of(self.driver).num_laps(), 3)

    def test_ricciardos_race_has_first_lap_time(self):
        race = parse_as_race(self.data)
        self.assertEqual(race.of(self.driver).first_lap_time, pyf1data.parse_as_first_lap_time("14:04:36"))

    def test_ricciardos_race_has_other_lap_times(self):
        race = parse_as_race(self.data)
        expected_lap_times = [pyf1data.parse_as_lap_time("1:21.599"), pyf1data.parse_as_lap_time("1:21.346")]
        self.assertEqual(race.of(self.driver).lap_times, expected_lap_times)

class TestWrappedSingleDriverRace(unittest.TestCase):
    data = '''
3 D. RICCIARDO

1
2
14:04:36
1:21.599

3
1:21.346
'''

    driver = pyf1data.Driver(3, "D. RICCIARDO")

    def test_num_drivers_is_one(self):
        race = parse_as_race(self.data)
        self.assertEqual(race.num_drivers(), 1)

    def test_ricciardo_has_A_race(self):
        race = parse_as_race(self.data)
        self.assertIsNotNone(race.of(self.driver))

    def test_ricciardos_race_has_three_laps(self):
        race = parse_as_race(self.data)
        self.assertEqual(race.of(self.driver).num_laps(), 3)

    def test_ricciardos_race_has_first_lap_time(self):
        race = parse_as_race(self.data)
        self.assertEqual(race.of(self.driver).first_lap_time, pyf1data.parse_as_first_lap_time("14:04:36"))

    def test_ricciardos_race_has_other_lap_times(self):
        race = parse_as_race(self.data)
        expected_lap_times = [pyf1data.parse_as_lap_time("1:21.599"), pyf1data.parse_as_lap_time("1:21.346")]
        self.assertEqual(race.of(self.driver).lap_times, expected_lap_times)

class TestTwoDriverRace(unittest.TestCase):
    data = '''
3 D. RICCIARDO

4 P. RICCIARDO

1

14:04:36

1

15:23:00
'''

    driver1 = pyf1data.Driver(3, "D. RICCIARDO")
    driver2 = pyf1data.Driver(4, "P. RICCIARDO")

    def test_num_drivers_is_two(self):
        race = parse_as_race(self.data)
        self.assertEqual(race.num_drivers(), 2)

    def test_ricciardo_has_A_race(self):
        race = parse_as_race(self.data)
        self.assertIsNotNone(race.of(self.driver1))

    def test_ricciardos_race_has_three_laps(self):
        race = parse_as_race(self.data)
        self.assertEqual(race.of(self.driver1).num_laps(), 1)

    def test_ricciardos_race_has_first_lap_time(self):
        race = parse_as_race(self.data)
        self.assertEqual(race.of(self.driver1).first_lap_time, pyf1data.parse_as_first_lap_time("14:04:36"))

    def test_driver2_has_lap_time(self):
        race = parse_as_race(self.data)
        self.assertEqual(race.of(self.driver2).first_lap_time, pyf1data.parse_as_first_lap_time("15:23:00"))
