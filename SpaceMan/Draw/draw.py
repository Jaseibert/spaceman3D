import matplotlib.pyplot as plt
plt.style.use('dark_background')
from mpl_toolkits.mplot3d import Axes3D
from mpltools import layout
import numpy as np
from spaceman.Orbit import Orbit
import spaceman.Orbit.satellites as s

class Draw(object):

    def __init__(self):
        return

    fig = plt.figure(figsize=layout.figaspect(1))
    ax = fig.add_subplot(111, projection='3d', aspect=1)

    def plot_earth(self):
        "Draw Earth as a globe at the origin"

        Earth_radius = 6371
        coefs = (1, 1, 1)
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

    def plot_orbit(self,semi_major_axis=0, eccentricity=0, inclination=0, right_ascension=0, argument_perigee=0, true_anomaly=0, label=None):
        "Draws orbit around an earth in units of kilometers."

        o = Orbit()
        # Rotation matrix for inclination
        inc = o.degree_to_radian(inclination)
        R = np.matrix([[1, 0, 0],
                       [0, np.cos(inc), -np.sin(inc)],
                       [0, np.sin(inc), np.cos(inc)]])

        # Rotation matrix for argument of perigee + right ascension
        rot = o.degree_to_radian(right_ascension + argument_perigee)
        R2 = np.matrix([[np.cos(rot), -np.sin(rot), 0],
                        [np.sin(rot), np.cos(rot), 0],
                        [0, 0, 1]])

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
        sat_angle = o.degree_to_radian(true_anomaly)
        satr = (semi_major_axis * (1-eccentricity**2)) / (1 + eccentricity*np.cos(sat_angle))
        satx = satr * np.cos(sat_angle)
        saty = satr * np.sin(sat_angle)
        satz = 0

        sat = (R * R2 * np.matrix([satx, saty, satz]).T).flatten()
        satx = sat[0,0]
        saty = sat[0,1]
        satz = sat[0,2]

        c = np.sqrt(satx*satx + saty*saty)
        lat = o.degree_to_radian(np.arctan2(satz, c))
        lon = o.degree_to_radian(np.arctan2(saty, satx))
        print("----------------------------------------------------------------------------------------")
        print("{} : Projected Lat: {}° Long: {}°".format(label, lat, lon))

        # Draw radius vector from earth & Red sphere for satellite
        #self.ax.plot([0,0],[0,0],[0,0],'r-')
        self.ax.plot([0, satx], [0, saty], [0, satz], 'b-')
        self.ax.plot([satx],[saty],[satz], 'bo')

        x,y,z = self.plot_earth()
        self.ax.plot_surface(x, y, z,  rstride=4, cstride=4, alpha=0.2, color='g')
        self.ax.set_axis_off()

        # Write satellite name next to it
        if label is not None:
            self.ax.text(satx, saty, satz, label, fontsize=11)
            #self.ax.text(satx, saty, satz, round(semi_major_axis,3), fontsize=10)

    def draw_orbit(self,*argv,print_info=False):
        '''This function calls the plot orbit function using the TLE elements defined in orbit.py'''
        o = Orbit()
        semi_major_axes = []
        for arg in argv:
            o.import_tle(arg)
            semi_major_axis = o.semi_major_axis_calc()
            semi_major_axes.append(semi_major_axis)
            true_anomaly = o.anomoly_calc()
            self.plot_orbit(semi_major_axis,o.eccentricity,o.inclination,o.right_ascension,
                            o.argument_periapsis,true_anomaly,o.title)

            if print_info is True:
                #Print Keplerian (Orbital) Elements
                print("----------------------------------------------------------------------------------------")
                print("----------------------------------------------------------------------------------------")
                print("Semi Major Axis [kilometers]                                {}".format(semi_major_axis))
                print("Inclination [Degrees]                                       {}°".format(o.inclination))
                print("Right Ascension of the Ascending Node [Degrees]             {}°".format(o.right_ascension))
                print("Eccentricity                                                {}".format(o.eccentricity))
                print("Argument of Periapsis [Degrees]                             {}°".format(o.argument_periapsis))
                print("True Anomaly [Degrees]                                      {}°".format(true_anomaly))
                print("----------------------------------------------------------------------------------------")
            else:
                pass

        #Scale Axes proportionate to the largest satellites radius
        max_axis = max(semi_major_axes)
        self.ax.auto_scale_xyz([-max_axis,max_axis],[-max_axis,max_axis],[-max_axis,max_axis])

        # Draw figure
        plt.show()
