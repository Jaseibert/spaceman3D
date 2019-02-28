import numpy as np
from datetime import datetime, timedelta
import pytz as tz
import urllib
import spaceman.Orbit.tle as t

class Orbit(object):

    def __init__(self):
        return

    elem1 = """ISS (ZARYA)
    1 25544U 98067A   19054.54477108  .00016717  00000-0  10270-3 0  9035
    2 25544  51.6375 206.2871 0005712  59.5442 300.6274 15.53254633 37592"""


    TLE = t.tle()
    title, inclination, right_ascension, eccentricity, argument_periapsis, mean_anomaly, mean_motion = TLE.tle_keplerian_elements(tle=elem1)
    epoch_date = TLE.tle_satellite_time_elements(tle=elem1)

    def radian_to_degree(self,val):
        val_rad = val * 180/np.pi
        return val_rad

    def degree_to_radian(self,val):
        val_deg = val * np.pi/180
        return val_deg

    def eccentric_anomoly_calculation(self, mean_anomaly, eccentricity, max_iterations=500, max_accuracy=0.0001):
        """Approximates Eccentric Anomaly from Mean Anomaly All input and outputs are in radians"""

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
        # Why Radians -> Mod 360
        adjusted_mean_anomaly = self.degree_to_radian(diff_seconds*motion_per_sec)
        self.mean_anomaly += adjusted_mean_anomaly % 360
        return self.mean_anomaly

    def period_calc(self):
        '''This function infers the period from the TLE mean motion.'''
        day_seconds = 24*60*60
        period = day_seconds * 1/self.mean_motion
        return period

    def semi_major_axis_calc(self):
        '''This function calculates the semi major axis.'''
        period = self.period_calc()
        motion_per_sec = self.motion_radian_per_second()
        GM = 398600.4418
        semi_major_axis = (GM**(1/3))/((motion_per_sec)**(2/3))
        return semi_major_axis

    def anomoly_calc(self):
        '''This function calculates the true and eccentric anomalies.'''
        #self.mean_anomaly =
        self.mean_anomaly = self.radian_to_degree(self.time_adjusted_mean_anomaly_calc())
        eccentric_anomaly = self.eccentric_anomoly_calculation(self.eccentricity, self.mean_anomaly)
        true_anomaly = 2*np.arctan2(np.sqrt(1+self.eccentricity) * np.sin(eccentric_anomaly/2.0), np.sqrt(1-self.eccentricity) * np.cos(eccentric_anomaly/2.0))
        eccentric_anomaly *= 180/np.pi
        true_anomaly *= 180/np.pi
        return true_anomaly
