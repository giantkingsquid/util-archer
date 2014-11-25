from pylab import *
import datetime 
import sqlite3 as lite

import numpy as np
import matplotlib.pyplot as plt

sourceFile = 'archive/stats.sdb'
plot_year = 2013

con = lite.connect(sourceFile)
con.row_factory = lite.Row

cursor = con.cursor()
cursor.execute("SELECT dateTime, min, max FROM outTemp")

count = 0
x = []
temp_min = []
temp_max = []
year = None

for row in cursor:
    if row['min'] is not None:
        dt = datetime.datetime.fromtimestamp(row['dateTime'])
        yr = dt.year

        if yr != year:
            if count > 0:
                print "%d records" % count
            print "Year %d" % yr
            year = yr
            count = 0

        if plot_year == yr:
            day_of_year = int(dt.strftime('%j'))
            angle = day_of_year * 2.0 * np.pi / 365

            x.append(angle)
            temp_min.append((float(row['min']) - 32.0) / 1.8)
            temp_max.append((float(row['max']) - 32.0) / 1.8)

            count += 1

print "%d records" % count

print "Plotting..."

ax = plt.subplot(111, polar=True)
ax.plot(x, temp_min)
ax.plot(x, temp_max)
ax.set_rmin(-10)
ax.grid(True)
ax.set_theta_direction(-1)
ax.set_theta_offset(np.pi / 2)

ax.set_title("Min and Max daily temperature, %d" % plot_year, va='bottom')

plt.savefig('temp_polar.jpg', dpi=300)
plt.show()