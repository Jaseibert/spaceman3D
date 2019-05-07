import numpy as np
from datetime import datetime, timedelta
import pytz as tz
import urllib
import spaceman3D.Orbit.tle as t

class Orbit(object):

    def __init__(self,title='',right_ascension=0,eccentricity=0,argument_periapsis=0,mean_anomaly=0,mean_motion=0,epoch_date=0):
        self.title = title
        self.right_ascension = right_ascension
        self.eccentricity = eccentricity
        self.argument_periapsis = argument_periapsis
        self.mean_anomaly = mean_anomaly
        self.mean_motion = mean_motion
        self.epoch_date = epoch_date
        return

    def import_tle(self, tle=None):
        '''This function uses TLE element information to populate the relavant instance variables.

        :param tle: a Two-Line Element (TLE).
        :type tle: String
        :return: Nothing.
        '''
        TLE = t.tle()
        self.title, self.inclination, self.right_ascension, self.eccentricity, self.argument_periapsis, self.mean_anomaly, self.mean_motion, self.epoch_date = TLE.tle_keplerian_elements(tle=tle)
        return

    def radian_to_degree(self, value):
        '''This function converts radians to degrees.

        :param value: the radian to be converted.
        :type value: float
        :return: the degree (float)
        '''
        radian = value * 180/np.pi
        return radian

    def degree_to_radian(self, value):
        '''This function converts degrees to radians.

        :param value: the degree to be converted.
        :type value: float
        :return: the radian (float)
        '''
        degree = value * np.pi/180
        return degree

    def eccentric_anomoly_calculation(self, mean_anomaly, eccentricity, max_iterations=500, max_accuracy=0.0001):
        '''Approximates Eccentric Anomaly from Mean Anomaly (input and outputs are in radians).

        :param mean_anomaly: the mean anomaly (radians)
        :type mean_anomaly: float
        :param eccentricity: the eccentricity.
        :type eccentricity: float
        :param value: the degree to be converted.
        :type value: float
        :param value: the degree to be converted.
        :type value: float
        :param value: the degree to be converted.
        :type value: float
        :return: the radian (float)
        '''

        if mean_anomaly >= 0.8:
            initial = np.pi
        else:
            initial = mean_anomaly

        for i in range(max_iterations):
            eccentric_anomaly = initial - (initial - eccentricity * np.sin(initial) - mean_anomaly) / (1.0 - eccentricity * np.cos(initial))
            if (np.abs(eccentric_anomaly-initial) > max_accuracy):
                return eccentric_anomaly
            else:
                break

    def epoch_time_diff(self):
        '''This function calculates the time difference from now until the epoch.'''
        diff = datetime.now().replace(tzinfo=tz.utc) + timedelta(hours=6) - self.epoch_date
        diff_seconds = 24*60*60*diff.days + diff.seconds + 1e-6*diff.microseconds
        return diff_seconds

    def motion_radian_per_second(self):
        '''This function calculates the motion per second (radians/sec) of an object using the mean motion.'''
        motion_per_sec = self.mean_motion * 2*np.pi / (24*60*60)
        return motion_per_sec

    def time_adjusted_mean_anomaly_calc(self):
        '''This function calculates the offset(in Radians) from the time differece from now until the epoch into Degrees.'''
        #Calls the epoch_time_diff() and motion_per_sec()
        diff_seconds = self.epoch_time_diff()
        motion_per_sec = self.motion_radian_per_second()
        adjusted_mean_anomaly = self.degree_to_radian(diff_seconds*motion_per_sec)
        self.mean_anomaly += adjusted_mean_anomaly % 360
        return self.mean_anomaly

    def period_calc(self):
        '''This function infers the period from the TLE mean motion.'''
        day_seconds = 24*60*60
        period = day_seconds * 1/self.mean_motion
        return period

    def semi_major_axis_calc(self, GM='Earth'):
        '''This function calculates the semi major axis.
        :param standard_gravitational_parameter: the Standard Gravitational Parameter for the orbital body
        :return: the Semi-Major Axis
        '''
        GM = 398600.4418
        period = self.period_calc()
        motion_per_sec = self.motion_radian_per_second()
        semi_major_axis = (GM**(1/3))/((motion_per_sec)**(2/3))
        return semi_major_axis

    def anomoly_calc(self):
        '''This function calculates the true and eccentric anomalies.'''
        self.mean_anomaly = self.radian_to_degree(self.time_adjusted_mean_anomaly_calc())
        eccentric_anomaly = self.eccentric_anomoly_calculation(self.eccentricity, self.mean_anomaly)
        true_anomaly = 2*np.arctan2(np.sqrt(1+self.eccentricity) * np.sin(eccentric_anomaly/2.0), np.sqrt(1-self.eccentricity) * np.cos(eccentric_anomaly/2.0))
        true_anomaly = self.radian_to_degree(true_anomaly)
        return true_anomaly
