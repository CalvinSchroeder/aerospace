
'''
Name: Calvin Schroeder
Class: AERO 201-501
Date: 9-8-2023

This program accepts input altitude in geometric feet and computes ICAO Standard Atmosphere.
The program then outputs temperature in degrees R, pressure in pounds per square feet,
density in slugs per cubic feet, and the speed of sound in feet per second.
The gas is assumed to be air.'''

import math

#Input
geo_feet = input('Please enter the geometric altitude in feet w/o units: ') #Does not accept the feet units

#Constants used for calculations
r = 1716 #ft * lb / slug * Rankine -> gas constant for normal air
g = 32.17 #ft / s / s -> gravity
r_earth = 2.092526 * 10**7 #m -> radius of the Earth
gamma = 1.4 #ratio i.e. no units -> constant for speed of sound equation

#Geometric altitude to geopotential altitude conversion
h = r_earth * float(geo_feet) / (r_earth + float(geo_feet))

#Reference numbers for base and top of thermal regions
temp_graph = [(0, 518.69, 2.1162 * 10**3, 2.377 * 10 **(-3)), #temperature chart matrix
              (36089, 389.99, 4.6486 * 10**2, 6.9443 * 10**(-4)), #Geopotential height, base temp, base pressure, base density
              (82349, 389.99, 5.2837 * 10, 7.8931 *10**(-5)),
              (154199.475, 508.79, 2.5475, 2.9202 * 10**(-6))]#''',
'''              (173884.514, 508.79, , ), #this is for higher regions
              (259186.352, 298.188, , ), #but we don't have the reference numbers for pressure and density
              (295275.591, 298.188, , )
              (344488.189, 406.19, , )]'''

#Grabbing reference numbers for the calculations
i = -1
h_check = h - 1
if h <= 153856:
    while h > h_check:
        i += 1
        h_check = temp_graph[i+1][0]
        h1 = temp_graph[i][0]
        t1 = temp_graph[i][1]
        p1 = temp_graph[i][2]
        rho1 = temp_graph[i][3]
else:
    h1 = temp_graph[-1][0]
    t1 = temp_graph[-1][1]
    p1 = temp_graph[-1][2]
    rho1 = temp_graph[-1][3]
h2 = temp_graph[i+1][0]
t2 = temp_graph[i+1][1]

#Calculating the lapse rate
a = (t2 - t1) / (h2 - h1)

#print(r_earth, a, h1, t1, p1, rho1)

#Temperature calculations
t = t1 + a * (h - h1)

#Pressure calculations
if a == 0: #for isothermal regions
    p = p1 * math.exp(g * (h1 - h)/(r * t))
else: #for gradient regions
    p = p1 * (t1 / t) ** (g/(a * r))

#Density calculations
if a == 0:
    rho = rho1 * math.exp(g * (h1 - h)/(r * t))
else:
    rho = rho1 * (t1 / t) ** (g/(a * r) + 1)

#Speed of sound calculations
vs = (gamma * r * t)**(1/2)

#Output
print()
print(f'Geopotential Altitude: {h:.5} ft, Temperature: {t:.5} Rankine, Pressure: {p:.5} lb/ft^2, Density {rho:.5} slugs/ft^3, Speed of Sound {vs:.5} ft/s.')
print()
