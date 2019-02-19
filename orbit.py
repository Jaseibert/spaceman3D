import numpy as np
from datetime import datetime, timedelta
import pendulum as p
import graphics
import urllib

class Orbit(object):

    def __init__():
        return

    tz = p.timezone('America/Chicago')

    # Standard Gravitational parameter in km^3 / s^2 of Earth
    GM = 398600.4418

    def eccentric_anomoly_calculation(mean_anomaly, eccentricity, initial, max_iterations=500, max_accuracy=0.0001):
        """Approximates Eccentric Anomaly from Mean Anomaly All input and outputs are in radians"""

        #mean_anomaly = mean_anomaly
        #e0 = initValue
        for i in range(max_iterations):
            eccentric_anomaly = initial - (initial - eccentricity * np.sin(initial) - mean_anomaly) / (1.0 - eccentricity * np.cos(initial))
            if (np.abs(eccentric_anomaly-initial) > maxAccuracy):
                return eccentric_anomaly
            else:
                break

    "Create Function "

    # Time difference of now from epoch, offset in radians
    diff = datetime.now().replace(tzinfo=tz.utc) + timedelta(hours=8) - epoch_date # Offset for PDT
    diff_seconds = 24*60*60*diff.days + diff.seconds + 1e-6*diff.microseconds # sec
    print("Time offset: {}s").format(diff)

    motion_per_sec = mean_motion * 2*np.pi / (24*60*60) # rad/sec
    print("Radians per second: {}g").format(motion_per_sec)

    offset = diff_seconds * motion_per_sec #rad
    print("Offset to apply: %g").format(offset)

    mean_anomaly += offset * 180/np.pi % 360




    "Create a Function to Calculate other Keplerian Elements"

    # Inferred period
    day_seconds = 24*60*60
    period = day_seconds * 1/mean_motion

    # Inferred semi-major axis (in km)
    semi_major_axis = ((period/(2*np.pi))**2 * GM)**(1/3)

    # Inferred true anomaly
    eccentric_anomaly = eccentric_anomoly_calculation(mean_anomaly * np.pi/180, eccentricity, mean_anomaly * np.pi/180)
    true_anomaly = 2*np.arctan2(np.sqrt(1+eccentricity) * np.sin(eccentric_anomaly/2.0), np.sqrt(1-eccentricity) * np.cos(eccentric_anomaly/2.0))

    # Convert to degrees
    eccentric_anomaly *= 180/np.pi
    true_anomaly *= 180/np.pi


    # elem1 = """ISS (ZARYA)
    # 1 25544U 98067A   08264.51782528 -.00002182  00000-0 -11606-4 0  2927
    # 2 25544  51.6416 247.4627 0006703 130.5360 325.0288 15.72125391563537"""

    # dragon = """DRAGON CRS-2
    # 1 39115U 13010A   13062.62492353  .00008823  00000-0  14845-3 0   188
    # 2 39115  51.6441 272.5899 0012056 334.2535  68.5574 15.52501943   306"""

    graphics.plot_earth()

    # Data from NORAD http://www.celestrak.com/NORAD/elements/
    # filename = "noaa.txt" # NOAA satellites
    # filename = "geo.txt" # Geostationary satellites
    # filename = "gps-ops.txt" # GPS sats
    # filename = "military.txt" # Some military satellites
    # filename = "stations.txt" # Space stations
    # filename = "visual.txt" # 100 brightest or so objects

    # files = ["noaa.txt", "stations.txt", "military.txt", "gps-ops.txt"]
    # files = ["stations.txt"]

    names = ["stations"]

    for urlname in names:
        f = urllib.urlopen("http://www.celestrak.com/NORAD/elements/%s.txt" % urlname)
        elem = ""
        for line in f:
            elem += line
            if (line[0] == '2'):
                elem = elem.strip()
                if elem.startswith("ISS"):
                    pretty_print(elem, printInfo=True, labels=True)
                elem = ""

    # pretty_print(elem1)
    # pretty_print(dragon)

    graphics.doDraw()

    # EOF
