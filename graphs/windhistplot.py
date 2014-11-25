from pylab import *
import datetime 
import sqlite3 as lite

import numpy as np
import matplotlib.pyplot as plt

sourceFile = 'archive/weewx.sdb'
year_start = 2010

con = lite.connect(sourceFile)
con.row_factory = lite.Row

cursor = con.cursor()
cursor.execute("SELECT dateTime, windSpeed, windDir FROM archive")

x = []
y = []
year = None
limit = 0
count = 0

for row in cursor:
    if limit < 400000:
        if row['windDir'] is not None:
            ws = int(float(row['windSpeed']) * 10.0)
            if ws > 1:

                dt = datetime.datetime.fromtimestamp(row['dateTime'])
                yr = dt.year

                if yr >= year_start:
                    if yr != year:
                        if count > 0:
                            print "%d records" % count
                        print "Year %d" % yr
                        year = yr
                        count = 0

                    day_of_year = int(dt.strftime('%j'))

                    wind_dir = float(row['windDir'])
                    if wind_dir > 180:
                        wind_dir -= 360

                    while ws > 0:
                        x.append(day_of_year)
                        y.append(wind_dir)
                        ws -= 1

                    count += 1
    limit += 1
print "%d records" % count

print "Plotting..."



plt.figure(1)
plt.subplot(211)
H, xedges, yedges = np.histogram2d(x, y, bins=(52, 16), normed=True)
new_x, new_y = 0.5*(xedges[1:]+xedges[:-1]), 0.5*(yedges[1:]+yedges[:-1])
z = H.T
plt.contour(new_x, new_y, z, 4)

plt.xticks((0, 90, 180, 270), ('', '', '', ''))

plt.yticks((-180, -90, 0, 90, 180), ('S', 'W', 'N', 'E', 'S'))
plt.ylabel('Wind dir')

plt.subplot(212)
plt.hist2d(x, y, bins=(52, 16))

plt.xlabel('Time of year')
plt.xticks((0, 90, 180, 270), ('Jan', 'Apr', 'Jul', 'Oct'))

plt.yticks((-180, -90, 0, 90, 180), ('S', 'W', 'N', 'E', 'S'))
plt.ylabel('Wind dir')

plt.savefig('wind_dir_plots.jpg', dpi=300)
plt.show()


