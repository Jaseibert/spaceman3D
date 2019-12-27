[![Version](https://img.shields.io/pypi/v/spaceman3D.svg)](https://pypi.python.org/pypi/spaceman3D)
[![License](https://img.shields.io/pypi/l/spaceman3D.svg)](https://pypi.python.org/pypi/spaceman3D)
[![Python](https://img.shields.io/pypi/pyversions/spaceman3D.svg)](https://pypi.python.org/pypi/spaceman3D)
[![Downloads](https://img.shields.io/pypi/dm/spaceman3D.svg?style=plastic)](https://img.shields.io/pypi/dm/spaceman3D.svg?style=plastic)
[![Build Status](https://travis-ci.org/Jaseibert/spaceman3D.svg?branch=master)](https://travis-ci.org/Jaseibert/spaceman3D)

**Author:** [Jeremy Seibert](https://www.jeremyseibert.com)<br/>
**License:** [MIT](https://opensource.org/licenses/MIT)<br/>

# Spaceman3D

Spaceman3D is a python package that accomplishes several unique tasks within the space of Astrodynamics (pun intended). The package gives users the ability to parse satellite Two-Line Element (TLE) Data into its Ballistic, Keplerian, and satellite identifying orbital elements. Beyond, this SpaceMan uses a `Matplotlib` 3D plotting toolkit to plot the orbit of the satellites.

[![Spaceman3D Demo](https://i.imgur.com/W41jW2o.png)](https://vimeo.com/322704127 "Spaceman3D Draw Orbit Demonstration - Click to Watch!")

# Basic Plotting Functionality

The plotting functionality mentioned below is accessed through the Draw() module.

```python
from spaceman3D.Draw import Draw
from spaceman3D.Orbit import satellites

#Create a class instance of Draw()
d = Draw()

#Call the draw Orbit function
d.draw_orbit(satellites.ISS, satellites.Dragon)

#or What would the Satellite look like around the Moon
d.draw_orbit(satellites.Dragon, object='Moon')
```

Using the code above will output an image that resembles this:

![alt text](./info/img/ISS_Dragon.png)

Along with this, by calling the `draw_orbit(element ,print_info=True)` you will print out the keplerian elements used to calculate the satellites trajectory.

![alt text](./info/img/example_output.png)

# Basic TLE Parser Functionality

```python
from spaceman3D.Orbit import tle, satellites

#Create a class instance of tle()
t = tle()

#Call the satellite elements function
t.tle_satellite_elements(satellites.ISS, satellites.Dragon, print_info=True)
```

## Orbital Mechanic's Resources
I know that I struggled to find resources explaining the mathematics used within Astrodynamics and orbital mechanics, so I have included the "PackageCalculations.txt" file that explains the mathematics behind the functions in Orbit.py and tle.py and the logic behind each function.
