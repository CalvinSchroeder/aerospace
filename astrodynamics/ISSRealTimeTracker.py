
import matplotlib.pyplot as plt
import requests as rqsts
import cartopy.crs as ccrs
import numpy as np
import cartopy.feature as cfeat
import time

def update_graph(lo, la):
    path.set_data(lo, la)
    ax.relim()
    ax.autoscale_view()
    plt.draw()

print()
#accessing API for ISS and Shenzhou 15 crews and the lat and long of the ISS
ISSastr = rqsts.get('http://api.open-notify.org/astros.json')

rawcrew = ISSastr.text

crew = rawcrew.split('}, {')

crewcnt = 0
crewnames = []

for member in crew: #parse through data to only include ISS crew
    if "ISS" in member:
        crewcnt += 1
        ID = member.split('name')
        crewnames += [ID[1][4:-17]]
 
ISScrew = input('Would you like to know more about the current ISS crew? [y/n] ')

print()

if ISScrew in 'Yy': #prints out the crew
    print(f'Currently, the ISS has {crewcnt} crew members.\n')
    print(f'The crewmembers on the ISS are {crewnames[0]}', end='')
    for person in crewnames[1:-2]:
        print(',', person, end='')
    print(f', and {crewnames[-1][:]}.')
    print()
else:
    print('Fine, be that way.')
    print()

ready = input('Are you ready to see the ISS path plotted? [y/n] ')

if ready in 'Yy':
    long = []
    lat = []

    #creates the map plot, Equal Earth projection
    fig = plt.figure(figsize=(10,6))
    ax = plt.axes(projection=ccrs.EqualEarth())
    ax.set_title('Live ISS Path Tracker')

    path, = ax.plot(long, lat, transform=ccrs.PlateCarree(), color='w')

    #Add some features to the map
    ax.add_feature(cfeat.COASTLINE)
    ax.add_feature(cfeat.BORDERS)
    ax.gridlines(draw_labels=True)
    ax.set_global() #keeps the map zoomed out on the whole world
    ax.add_feature(cfeat.LAND, color='g')
    ax.add_feature(cfeat.OCEAN, color='b')

while ready in 'Yy':
    ISScoor = rqsts.get('http://api.open-notify.org/iss-now.json')
    rawcoor = ISScoor.text
    coordict = eval(rawcoor) #retrieving data from API source -> dictionary
    
    newlat = coordict['iss_position']['latitude']
    newlat = float(newlat)
    #cleans up the longitude and latitude data to friendly format
    newlong = coordict['iss_position']['longitude']
    newlong = float(newlong)

    lat.append(newlat)
    long.append(newlong)

    oldlat = [] #chunk to prevent path of ISS cutting across entire globe when ISS circumnavigates the globe
    oldlong = []
    if len(long) > 1:
        if long[-1] < long[-2]:
            oldlong.append([long[0:-2]])
            long = [long[-1]]
            oldlat.append([lat[0:-2]])
            lat = [lat[-1]]
            for i in range(len(oldlong)):
                ax.plot(oldlong[i], oldlat[i], transform=ccrs.PlateCarree(), color='silver') 

    update_graph(long,lat)

    if 'ISS' in locals():
        ISS.remove()

    ISS = ax.scatter(newlong, newlat, transform=ccrs.PlateCarree(), color='r')
    plt.pause(5)

plt.show()
