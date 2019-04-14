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
    def first_derivative_mean_motion_divided_by_two(self, tle=None):
        '''This function parses and returns the first derivative mean motion from the TLE element.

        :param tle: a Two-Line Element (TLE).
        :return: The 1st Time Derivative of the Mean of Motion / 2
        '''
        first_time_derivative_of_the_mean_motion_divided_by_two = self.individual_element(tle,1,33,43,func=float)
        return first_time_derivative_of_the_mean_motion_divided_by_two

    def second_time_derivative_of_mean_motion_divided_by_six(self, tle=None):
        '''This function parses and returns the second derivative of mean motion from the TLE element.

        :param tle: a Two-Line Element (TLE).
        :return: The 2nd Time Derivative of the Mean of Motion / 6
        '''
        second_time_derivative_of_mean_motion_divided_by_six = self.individual_element(tle,1,44,52,func=self.scientific_notation_conversion)
        return second_time_derivative_of_mean_motion_divided_by_six

    def bstar_drag_term(self, tle=None):
        '''This function parses and returns the Bstar drag term from the TLE element.

        :param tle: a Two-Line Element (TLE).
        :return: The B-Star Drag Term.
        '''
        bstar_drag_term = self.individual_element(tle,1,53,61,func=self.scientific_notation_conversion)
        return bstar_drag_term

    def satellite_number_and_classification(self, tle=None):
        '''This function parses and returns the satellite number and the classification from the TLE element.

        :param tle: a Two-Line Element (TLE).
        :return: The Satellites Number and its Classification.
        '''
        satellite_number = self.individual_element(tle,1,2,8,func=str)
        classification = satellite_number[-1:]
        satellite_number = int(satellite_number)
        return satellite_number, classification

    def international_designator_year(self, tle=None):
        '''This function parses and returns the international designator year from the TLE element.

        :param tle: a Two-Line Element (TLE).
        :return: The International Designator Year
        '''
        international_designator_year = self.individual_element(tle,1,9,11,func=int)
        return international_designator_year

    def international_designator_launch_number(self, tle=None):
        '''This function parses and returns the international designator launch number from the TLE element.

        :param tle: a Two-Line Element (TLE).
        :return: The International Designator Launch Number.
        '''
        international_designator_launch_number  = self.individual_element(tle,1,11,14,func=int)
        return international_designator_launch_number

    def international_designator_piece_of_launch(self, tle=None):
        '''This function parses and returns the international designator launch number from the TLE element.

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
        '''This function parses and returns the epoch year from the TLE element'''
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
        '''This function parses and returns the epoch (days) from the TLE element'''
        epoch = self.individual_element(tle,1,20,32,func=float)
        return epoch

    def epoch_date(self, tle=None):
        '''This function parses and returns the epoch date from the TLE element'''
        epoch = self.epoch(tle)
        year = self.epoch_year(tle,full_year=True)
        epoch_date = datetime(year=year, month=1, day=1, tzinfo=tz.utc) + timedelta(days=epoch-1)
        return epoch_date

    def inclination(self, tle=None):
        '''This function parses and returns the inclination of the satellite from the TLE element'''
        inclination = self.individual_element(tle,2,8,16,func=float)
        return inclination

    def right_ascension(self, tle=None):
        '''This function parses and returns the right_ascension of the satellites orbit from the TLE element'''
        right_ascension = self.individual_element(tle,2,17,25,func=float)
        return right_ascension

    def eccentricity(self, tle=None):
        '''This function parses and returns the eccentricity of the satellites orbit from the TLE element'''
        eccentricity = self.individual_element(tle,2,26,33,func=self.decimal_conversion)
        return eccentricity

    def argument_periapsis(self, tle=None):
        '''This function parses and returns the argument of periapsis of the satellites orbit from the TLE element'''
        argument_periapsis = self.individual_element(tle,2,34,42,func=float)
        return argument_periapsis

    def mean_anomaly(self, tle=None):
        '''This function parses and returns the mean anomaly of the satellites orbit from the TLE element'''
        mean_anomaly = self.individual_element(tle,2,43,51,func=float)
        return mean_anomaly

    def mean_motion(self, tle=None):
        '''This function parses and returns the mean motion of the satellites orbit from the TLE element'''
        mean_motion = self.individual_element(tle,2,52,63,func=float)
        return mean_motion

    def revolution(self, tle=None):
        '''This function parses and returns the satellites revolution from the TLE element'''
        revolution = self.individual_element(tle,2,63,68,func=float)
        return revolution

    def tle_to_dataframe(self, tle=None):
        '''This function take a Two-Line Element and converts its elements into a Pandas DataFrame.'''
        satellite_number, classification, international_designator_year, international_designator_launch_number,international_designator_piece_of_launch,element_set_number = self.tle_sat_identity_elements(tle)
        title, inclination, right_ascension, eccentricity, argument_periapsis, mean_anomaly, mean_motion, epoch_date = self.tle_keplerian_elements(tle)
        revolution = self.revolution(tle)
        bstar_drag_term = self.bstar_drag_term(tle)
        second_time_derivative_of_mean_motion_divided_by_six = self.second_time_derivative_of_mean_motion_divided_by_six(tle)
        first_derivative_mean_motion_divided_by_two = self.first_derivative_mean_motion_divided_by_two(tle)
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
            'second_time_derivative_of_mean_motion_divided_by_six': second_time_derivative_of_mean_motion_divided_by_six,
            'first_derivative_mean_motion_divided_by_two': first_derivative_mean_motion_divided_by_two
        }
        df = pd.DataFrame(sat_elements,index=[0])
        return df
