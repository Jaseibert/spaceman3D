from datetime import datetime, timedelta
import pytz as tz

class tle(object):

    def __init__(self):
        return

    def parse_tle(self,tle):
        '''Parses a Two line Element (TLE) set into a title and the two individual lines.'''
        title, line1, line2 = map(lambda x: x.strip(), tle.split('\n'))
        return title, line1, line2

    def tle_checksum_algortithm(self,line):
        '''This function defines the modulo 10 checksum algorithm used to determine validity on TLE sets.'''
        line = line.replace('-','1')
        ind_val = [int(d) for d in line if d.isdigit()]
        del ind_val[-1]
        mod10_chksum = sum(ind_val) % 10
        return mod10_chksum

    def validation_framework(self,condition1, condition2, expected1=None, expected2=None,dual_condition=True):
        '''This function defines two conditional tests that will be used to check the TLE data'''
        if dual_condition is True:
            if str(condition1) == str(expected1) and str(condition2) == str(expected2):
                return True
            else:
                return False
        else:
            if str(condition1) == str(condition2):
                return True
            else:
                return False

    def check_valid_tle(self,tle):
        '''This function validates the tle by checking that several tle elements are valid.'''
        title, line1, line2 =  self.parse_tle(tle)
        line_index = self.validation_framework(line1[0],line2[0],'1','2')
        sat_num = self.validation_framework(line1[2:7],line2[2:7],dual_condition=False)
        checksum_check = self.validation_framework(line1[-1],line2[-1],self.tle_checksum_algortithm(line1), self.tle_checksum_algortithm(line2))
        if line_index and sat_num and checksum_check is True:
            return True
        else:
            return False

    def scientific_notation_conversion(self,val):
        '''This function takes the tle format of floats (01234-5) a + or -, and converts them into 1234.000000..5'''
        split = val.split('-')
        #Handles Negative Values
        if len(split) > 2:
            X_digits = split[0] + split[1]
            exp = split[2]
        else:
            X_digits = split[0]
            exp = split[1]
        multiplier = 0.1**int(len(X_digits))
        base = multiplier*int(X_digits)
        exponent = 10**int(exp)
        return base * exponent

    def decimal_conversion(self,val):
        value = float(f'{val[0]}.{val[1:]}')
        return value

    def tle_satellite_elements(self,tle, print_info=False):
        '''This function parses and returns the satellite's basic TLE elements as individual components.'''
        title, line1, line2 =  self.parse_tle(tle)
        if self.check_valid_tle(tle) is True:

            satellite_number = int(line1[2:7])
            classification = line1[7:8]
            international_designator_year = int(line1[9:11])
            international_designator_launch_number = int(line1[11:14])
            international_designator_piece_of_launch = line1[14:17]
            element_number = float(line1[64:68])
            epoch_year = int(line1[18:20])
            year = (
                2000 + epoch_year
                if epoch_year < 70
                else 1900 + epoch_year)
            epoch = float(line1[20:32])
            epoch_date = datetime(year=year, month=1, day=1, tzinfo=tz.utc) + timedelta(days=epoch-1)
        else:
            assert self.check_valid_tle(tle) is True, "Your TLE data doesn't apppear to be correct, check the data and try again."

        if print_info is True:
            print("----------------------------------------------------------------------------------------")
            print(tle)
            print("----------------------------------------------------------------------------------------")
            print("Satellite Name                                              {}".format(title))
            print("Satellite Number                                            {} ({})".format(satellite_number, "Unclassified" if classification == 'U' else "Classified"))
            print("International Designator                                    YR:{}, LAUNCH #:{}, PIECE: {}".format(international_designator_year, international_designator_launch_number, international_designator_piece_of_launch))
            print("Epoch Date                                                  {} (YR:{} DAY:{})".format(epoch_date.strftime("%Y-%m-%d %H:%M:%S.%f %Z"), year, epoch))
            print("Element number                                              {}".format(element_number))
            print("----------------------------------------------------------------------------------------")
        else:
            pass
        return title, satellite_number, classification, international_designator_year, international_designator_launch_number,
        international_designator_piece_of_launch, element_number, epoch_year, year, epoch, epoch_date


    def tle_ballistic_elements(self,tle, print_info=False):
        '''This function parses and returns the ballistic TLE elements as individual components.'''
        title, line1, line2 =  self.parse_tle(tle)
        if self.check_valid_tle(tle) is True:
            revolution = float(line2[63:68])
            first_time_derivative_of_the_mean_motion_divided_by_two = float(line1[33:43])
            second_time_derivative_of_mean_motion_divided_by_six = self.scientific_notation_conversion(line1[44:52])
            bstar_drag_term = self.scientific_notation_conversion(line1[53:61])
        else:
            assert self.check_valid_tle(tle) is True, "Your TLE data doesn't apppear to be correct, check the data and try again."

        if print_info is True:
            print("----------------------------------------------------------------------------------------")
            print(tle)
            print("----------------------------------------------------------------------------------------")
            print("Revolution number at epoch [Revs]                           {}".format(revolution))
            print("First Time Derivative of the Mean Motion divided by two     {}".format(first_time_derivative_of_the_mean_motion_divided_by_two))
            print("Second Time Derivative of Mean Motion divided by six        {}".format(second_time_derivative_of_mean_motion_divided_by_six))
            print("BSTAR drag term                                             {}".format(bstar_drag_term))
            print("----------------------------------------------------------------------------------------")
        else:
            pass
        return title, revolution, first_time_derivative_of_the_mean_motion_divided_by_two,
        second_time_derivative_of_mean_motion_divided_by_six, bstar_drag_term


    def tle_keplerian_elements(self,tle, print_info=False):
        '''This function parses and returns the TLE elements as individual components.'''
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
        else:
            assert self.check_valid_tle(tle) is True, "Your TLE data doesn't apppear to be correct, check the data and try again."
        return title, inclination, right_ascension, eccentricity, argument_periapsis, mean_anomaly, mean_motion, epoch_date
