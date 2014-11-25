from pylab import *
import datetime 
import sqlite3 as lite

import matplotlib.pyplot as plt

sourceFile = 'archive/weewx.sdb'
year_start = 2013

con = lite.connect(sourceFile)
con.row_factory = lite.Row

cursor = con.cursor()
cursor.execute("SELECT dateTime, outTemp FROM archive")

limit = 0
count = 0
x = {}
y = {}
year = None

for row in cursor:
    if limit < 400000:
        if row['outTemp'] is not None:

            dt = datetime.datetime.fromtimestamp(row['dateTime'])
            yr = dt.year

            if yr >= year_start:
                if yr != year:
                    if count > 0:
                        print "%d records" % count
                        x[year] = x_temp
                        y[year] = y_temp
                    print "Year %d" % yr
                    year = yr
                    x_temp = []
                    y_temp = []
                    count = 0

                day_of_year = int(dt.strftime('%j'))

                temp = (float(row['outTemp']) - 32.0) / 1.8

                x_temp.append(day_of_year)
                y_temp.append(temp)

                count += 1
    limit += 1

print "%d records" % count
x[year] = x_temp
y[year] = y_temp

print "Plotting..."

bin_sizes=(52, 30)

plt.figure(1)

plt.subplot(211)
plt.title("2013")
plt.hist2d(x[2013], y[2013], bins=bin_sizes)
plt.xticks((0, 30+28+31, 30+28+31+30+31+30, 30+28+31+30+31+30+31+31+30), ('', '', '', ''))

plt.subplot(212)
plt.title("2014")
plt.hist2d(x[2014], y[2014], bins=bin_sizes)
plt.xlabel('Time of year')
plt.xticks((0, 30+28+31, 30+28+31+30+31+30, 30+28+31+30+31+30+31+31+30), ('Jan', 'Apr', 'Jul', 'Oct'))

plt.savefig('temp_plots.jpg', dpi=300)
plt.show()


