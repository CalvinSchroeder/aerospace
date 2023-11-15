
from datetime import date

print()
coor = input('Please enter longitude (note West is negative): ')
datetime = input('Please enter date (dd/mm/yyyy), time (military): ')
print()

#getting coordinates in working order
long = float(coor)

#getting time in working order
times = datetime.split(', ')
clock = times[1]
dates = times[0].split('/')

#finding difference between user entered date and January 1, 2000
d1 = date(int(dates[2]), int(dates[1]), int(dates[0]))
d0 = date(2000, 1, 1)
delta = d1 - d0

#adding in the time difference between user entered time and noon
hours = (int(clock[:2])/24) + (int(clock[2:])/(24*60)) - 0.720347

#converting to days since J2000
delta_time = (float(delta.days) + hours)

#finding Greenwich mean sidereal time
gst = (1.0027379093 * 360 * delta_time) % 360
gst_rad = gst / 180
gst_tot_hours = gst / 15
gst_hours = gst_tot_hours // 1
gst_minutes = (gst_tot_hours - gst_hours) * 60 // 1
gst_seconds = (gst_tot_hours * 60) % 1 * 60 // 1

#time adjustments for local timezone
hour_adj = long // 15

#output
print()
print(f'Local Sidereal Time Degrees: {gst + long}')
print(f'Local Sidereal Time Radians: {gst_rad + long/180} * pi')
print(f'Local Sidereal Time hours {gst_tot_hours + hour_adj}')
print(f'Greenwich Sidereal Time: {int(gst_hours + hour_adj)}H {int(gst_minutes)}M {int(gst_seconds)}S')
print()
print(f'Greenwich Sidereal Time: {gst} Degrees')
print(f'Local Sidereal Time Radians: {gst_rad} * pi')
print(f'Greenwhich Sidereal Time: {gst_tot_hours} hours')
print(f'Greenwich Sidereal Time: {int(gst_hours)}H {int(gst_minutes)}M {int(gst_seconds)}S')
print()
