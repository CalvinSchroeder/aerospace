
'''
Name: Calvin Schroeder
Class: AERO 201-501
Date: 9-15-2023

This program produces a chart of the altitude (geometric and geopotential) in feet, temperature in degrees R, pressure in pounds per square feet,
density in slugs per cubic feet, and the speed of sound in feet per second for standard atmosphere. The points of the chart are for every 500 ft
of geometric altitude from sea level (0 feet) to 100,000 feet.'''

import math

print()

#Top of the chart
print('GMet (ft) | GPot (ft) | T (Rankine) | P (lb/ft^2) | Rho (slugs/ft^3) | a [Vs] (ft/s)')

#Constants used for calculations
r = 1716 #ft * lb / slug * Rankine -> gas constant for normal air
g = 32.17 #ft / s / s -> gravity
r_earth = 2.092526 * 10**7 #m -> radius of the Earth
gamma = 1.4 #ratio i.e. no units -> constant for speed of sound equation

#Reference numbers for base and top of thermal regions
temp_graph = [(0, 518.69, 2.1162 * 10**3, 2.377 * 10 **(-3)), #temperature chart matrix
              (36089, 389.99, 4.6486 * 10**2, 6.9443 * 10**(-4)), #Geopotential height, base temp, base pressure, base density
              (82349, 389.99, 5.2837 * 10, 7.8931 *10**(-5)),
              (154199.475, 508.79, 2.5475, 2.9202 * 10**(-6))]

for n in range(int(100000/500+1)):
    #Producing geometric altitude
    geo_feet = float(500 * n)

    #Converting geometric altitude to geopotential altitude
    h = r_earth * float(geo_feet) / (r_earth + float(geo_feet))

    #Grabbing reference numbers for the calculations
    h_check = h - 1
    i = -1
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
    print('{:^10}'.format(f'{geo_feet:.6}'), end='|')
    print('{:^11}'.format(f'{h:.6}'), end='|')
    print('{:^13}'.format(f'{t:.5}'), end='|')
    print('{:^13}'.format(f'{p:.5}'), end='|')
    print('{:^18}'.format(f'{rho:.5}'), end='|')
    print('{:^14}'.format(f'{vs:.5}'))

print()
