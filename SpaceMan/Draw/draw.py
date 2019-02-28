from __future__ import division
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import spaceman.Orbit.orbit as o

class Draw(object):

    def __init__(self):
        return

    fig = plt.figure(figsize=plt.figaspect(1))
    ax = fig.add_subplot(111, projection='3d', aspect=1)
    max_radius = 0

    def plot_earth(self):
        "Draw Earth as a globe at the origin"

        Earth_radius = 6371
        self.max_radius = max(self.max_radius, Earth_radius)

        # Coefficients in a0/c x**2 + a1/c y**2 + a2/c z**2 = 1
        coefs = (1, 1, 1)

        # Radii corresponding to he coefficients:
        rx, ry, rz = [Earth_radius/np.sqrt(coef) for coef in coefs]

        # Azimuth Angle & Altitude in Spherical Coordinates
        phi = np.linspace(0, 2*np.pi, 100)
        theta = np.linspace(0, np.pi, 100)

        # Spherical Angles: X = r * cos(ϕ)sin(θ), Y = r * cos(ϕ)sin(θ), Z = r * cos(θ)
        x = rx * np.outer(np.cos(phi), np.sin(theta))
        y = ry * np.outer(np.sin(phi), np.sin(theta))
        z = rz * np.outer(np.ones_like(phi), np.cos(theta))
        #z = rz *  np.cos(theta)
        return x,y,z

    def plot_orbit(self,semi_major_axis, eccentricity=0, inclination=0, right_ascension=0, argument_perigee=0, true_anomaly=0, label=None):
        "Draws orbit around an earth in units of kilometers."

        orb = o.Orbit()

        # Rotation matrix for inclination
        inc = orb.degree_to_radian(inclination)
        R = np.matrix([[1, 0, 0],
                       [0, np.cos(inc), -np.sin(inc)],
                       [0, np.sin(inc), np.cos(inc)]    ])

        # Rotation matrix for argument of perigee + right ascension
        rot = orb.degree_to_radian(right_ascension + argument_perigee)
        R2 = np.matrix([[np.cos(rot), -np.sin(rot), 0],
                        [np.sin(rot), np.cos(rot), 0],
                        [0, 0, 1]   ])

        ### Draw orbit
        theta = np.linspace(0,2*np.pi, 360)
        r = (semi_major_axis * (1-eccentricity**2)) / (1 + eccentricity*np.cos(theta))

        xr = r*np.cos(theta)
        yr = r*np.sin(theta)
        zr = 0 * theta

        pts = np.matrix(list(zip(xr,yr,zr)))

        # Rotate by inclination, & Ascension + Perigee
        pts =  (R * R2 * pts.T).T

        # Turn back into 1d vectors
        xr,yr,zr = pts[:,0].A.flatten(), pts[:,1].A.flatten(), pts[:,2].A.flatten()

        # Plot the orbit
        self.ax.plot(xr, yr, zr, '-')

        # Plot the satellite
        sat_angle = orb.degree_to_radian(true_anomaly)
        satr = (semi_major_axis * (1-eccentricity**2)) / (1 + eccentricity*np.cos(sat_angle))
        satx = satr * np.cos(sat_angle)
        saty = satr * np.sin(sat_angle)
        satz = 0

        sat = (R * R2 * np.matrix([satx, saty, satz]).T).flatten()
        satx = sat[0,0]
        saty = sat[0,1]
        satz = sat[0,2]

        c = np.sqrt(satx*satx + saty*saty)
        lat = np.arctan2(satz, c) * 180/np.pi
        lon = np.arctan2(saty, satx) * 180/np.pi
        print("----------------------------------------------------------------------------------------")
        print("{} : Projected Lat: {}° Long: {}°".format(label, lat, lon))

        # Draw radius vector from earth
        self.ax.plot([0, satx], [0, saty], [0, satz], 'r-')

        x,y,z = self.plot_earth()
        self.ax.plot_surface(x, y, z,  rstride=4, cstride=4, alpha=0.4, color='g')

        # Draw red sphere for satellite
        self.ax.plot([satx],[saty],[satz], 'ro')
        ax.w_xaxis.set_pane_color((0.5, 0.5, 0.5, 1.0))
        ax.w_yaxis.set_pane_color((0.5, 0.5, 0.5, 1.0))
        ax.w_zaxis.set_pane_color((0.5, 0.5, 0.5, 1.0))
        #ax.view_init(, 35)

        # Write satellite name next to it
        if label is not None:
            self.ax.text(satx, saty, satz, label, fontsize=12)

    def draw(self):
        '''This function calls the plot orbit function using the TLE elements defined in orbit.py'''
        orb = o.Orbit()
        inclination = orb.inclination
        eccentricity = orb.eccentricity
        right_ascension = orb.right_ascension
        argument_periapsis = orb.argument_periapsis
        title = orb.title
        semi_major_axis = orb.semi_major_axis_calc()
        true_anomaly = orb.anomoly_calc()
        self.plot_orbit(semi_major_axis,eccentricity,inclination,right_ascension,argument_periapsis,true_anomaly,title)

        #Print Keplerian (Orbital) Elements
        print("----------------------------------------------------------------------------------------")
        print("----------------------------------------------------------------------------------------")
        print("Semi Major Axis [kilometers]                                {}".format(semi_major_axis))
        print("Inclination [Degrees]                                       {}°".format(inclination))
        print("Right Ascension of the Ascending Node [Degrees]             {}°".format(right_ascension))
        print("Eccentricity                                                {}".format(eccentricity))
        print("Argument of Periapsis [Degrees]                             {}°".format(argument_periapsis))
        print("True Anomaly [Degrees]                                      {}°".format(true_anomaly))
        print("----------------------------------------------------------------------------------------")

        for axis in 'xyz':
            getattr(self.ax, 'set_{}lim'.format(axis))((-self.max_radius, self.max_radius))
        # Draw figure
        plt.show()
