
def parse_tle(tle):
    '''Parses a Two line Element (TLE) set into a title and the two individual lines.'''
    title, line1, line2 = map(lambda x: x.strip(), tle.split('\n'))
    return title, line1, line2

def tle_checksum_algortithm(line):
    '''This function defines the (mod 10) checksum algorithm used to determine validity on TLE sets.'''
    line = line.replace('-','1').replace(' ','0').replace('+','0')
    ind_val = lambda x: x >= '0' and x <= '9'
    chksum = sum(int(ind_val(line)))
    mod10_chksum = chksum % 10
    return mod10_chksum

def validation_framework(condition1, condition2, expected1, expected2,dual_condition=True):

    if dual_condition is True:
        if str(condition1) == str(expected1) and str(condition2) == str(expected2):
            return True
        else:
            break
    else:
        if str(condition1) == str(conditition2):
            return True
        else:
            break

def check_valid_tle(tle):
    '''This function validates the tle by checking that several tle elements are valid.'''
    title, line1, line2 =  parse_tle(tle)

    line_index = validation_framework(line1[0],line2[0],'1','2')
    sat_num = validation_framework(line1[2:7],line2[2:7],dual_condition=False)
    checksum_check = validation_framework(line1[-1],line2[-1],tle_checksum_algortithm(line1), tle_checksum_algortithm(line2))

    if line_index and sat_num and checksum_check is True:
        return True
    else:
        break

def scientific_notation_conversion(val):
    '''Specific format is X digits, a + or -, and 1 digit, ex: 01234-5 which is 0.01234e-5'''
    split = val.str.split('-')
    X_digits = split.str.get(0)
    multiplier = 0.1**int(len(X_digits))
    exp = split.str.get(1)
    base = multiplier*float(value[int(len(int_base))])
    exponent = 10**int(value[int(exponent):])
    return base * exponent

def tle_satellite_elements(tle, print_info=False):
    '''This function parses and returns the TLE elements as individual components.'''

    title, line1, line2 =  parse_tle(tle)

    if check_valid_tle(tle) is True:

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
        first_time_derivative_of_the_mean_motion_divided_by_two = float(line1[33:43])
        second_time_derivative_of_mean_motion_divided_by_six = scientific_notation_conversion(line1[44:52])
        bstar_drag_term = scientific_notation_conversion(line1[53:61])
    else:
        assert check_valid_tle(tle) is True, "Your TLE data doesn't apppear to be correct, check the data and try again."

    if print_info is True:
        print("----------------------------------------------------------------------------------------")
        print(tle)
        print("----------------------------------------------------------------------------------------")
        print("Satellite Name                                            = {}s").format(title)
        print("Satellite Number                                          = {}g ({}s)").format(satellite_number, "Unclassified" if classification == 'U' else "Classified")
        print("International Designator                                  = YR: %02d, LAUNCH #%d, PIECE: %s").format(international_designator_year, international_designator_launch_number, international_designator_piece_of_launch)
        print("Epoch Date                                                = {}s (YR:{} DAY:{})").format(epoch_date.strftime("%Y-%m-%d %H:%M:%S.%f %Z"), epoch_year, epoch)
        print("First Time Derivative of the Mean Motion divided by two   = {}g").format(first_time_derivative_of_the_mean_motion_divided_by_two)
        print("Second Time Derivative of Mean Motion divided by six      = {}g").format(second_time_derivative_of_mean_motion_divided_by_six)
        print("BSTAR drag term                                           = {}g").format(bstar_drag_term)
        print("Element number                                            = {}g").format(element_number)
        print("----------------------------------------------------------------------------------------")
    else:
        pass

    return


def tle_ballistic_elements(tle):
    '''This function parses and returns the TLE elements as individual components.'''

    title, line1, line2 =  parse_tle(tle)

    if check_valid_tle(tle) is True:


        mean_motion = float(line2[52:63])
        revolution = float(line2[63:68])

def tle_keplerian_elements(tle):
    '''This function parses and returns the TLE elements as individual components.'''

    title, line1, line2 =  parse_tle(tle)

    if check_valid_tle(tle) is True:

        #Line 2
        inclination = float(line2[8:16])
        right_ascension = float(line2[17:25])
        eccentricity = scientific_notation_conversion(line2[26:33])
        argument_periapsis = float(line2[34:42])
        mean_anomaly = float(line2[43:51])

        return

    else:
        pass













        print "Inclination [Degrees]                                     = %g°" % inclination
        print "Right Ascension of the Ascending Node [Degrees]           = %g°" % right_ascension
        print "Eccentricity                                              = %g" % eccentricity
        print "Argument of Perigee [Degrees]                             = %g°" % argument_perigee
        print "Mean Anomaly [Degrees] Anomaly                            = %g°" % mean_anomaly
        print "Eccentric Anomaly                                         = %g°" % eccentric_anomaly
        print "True Anomaly                                              = %g°" % true_anomaly
        print "Mean Motion [Revs per day] Motion                         = %g" % mean_motion
        print "Period                                                    = %s" % timedelta(seconds=period)
        print "Revolution number at epoch [Revs]                         = %g" % revolution

        print
        print "semi_major_axis = %gkm" % semi_major_axis
        print "eccentricity    = %g" % eccentricity
        print "inclination     = %g°" % inclination
        print "arg_perigee     = %g°" % argument_perigee
        print "right_ascension = %g°" % right_ascension
        print "true_anomaly    = %g°" % true_anomaly
        print "----------------------------------------------------------------------------------------"

    if labels:
        graphics.plotOrbit(semi_major_axis, eccentricity, inclination,
                           right_ascension, argument_perigee, true_anomaly, title)
    else:
        graphics.plotOrbit(semi_major_axis, eccentricity, inclination,
                           right_ascension, argument_perigee, true_anomaly)
