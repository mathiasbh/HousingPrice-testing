from bs4 import BeautifulSoup
import urllib.request
import pandas as pd
import numpy as np
import re
import random
import time

# Webscrape from aarhusbolig.dk

urlpages = 121

url = ('https://www.aarhusbolig.dk/Soeg-bolig?Fritekst=&omr-data-carrier=&\
BoligOmraader=&org-data-carrier=&Selskaber=&bolig-data-carrier=&BoligTyper=&\
FloorWish.Min=&FloorWish.Max=&min-data-carrier=&HuslejeMin=&max-data-carrier=&\
HuslejeMax=&antv-data-carrier=&AntalVaerelser=&antvmax-data-carrier=&\
AntalVaerelserMax=&div-data-carrier=&BoligArealMin=0&BoligArealMax=200&\
orderby=&sort=&page=')

# Initialize lists for storing data
size_list = []  # m^2
room_list = []  # number of rooms
department_list = []  # which department is the home
homeType_list = []  # type of home
numberOfHomes_list = []  # number of this type of home
price_list = []  # kr
link_list = []  # link to home
address_list = []  # ...
zipcode_list = []  # ...
latitude_list = []
longitude_list = []

# Iterate over all url pages
counter = 0
pageList = list(range(1, urlpages + 1))
random.shuffle(pageList)
for pageNum in pageList:
    counter += 1
    print('Page number: ' + str(pageNum) + ' --- ' + str(counter) + '/' + str(urlpages))
    page = urllib.request.urlopen(url + str(pageNum))
    soup = BeautifulSoup(page.read(), "html5lib")
    body = soup.find_all('div', class_='hc-details')  # contains list of homes

    # Iterate over elements in body
    for element in body[16:]:  # Page1 duplicates on all pages
        # size, #rooms, homeType, #homes
        home_data = element.find_all('table', class_='hc-bolig-data')[0].tbody.find_all('td')
        size_list.append(int(re.search('\d+', home_data[3].get_text()).group(0)))
        room_list.append(int(re.search('\d+', home_data[2].get_text()).group(0)))
        homeType_list.append(home_data[0].get_text())
        numberOfHomes_list.append(int(re.search('\d+', home_data[1].get_text()).group(0)))

        # address, zipcode, department
        address_data = element.find_all('div', class_='hc-address')[0].find_all('p')
        address_list.append(address_data[1].get_text())
        zipcode_list.append(int(re.search('\d+', address_data[2].get_text()).group(0)))
        department_list.append(int(re.search('\d+', address_data[0].get_text()).group(0)))

        # coordinates
        extra_data = element.find_all('a', class_='btn btn-r icon-map js-map')
        if len(extra_data) == 0:
            latitude_list.append(0.000)
            longitude_list.append(0.000)
        else:
            coords = re.search('\d+\.\d+,\d+\.\d+', extra_data[0]['href']).group(0).split(',')
            latitude_list.append(float(coords[0]))
            longitude_list.append(float(coords[1]))

        # price
        price_data = element.find_all('span', class_='hc-price')[0]
        # needs cleaning (remove '.' and 'Kr.')
        price_list.append(price_data.get_text())

        # link
        link_data = element.find_all('a', class_='hc-link')[0]
        link_list.append(link_data['href'][21:])

    time.sleep(1.5)
    # end loop

# Pandas
ordercol = ['Department', 'Size', 'Rooms', 'Price', 'HomeType', 'NumberHomes',
            'Latitude', 'Longitude', 'Zipcode', 'Link']
df = pd.DataFrame({'Price': price_list,
                   'Size': size_list,
                   'Rooms': room_list,
                   # 'Address': address_list,
                   'Department': department_list,
                   'HomeType': homeType_list,
                   'NumberHomes': numberOfHomes_list,
                   'Zipcode': zipcode_list,
                   'Latitude': latitude_list,
                   'Longitude': longitude_list,
                   'Link': link_list},
                  columns=ordercol)


# Process data
df.Price = df.Price.str.replace(' Kr.', '')
df.Price = df.Price.str.replace('.', '')

dict_replace = {'í': 'i',
                'á': 'a',
                'ø': 'oe',
                'Ø': 'Oe',
                'å': 'aa',
                'Å': 'Aa',
                'æ': 'ae',
                'Æ': 'ae',
                'ü': 'u',
                'é': 'e'}
df.replace(dict_replace, regex=True, inplace=True)


# Save to txt
fmtcol = '%4s,%4s,%4s,%6s,%23s,%4s,%18s,%18s,%6s,%44s'
np.savetxt(r'scrapedata.txt', df.values, fmt=fmtcol, header=' '.join(df.columns.values))
