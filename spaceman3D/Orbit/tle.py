from datetime import datetime, timedelta
import pytz as tz
import pandas as pd

class tle(object):

    def __init__(self):
        return

    def parse_tle(self,tle=None):
        '''Parses and cleans a Two line Element (TLE) into individual lines.

        :param tle: a Two-Line Element (TLE).
        :return: The individual lines from the TLE.
        '''
        title, line1, line2 = map(lambda x: x.strip(), tle.split('\n'))
        return title, line1, line2

    def tle_checksum_algortithm(self,line=None):
        '''This function defines the modulo 10 checksum algorithm used to determine validity of the TLE lines.

        :param line: the line to be verified.
        :return: the mod 10 checksum.
        '''
        line = line.replace('-','1')
        ind_val = [int(d) for d in line if d.isdigit()]
        del ind_val[-1]
        mod10_chksum = sum(ind_val) % 10
        return mod10_chksum

    def validation_framework(self,condition1=None, condition2=None, expected1=None, expected2=None,dual_condition=True):
        '''This function defines two conditional tests that will be used to check the TLE data.

        :param condition1: The first condition that is to be verified.
        :param condition2: A second condition that is to be verified.
        :param expected1: The expected value of the first condition.
        :param expected2: The expected value of the second condition.
        :param dual condition: Indicator for the number of conditions being tested.
        :return: A boolean value of the conditions being tested.
        '''
        if dual_condition is False:
            if str(condition1) == str(condition2):
                return True
            else:
                return False
        else:
            if str(condition1) == str(expected1) and str(condition2) == str(expected2):
                return True
            else:
                return False

    def check_valid_tle(self,tle=None):
        '''This function validates the TLE by checking that several tle elements are correct.

        :param tle: a Two-Line Element (TLE).
        :return: A boolean value indicating the validity of the data in the TLE.
        '''
        title, line1, line2 =  self.parse_tle(tle)
        line_index_chk = self.validation_framework(line1[0],line2[0],'1','2')
        sat_number_chk = self.validation_framework(line1[2:7],line2[2:7],dual_condition=False)
        checksum_chk = self.validation_framework(line1[-1],line2[-1],self.tle_checksum_algortithm(line1), self.tle_checksum_algortithm(line2))
        if line_index_chk and sat_number_chk and checksum_chk is True:
            return True
        else:
            return False

    def scientific_notation_conversion(self, element=None):
        '''This function takes the tle format of floats (01234-5) a + or -, and converts them into 1.234e-08.

        :param element: a element that needs converting to a float. (Example: 01234-5)
        :return: the float version of the element.
        '''
        exp = int(element[-2:])
        base = int(element[:-2])
        #Needs to be improved, but works.
        decimal_places = int(len(str(abs(int(element[:-2])))))
        multiplier = 0.1 ** decimal_places
        base = multiplier * base
        exponent =  10 ** exp
        return base * exponent

    def decimal_conversion(self, element=None):
        '''This function converts a string of an integer to a float.

        :param element: A string of an integer.
        :return: a float of the string integer.
        '''
        value = float(f'{element[0]}.{element[1:]}')
        return value

    def individual_element(self, tle=None, line=None, start=None, end=None, func=None):
        '''This function is the template to parse the individual elements.

        :param tle: a Two-Line Element (TLE).
        :param line: The line in the TLE that the elment being parsed is contained in.
        :param start: The starting position within the specified line for the element.
        :param end: The ending position within the specified line for the element.
        :param func: The function that is used to convert to the element to the infered form.
        :return: The properly formatted element.
        '''
        title, line1, line2 =  self.parse_tle(tle)
        if self.check_valid_tle(tle) is True:
            if line == 1:
                line = line1
            elif line == 2:
                line = line2
            else:
                pass
            if func is not None:
                value = func(line[start:end])
            else:
                value = line[start:end]
        else:
            assert self.check_valid_tle(tle) is True, "Your TLE data doesn't apppear to be correct, check the data and try again."
        return value

    def tle_sat_identity_elements(self, tle=None):
        '''This function parses and returns the satellite's identifying elements as individual components.

        :param tle: a Two-Line Element (TLE).
        :return: The satellites identifying elements.
        '''
        title, line1, line2 =  self.parse_tle(tle)
        if self.check_valid_tle(tle) is True:
            satellite_number = int(line1[2:7])
            classification = line1[7:8]
            international_designator_year = int(line1[9:11])
            international_designator_launch_number = int(line1[11:14])
            international_designator_piece_of_launch = line1[14:17]
            element_set_number = float(line1[64:68])
        else:
            assert self.check_valid_tle(tle) is True, "Your TLE data doesn't apppear to be correct, check the data and try again."
        return satellite_number, classification, international_designator_year, international_designator_launch_number,
        international_designator_piece_of_launch, element_set_number

    def tle_keplerian_elements(self, tle=None):
        '''This function parses and returns the Keplerian "Orbital" elements as individual components.

        :param tle: a Two-Line Element (TLE).
        :return: The satellites identifying elements.
        '''
        title, line1, line2 =  self.parse_tle(tle)
        if self.check_valid_tle(tle) is True:
            inclination = float(line2[8:16])
            right_ascension = float(line2[17:25])
            eccentricity = self.decimal_conversion(line2[26:33])
            argument_periapsis = float(line2[34:42])
            mean_anomaly = float(line2[43:51])
            mean_motion = float(line2[52:63])
            epoch_year = int(line1[18:20])
            year = (
                2000 + epoch_year
                if epoch_year < 70
                else 1900 + epoch_year
            )
            epoch = float(line1[20:32])
            epoch_date = datetime(year=year, month=1, day=1, tzinfo=tz.utc) + timedelta(days=epoch-1)
            return title, inclination, right_ascension, eccentricity, argument_periapsis, mean_anomaly, mean_motion, epoch_date
        else:
            assert self.check_valid_tle(tle) is True, "Your TLE data doesn't apppear to be correct, check the data and try again."

#################### Parsing the individual TLE components ####################

    def ballistic_coeffecient(self, tle=None):
        '''This function parses and returns the ballistic coeffecient. This is also called the first
        derivative of mean motion. It is defined as the daily rate of change in the number of revolutions
        that an orbiting object completes each day, divided by 2. This is "catch all"drag term used in
        the Simplified General Perturbations (SGP4) USSPACECOM predictor. (NASA 1)

        Definition Citation:
        1. “Definition of Two-line Element Set Coordinate System.” SpaceFlight, National Aeronautics and Space Administration,
                23, Sept. 2011, https://spaceflight.nasa.gov/realdata/sightings/SSapplications/Post/JavaSSOP/SSOP_Help/tle_def.html.

        :param tle: a Two-Line Element (TLE).
        :type tle: str
        :return: Ballistic Coeffecient (Revolutions/Day)
        '''
        first_time_derivative_of_the_mean_motion_divided_by_two = self.individual_element(tle,1,33,43,func=float)
        return first_time_derivative_of_the_mean_motion_divided_by_two

    def second_time_derivative_of_mean_motion(self, tle=None):
        '''This function parses and returns the second derivative of mean motion from the TLE element.
        The second derivative of mean motion is a second order drag term in the SGP4 predictor used to
        model terminal orbit decay. It measures the second time derivative in daily mean motion, divided
        by 6. (NASA 1)

        Definition Citation:
        1. “Definition of Two-line Element Set Coordinate System.” SpaceFlight, National Aeronautics and Space Administration,
                23, Sept. 2011, https://spaceflight.nasa.gov/realdata/sightings/SSapplications/Post/JavaSSOP/SSOP_Help/tle_def.html.

        :param tle: a Two-Line Element (TLE).
        :type tle: str
        :return: The 2nd Time Derivative of Mean Motion (Revolutions/Day^3)
        '''
        second_time_derivative_of_mean_motion_divided_by_six = self.individual_element(tle,1,44,52,func=self.scientific_notation_conversion)
        return second_time_derivative_of_mean_motion_divided_by_six

    def bstar_drag_term(self, tle=None):
        '''This function parses and returns the BSTAR drag term from the TLE element. Also called the
        radiation pressure coefficient, the parameter is another drag term in the SGP4 predictor. (NASA 1)

        Definition Citation:
        1. “Definition of Two-line Element Set Coordinate System.” SpaceFlight, National Aeronautics and Space Administration,
                23, Sept. 2011, https://spaceflight.nasa.gov/realdata/sightings/SSapplications/Post/JavaSSOP/SSOP_Help/tle_def.html.

        :param tle: a Two-Line Element (TLE).
        :return: The B-Star Drag Term (earth radii^-1)
        '''
        bstar_drag_term = self.individual_element(tle,1,53,61,func=self.scientific_notation_conversion)
        return bstar_drag_term

    def satellite_number_and_classification(self, tle=None):
        '''This function parses and returns the satellite number and the classification from the TLE element. Similar to
        the International Designator, the satellite number is a naming convention used to catalog satellites by the
        United States Space Command (USSPACECOM). Each geocentric satellite is tracked and denoted by a 5-digit satellite
        number, and is given a classification for each piece of the satellite. (U is an Unclassified piece) (Wikipeda 1)

        Definition Citation:
        1. “Satellite Catalog Number.” Wikipedia,
                7, Feb. 2018, https://en.wikipedia.org/wiki/Satellite_Catalog_Number

        :param tle: a Two-Line Element (TLE).
        :return: The Satellites Number and its Classification.
        '''
        satellite_number = self.individual_element(tle,1,2,8,func=str)
        classification = satellite_number[-1:]
        satellite_number = int(satellite_number)
        return satellite_number, classification

    def international_designator_year(self, tle=None):
        '''This function parses and returns the international designator year from the TLE element. The International
        Designator, also known as the COSPAR designation, or in the U.S as NSSDC ID, is a naming convention for satellites
        parts. It consists of the launch year, a launch number of that year, and a code identifying each of a piece
        in a launch (Wikipedia 1). This function returns the first portion
        of the international designator parameter, which is the year of launch.

        Definition Citation:
        1. “International Designator.” Wikipedia,
                15, May 2018, https://en.wikipedia.org/wiki/International_Designator.

        :param tle: a Two-Line Element (TLE).
        :return: The International Designator Year
        '''
        international_designator_year = self.individual_element(tle,1,9,11,func=int)
        return international_designator_year

    def international_designator_launch_number(self, tle=None):
        '''This function parses and returns the international designator launch number from the TLE element. The International
        Designator, also known as the COSPAR designation, or in the U.S as NSSDC ID, is a naming convention for satellites
        parts. It consists of the launch year, a 3-digit incrementing launch number of that year and up to a code
        representing the sequential identifier of a piece in a launch (Wikipedia 1) . This function returns the second portion
        of the international designator parameter, which is the number associated with launch.

        Definition Citation:
        1. “International Designator.” Wikipedia,
                15, May 2018, https://en.wikipedia.org/wiki/International_Designator.

        :param tle: a Two-Line Element (TLE).
        :return: The International Designator Launch Number.
        '''
        international_designator_launch_number  = self.individual_element(tle,1,11,14,func=int)
        return international_designator_launch_number

    def international_designator_piece_of_launch(self, tle=None):
        '''This function parses and returns the international designator launch number from the TLE element. The International
        Designator, also known as the COSPAR designation, or in the U.S as NSSDC ID, is a naming convention for satellites
        parts. It consists of the launch year, a launch number of that year, and a code identifying each of a piece in a launch
        (Wikipedia 1). This function returns the second portion of the international designator parameter, which is the identifier
        associated with the launch piece.

        Definition Citation:
        1. “International Designator.” Wikipedia,
                15, May 2018, https://en.wikipedia.org/wiki/International_Designator.

        :param tle: a Two-Line Element (TLE).
        :return: the international_designator_piece_of_launch element.
        '''
        international_designator_piece_of_launch  = self.individual_element(tle,1,14,17,func=str)
        return international_designator_piece_of_launch

    def element_set_number(self, tle=None):
        '''This function parses and returns the element set number from the TLE element.

        :param tle: a Two-Line Element (TLE).
        :return: the Element Set Number.
        '''
        element_set_number = self.individual_element(tle,1,64,68,func=float)
        return element_set_number

    def epoch_year(self, tle=None, full_year=False):
        '''This function parses and returns the epoch year, or the year from the TLE element.

        :param tle: a Two-Line Element (TLE).
        :return: either the full year (4-digits) or the epoch year (2-digits).
        '''
        epoch_year = self.individual_element(tle,1,18,20,func=int)
        #return epoch_year
        try:
            if full_year is not False:
                if epoch_year < 70:
                    year = 2000 + epoch_year
                else:
                    year = 1900 + epoch_year
                return year
            else:
                return epoch_year
        except:
            assert full_year is not False or True, "The full_year argument must be a Boolean value"

    def epoch(self, tle=None):
        '''This function parses and returns the epoch (days) from the TLE element. The epoch parameter
        denotes the number of Julian calander days within the epoch year that this TLE element was created.

        :param tle: a Two-Line Element (TLE).
        :return: the epoch (Julian Calander Days)
        '''
        epoch = self.individual_element(tle,1,20,32,func=float)
        return epoch

    def epoch_date(self, tle=None):
        '''This function parses and returns the epoch date from the TLE element.

        :param tle: a Two-Line Element (TLE).
        :return: the formatted Epoch Date & TimeStamp
        '''
        epoch = self.epoch(tle)
        year = self.epoch_year(tle,full_year=True)
        epoch_date = datetime(year=year, month=1, day=1, tzinfo=tz.utc) + timedelta(days=epoch-1)
        return epoch_date

    def inclination(self, tle=None):
        '''This function parses and returns the orbital inclination of the satellite from the TLE element.
        The orbital inclincation is the average angle between the equator and the orbit plane. The
        value provided is the TEME mean inclination. (NASA 1)

        Definition Citation:
        1. “Definition of Two-line Element Set Coordinate System.” SpaceFlight, National Aeronautics and Space Administration,
                23, Sept. 2011, https://spaceflight.nasa.gov/realdata/sightings/SSapplications/Post/JavaSSOP/SSOP_Help/tle_def.html.

        :param tle: a Two-Line Element (TLE).
        :return: the TEME mean inclination.
        '''
        inclination = self.individual_element(tle,2,8,16,func=float)
        return inclination

    def right_ascension(self, tle=None):
        '''This function parses and returns the right ascension of the satellites orbit from the TLE element.
        The right ascension parameter from a TLE denotes the angle between vernal equinox and the point where
        the orbit crosses the equatorial plane in the Northern direction. The specific right ascenion parameter
        derived from the TLE is the TEME mean right ascension of the ascending node. (NASA 1)

        Definition Citation:
        1. “Definition of Two-line Element Set Coordinate System.” SpaceFlight, National Aeronautics and Space Administration,
                23, Sept. 2011, https://spaceflight.nasa.gov/realdata/sightings/SSapplications/Post/JavaSSOP/SSOP_Help/tle_def.html.

        :param tle: a Two-Line Element (TLE).
        :return: the TEME mean right ascension of the ascending node.
        '''
        right_ascension = self.individual_element(tle,2,17,25,func=float)
        return right_ascension

    def eccentricity(self, tle=None):
        '''This function parses and returns the orbital eccentricity from the TLE element. The eccentricity of an
        astronomical object is a parameter that defines the shape of an orbit. The closer the eccentricity parameter
        is to 0, the more circular the orbit. The closer the eccentricity parameter is to 1 the more elliptical the orbit.
        Any eccentricity greater than a 1, the orbit is a parabolic escape orbit. The value supplied in the TLE is the
        average eccentricity. (NASA 1)

        Definition Citation:
        1. “Definition of Two-line Element Set Coordinate System.” SpaceFlight, National Aeronautics and Space Administration,
                23, Sept. 2011, https://spaceflight.nasa.gov/realdata/sightings/SSapplications/Post/JavaSSOP/SSOP_Help/tle_def.html.

        :param tle: a Two-Line Element (TLE).
        :return: the average eccentricity parameter.
        '''
        eccentricity = self.individual_element(tle,2,26,33,func=self.decimal_conversion)
        return eccentricity

    def argument_periapsis(self, tle=None):
        '''This function parses and returns the argument of periapsis of the satellites orbit from the TLE element.
        The argument of periapsis is the angle between the ascending node and the orbit's point of closest approach to
        the earth, otherwise known as the orbit's "perigee". The term "perigee" is in the term used exlcusively for
        geocentric orbits, but is a specification on the more broad term "periapsis". The value provided in the TLE is
        the TEME mean argument of perigee.

        Definition Citation:
        1. “Definition of Two-line Element Set Coordinate System.” SpaceFlight, National Aeronautics and Space Administration,
                23, Sept. 2011, https://spaceflight.nasa.gov/realdata/sightings/SSapplications/Post/JavaSSOP/SSOP_Help/tle_def.html.

        :param tle: a Two-Line Element (TLE).
        :return: the TEME Mean Argument of Perigee. (Degrees)
        '''
        argument_periapsis = self.individual_element(tle,2,34,42,func=float)
        return argument_periapsis

    def mean_anomaly(self, tle=None):
        '''This function parses and returns the mean anomaly of the satellites orbit from the TLE element.
        The mean anomaly parameter measures the angle from satellite's perigee, of the satellite location in the orbit
        referenced to a circular orbit with radius equal to the semi-major axis. (NASA 1) The mean anomaly can be thought of as
        the fraction of an elliptical orbit's period that has elapsed since the orbiting body passed perigee. (Wikipedia 2)

        Definition Citation:
        1. “Definition of Two-line Element Set Coordinate System.” SpaceFlight, National Aeronautics and Space Administration,
                23, Sept. 2011, https://spaceflight.nasa.gov/realdata/sightings/SSapplications/Post/JavaSSOP/SSOP_Help/tle_def.html.

        2. “Mean Anomaly.” Wikipedia,
                17, Jan. 2019, https://en.wikipedia.org/wiki/Mean_anomaly.

        :param tle: a Two-Line Element (TLE).
        :return: the Mean Anomaly (Degrees)
        '''
        mean_anomaly = self.individual_element(tle,2,43,51,func=float)
        return mean_anomaly

    def mean_motion(self, tle=None):
        '''This function parses and returns the mean motion of the satellites orbit from the TLE element. The value is
        the mean number of orbits per day the object completes. (NASA 1)

        Definition Citation:
        1. “Definition of Two-line Element Set Coordinate System.” SpaceFlight, National Aeronautics and Space Administration,
                23, Sept. 2011, https://spaceflight.nasa.gov/realdata/sightings/SSapplications/Post/JavaSSOP/SSOP_Help/tle_def.html.

        :param tle: a Two-Line Element (TLE).
        :return: the Mean Motion (Average Number of Orbits/day).
        '''
        mean_motion = self.individual_element(tle,2,52,63,func=float)
        return mean_motion

    def revolution(self, tle=None):
        '''This function parses and returns the satellites orbital revolution from the TLE element. The orbit number
        at Epoch Time. This time is chosen very near the time of true ascending node passage as a matter of routine.
        (NASA 1)

        Definition Citation:
        1. “Definition of Two-line Element Set Coordinate System.” SpaceFlight, National Aeronautics and Space Administration,
                23, Sept. 2011, https://spaceflight.nasa.gov/realdata/sightings/SSapplications/Post/JavaSSOP/SSOP_Help/tle_def.html.

        :param tle: a Two-Line Element (TLE).
        :return: the orbital Revolution (Number of Revolutions ).
        '''
        revolution = self.individual_element(tle,2,63,68,func=float)
        return revolution

    def tle_to_dataframe(self, tle=None):
        '''This function take a Two-Line Element and converts its elements into a Pandas DataFrame.

        :param tle: a Two-Line Element (TLE).
        :return: a Pandas DataFrame.
        '''
        satellite_number, classification, international_designator_year, international_designator_launch_number,international_designator_piece_of_launch,element_set_number = self.tle_sat_identity_elements(tle)
        title, inclination, right_ascension, eccentricity, argument_periapsis, mean_anomaly, mean_motion, epoch_date = self.tle_keplerian_elements(tle)
        revolution = self.revolution(tle)
        bstar_drag_term = self.bstar_drag_term(tle)
        second_time_derivative_of_mean_motion = self.second_time_derivative_of_mean_motion(tle)
        ballistic_coeffecient = self.ballistic_coeffecient(tle)
        sat_elements = {
            'title': title,
            'satellite_number': satellite_number,
            'classification': classification,
            'international_designator_year': international_designator_year,
            'international_designator_launch_number': international_designator_launch_number,
            'international_designator_piece_of_launch': international_designator_piece_of_launch,
            'element_set_number': element_set_number,
            'inclination': inclination,
            'right_ascension': right_ascension,
            'eccentricity': eccentricity,
            'argument_periapsis': argument_periapsis,
            'mean_anomaly': mean_anomaly,
            'mean_motion': mean_motion,
            'epoch_date': epoch_date,
            'revolution': revolution,
            'bstar_drag_term': bstar_drag_term,
            'second_time_derivative_of_mean_motion': second_time_derivative_of_mean_motion,
            'ballistic_coeffecient': ballistic_coeffecient
        }
        df = pd.DataFrame(sat_elements,index=[0])
        return df
