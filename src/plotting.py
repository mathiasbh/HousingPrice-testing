import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

color_scheme = plt.get_cmap('summer')

h = ['Department', 'Size', 'Rooms', 'Price', 'HomeType',
     'NumberHomes', 'Latitude', 'Longitude', 'Zipcode', 'Link', 'skip']
data = pd.read_csv('scrapedata.txt', sep=',\s+', header=1, names=h, engine='python')


# Try various plots
plt.figure()
plt.xlabel('Size [m^2]')
plt.ylabel('Price [kr]')
plt.plot(data.Size, data.Price, 'k.')

plt.figure()
plt.xlabel('Rooms')
plt.ylabel('Price [kr]')
plt.plot(data.Rooms, data.Price, 'k.')

plt.figure()
plt.xlabel('Department number')
plt.ylabel('Price [kr]')
plt.plot(data.Department, data.Price, 'k.')

plt.figure()
plt.xlabel('Zipcode')
plt.ylabel('Price [kr]')
plt.plot(data.Zipcode, data.Price, 'k.')

plt.figure()
plt.xlabel('Rooms')
plt.ylabel('Size [m^2]')
plt.plot(data.Rooms, data.Size, 'k.')

plt.figure()
plt.xlabel('Latitude')
plt.ylabel('Longitude')
cut = (data.Latitude > 55) & (data.Longitude > 9)
plt.scatter(data.Latitude[cut], data.Longitude[cut], c=data.Price[cut], marker='.', s=100, lw=None, cmap=color_scheme, vmin=1300, vmax=14000)
plt.colorbar()
plt.show()
