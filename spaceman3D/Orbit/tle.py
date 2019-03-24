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
        '''This function takes the tle format of floats (01234-5) a + or -, and converts them into 1.234e-08'''
        split = val.split('-')
        #Handles Negative Values
        if len(split) > 2:
            X_digits = "-" + split[1]
            exp = "-"+split[2]
        else:
            X_digits = "-"+split[0]
            exp = split[1]
        multiplier = 0.1**int(len(X_digits))
        base = multiplier*int(X_digits)
        exponent = 10**int(exp)
        return base * exponent

    def decimal_conversion(self,val):
        value = float(f'{val[0]}.{val[1:]}')
        return value

    def individual_element(self,tle,line,start,end,func=None):
        '''This function is the template to parse the individual elements.'''
        title, line1, line2 =  self.parse_tle(tle)
        if self.check_valid_tle(tle) is True:
            if line == 1:
                line = line1
            elif line == 2:
                line = line2
            else:
                pass

            if func is not None:
                var = func(line[start:end])
            else:
                var = line[start:end]
            return var
        else:
            assert self.check_valid_tle(tle) is True, "Your TLE data doesn't apppear to be correct, check the data and try again."

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

    def tle_keplerian_elements(self,tle):
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

#################### Parsing the individual TLE components ####################
    def first_derivative_mean_motion_divided_by_two(self,tle):
        '''This function parses and returns the first derivative mean motion from the TLE element.'''
        first_time_derivative_of_the_mean_motion_divided_by_two = self.individual_element(tle,1,33,43,func=float)
        return first_time_derivative_of_the_mean_motion_divided_by_two

    def second_time_derivative_of_mean_motion_divided_by_six(self,tle):
        '''This function parses and returns the second derivative of mean motion from the TLE element'''
        second_time_derivative_of_mean_motion_divided_by_six = self.individual_element(tle,1,44,52,func=self.scientific_notation_conversion)
        return second_time_derivative_of_mean_motion_divided_by_six

    def bstar_drag_term(self,tle):
        '''This function parses and returns the Bstar drag term from the TLE element'''
        bstar_drag_term = self.individual_element(tle,1,53,61,func=self.scientific_notation_conversion)
        return bstar_drag_term

    def satellite_number(self,tle):
        '''This function parses and returns the satellite number from the TLE element'''
        satellite_number = self.individual_element(tle,1,2,8,func=str)
        classification = satellite_number[-1:]
        satellite_number = int(satellite_number)
        return satellite_number,classification

    def international_designator_year(self,tle):
        '''This function parses and returns the international designator year from the TLE element'''
        international_designator_year = self.individual_element(tle,1,9,11,func=int)
        return international_designator_year

    def international_designator_launch_number(self,tle):
        '''This function parses and returns the international designator launch number from the TLE element'''
        international_designator_launch_number  = self.individual_element(tle,1,11,14,func=int)
        return international_designator_launch_number

    def international_designator_piece_of_launch(self,tle):
        '''This function parses and returns the international designator launch number from the TLE element'''
        international_designator_piece_of_launch  = self.individual_element(tle,1,14,17,func=str)
        return international_designator_piece_of_launch

    def element_number(self,tle):
        '''This function parses and returns the element number from the TLE element'''
        element_number = self.individual_element(tle,1,64,68,func=float)
        return element_number

    def epoch_year(self,tle,full_year=False):
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

    def epoch(self,tle):
        '''This function parses and returns the epoch (days) from the TLE element'''
        epoch = self.individual_element(tle,1,20,32,func=float)
        return epoch

    def epoch_date(self,tle):
        '''This function parses and returns the epoch date from the TLE element'''
        epoch = self.epoch(tle)
        year = self.epoch_year(tle,full_year=True)
        epoch_date = datetime(year=year, month=1, day=1, tzinfo=tz.utc) + timedelta(days=epoch-1)
        return epoch_date

    def inclination(self,tle):
        '''This function parses and returns the inclination of the satellite from the TLE element'''
        inclination = self.individual_element(tle,2,8,16,func=float)
        return inclination

    def right_ascension(self,tle):
        '''This function parses and returns the right_ascension of the satellites orbit from the TLE element'''
        right_ascension = self.individual_element(tle,2,17,25,func=float)
        return right_ascension

    def eccentricity(self,tle):
        '''This function parses and returns the eccentricity of the satellites orbit from the TLE element'''
        eccentricity = self.individual_element(tle,2,26,33,func=self.decimal_conversion)
        return eccentricity

    def argument_periapsis(self,tle):
        '''This function parses and returns the argument of periapsis of the satellites orbit from the TLE element'''
        argument_periapsis = self.individual_element(tle,2,34,42,func=float)
        return argument_periapsis

    def mean_anomaly(self,tle):
        '''This function parses and returns the mean anomaly of the satellites orbit from the TLE element'''
        mean_anomaly = self.individual_element(tle,2,43,51,func=float)
        return mean_anomaly

    def mean_motion(self,tle):
        '''This function parses and returns the mean motion of the satellites orbit from the TLE element'''
        mean_motion = self.individual_element(tle,2,52,63,func=float)
        return mean_motion

    def revolution(self,tle):
        '''This function parses and returns the satellites revolution from the TLE element'''
        revolution = self.individual_element(tle,2,63,68,func=float)
        return revolution
