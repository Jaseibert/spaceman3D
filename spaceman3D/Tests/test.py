import unittest
from spaceman3D.Orbit import TLE, satellites

class setup_tests:

    def __init__(self):
        return

    def setup_wrong_tle_lengths(self):
        ''' We use this method to setup two test cases of Two-Line Elements (TLE) that have the incorrect number
        of lines. The method returns both of the different test cases. The first is the (long_tle) which has 4
        lines within the TLE, and the second is the (short_tle) which has 2 lines within the tle.

        :return: This method takes
        '''

        long_tle = """ISS (ZARYA)
                      1 25544U 98067A   08264.51782528 -.00002182  00000-0 -11606-4 0  2927
                      2 25544  51.6416 247.4627 0006703 130.5360 325.0288 15.72125391563537
                      3 234 5678"""

        short_tle= """1 25544U 98067A   08264.51782528 -.00002182  00000-0 -11606-4 0  2927
                      2 25544  51.6416 247.4627 0006703 130.5360 325.0288 15.72125391563537"""

        return long_tle, short_tle

class TestSpaceman(unittest.TestCase):

    # tle.parse_tle
    def test_parse_tle_integer(self):
        '''This test is for the TLE().parse_tle method and checks that the AssertionError is raised when
        an integer is passed in to the (tle) parameter of the method.'''
        integer = 1
        with self.assertRaises(AssertionError):
            TLE().parse_tle(tle=integer)

    def test_parse_tle_bool(self):
        '''This test is for the TLE().parse_tle method and checks that the AssertionError is raised when
        an bool value is passed in to the (tle) parameter of the method.'''
        bool = True
        with self.assertRaises(AssertionError):
            TLE().parse_tle(tle=bool)

    def test_parse_tle_float(self):
        '''This test is for the TLE().parse_tle method and checks that the AssertionError is raised when
        an float value is passed in to the (tle) parameter of the method.'''
        float = 1.0
        with self.assertRaises(AssertionError):
            TLE().parse_tle(tle=float)

    def test_parse_tle_short_length(self):
        '''This test is for the TLE().parse_tle method and checks that the AssertionError is raised when
        a tle that has less than three lines is is passed in to the (tle) parameter of the method.'''
        long_tle, short_tle = setup_tests().setup_wrong_tle_lengths()
        with self.assertRaises(AssertionError):
            TLE().parse_tle(tle=short_tle)

    def test_parse_tle_long_length(self):
        '''This test is for the TLE().parse_tle method and checks that the AssertionError is raised when
        a tle that has more than three lines is is passed in to the (tle) parameter of the method.'''
        
        long_tle, short_tle = setup_tests().setup_wrong_tle_lengths()
        with self.assertRaises(AssertionError):
            TLE().parse_tle(tle=long_tle)

    def test_parse_tle_return(self):
        title, line1, line2 = TLE().parse_tle(satellites.Dragon)
        self.assertIsInstance(title, str)
        self.assertIsInstance(line1, str)
        self.assertIsInstance(line2, str)

    def test_checksum_algorithm_integer(self):
        integer = 1
        with self.assertRaises(AssertionError):
            TLE().tle_checksum_algortithm(line=integer)

    def test_parse_tle_bool(self):
        bool = True
        with self.assertRaises(AssertionError):
            TLE().tle_checksum_algortithm(line=bool)

    def test_parse_tle_float(self):
        float = 1.0
        with self.assertRaises(AssertionError):
            TLE().tle_checksum_algortithm(line=float)

    def test_checksum_algorithm_calc_check(self):
        title, line1, line2 = TLE().parse_tle(satellites.Dragon)
        self.assertEqual(TLE().tle_checksum_algortithm(line1), '8')
        self.assertEqual(TLE().tle_checksum_algortithm(line2), '6')


if __name__ == "__main__":
    unittest.main()
