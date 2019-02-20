import numpy as np
from datetime import datetime, timedelta
import pendulum as p
import urllib
import SpaceMan.tle as t
import SpaceMan.draw as d

class orbit(object):

    def __init__():
        return

    tz = p.timezone('America/Chicago')

    # Standard Gravitational parameter in km^3 / s^2 of Earth
    GM = 398600.4418

    elem1 = """ISS (ZARYA)
    1 25544U 98067A   08264.51782528 -.00002182  00000-0 -11606-4 0  2927
    2 25544  51.6416 247.4627 0006703 130.5360 325.0288 15.72125391563537"""

    title, inclination, right_ascension, eccentricity, argument_periapsis, mean_anomaly = t.tle_keplerian_elements(elem1)

    def eccentric_anomoly_calculation(self, mean_anomaly, eccentricity, initial, max_iterations=500, max_accuracy=0.0001):
        """Approximates Eccentric Anomaly from Mean Anomaly All input and outputs are in radians"""

        #mean_anomaly = mean_anomaly
        #e0 = initValue
        for i in range(max_iterations):
            eccentric_anomaly = initial - (initial - eccentricity * np.sin(initial) - mean_anomaly) / (1.0 - eccentricity * np.cos(initial))
            if (np.abs(eccentric_anomaly-initial) > maxAccuracy):
                return eccentric_anomaly
            else:
                break

    def epoch_time_diff(self):
        '''This function calculates the time difference from now until the epoch.'''
        diff = datetime.now().replace(tzinfo=tz.utc) + timedelta(hours=8) - epoch_date # Offset for PDT
        diff_seconds = 24*60*60*diff.days + diff.seconds + 1e-6*diff.microseconds # sec
        print("Time offset: {}s").format(diff)
        return diff_seconds

    def motion_per_second(self):
        '''This function calculates the motion per second of an object using the mean motion.'''
        motion_per_sec = mean_motion * 2*np.pi / (24*60*60) # rad/sec
        print("Radians per second: {}g").format(motion_per_sec)
        return motion_per_sec

    def mean_anomaly_calc(self):
        '''This function calculates the offset from the time differece from now until the epoch into radians.'''
        diff_seconds = self.epoch_time_diff()
        motion_per_sec = self.motion_per_second()
        offset = diff_seconds * motion_per_sec #rad
        print("Offset to apply: %g").format(offset)
        mean_anomaly += offset * 180/np.pi % 360
        return mean_anomaly

    def period_calc(self):
        '''This function infers the period from the TLE mean motion.'''
        day_seconds = 24*60*60
        period = day_seconds * 1/mean_motion
        return period

    def semi_major_axis_calc(self):
        '''This function calculates the semi major axis.'''
        period = self.period_calc()
        semi_major_axis = ((period/(2*np.pi))**2 * GM)**(1/3)
        return semi_major_axis

    def anomoly_calc(self):
        '''This function calculates the true and eccentric anomalies.'''
        mean_anomaly = self.mean_anomaly_calc()
        # Inferred true anomaly
        eccentric_anomaly = eccentric_anomoly_calculation(mean_anomaly * np.pi/180, eccentricity, mean_anomaly * np.pi/180)
        true_anomaly = 2*np.arctan2(np.sqrt(1+eccentricity) * np.sin(eccentric_anomaly/2.0), np.sqrt(1-eccentricity) * np.cos(eccentric_anomaly/2.0))
        eccentric_anomaly *= 180/np.pi
        true_anomaly *= 180/np.pi
        return eccentric_anomaly, true_anomaly
