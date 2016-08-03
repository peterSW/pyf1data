import pyf1data
import datetime
import unittest


class TestDriverParserOnInvalid(unittest.TestCase):
    def test_returns_none_on_empty(self):
        self.assertIsNone(pyf1data.parse_as_driver(""))


class TestDriverParserOnValid(unittest.TestCase):
    def setUp(self):
        self.expectedNumber = 44
        self.expectedName = "L. HAMILTON"
        self.driverString = str(self.expectedNumber) + " " + self.expectedName

    def parse(self):
        return pyf1data.parse_as_driver(self.driverString)

    def test_result_has_number(self):
        self.assertEqual(self.parse().number, self.expectedNumber)

    def test_result_has_name(self):
        self.assertEqual(self.parse().name, self.expectedName)


class TestParseLapNumber(unittest.TestCase):

    def test_gives_none_on_empty(self):
        self.assertIsNone(pyf1data.parse_as_lap_number(""))

    def test_result_has_number(self):
        expected_lap = 29
        self.assertEqual(pyf1data.parse_as_lap_number(str(expected_lap)).number, expected_lap)

    def test_result_with_pit(self):
        self.assertTrue(pyf1data.parse_as_lap_number("18 P").pit)

    def test_gives_none_on_time(self):
        self.assertIsNone(pyf1data.parse_as_lap_number("11:51:12"))



class TestParseFirstLapTime(unittest.TestCase):

    def test_result_is_expected_time(self):
        expected = datetime.time(14, 3, 12)

        self.assertEqual(pyf1data.parse_as_first_lap_time("14:03:12"), expected)


class TestParseLapTime(unittest.TestCase):

    def test_result_is_expected_delta(self):
        expected = datetime.timedelta(minutes=1, seconds=23, milliseconds=162)

        self.assertEqual(pyf1data.parse_as_lap_time("1:23.162"), expected)
