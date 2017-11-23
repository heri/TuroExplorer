#!/usr/bin/python
# -*- coding: utf-8 -*-
 
import dryscrape
import sys
import bs4 as bs
import re
import datetime
import sqlite3 as lite
from sqlite3 import Error

if 'linux' in sys.platform:
    # start xvfb in case no X is running. Make sure xvfb 
    # is installed, otherwise this won't work!
    dryscrape.start_xvfb()

def setup_model(db_name):
    def create_connection(db_file):
        # create a database connection to a SQLite database
        try:
            conn = lite.connect(db_file)
            print(lite.version)
        except Error as e:
            print(e)
        finally:
            conn.close()

    if __name__ == '__main__':
        create_connection(db_name)

    conn = lite.connect(db_name)

    with conn:
        cur = conn.cursor()
        cur.execute("DROP TABLE IF EXISTS Cars")
        cur.execute("CREATE TABLE Cars(Id INT, Name TEXT, Amenities TEXT, Location TEXT, ReservationPrice INT, TotalTrips INT, Revenues INT)")
        return cur

model = setup_model('explorer.db')

sess = dryscrape.Session()
sess.set_attribute('auto_load_images', False)

def convert_to_int(search):
    return int(re.search(r'\d+', search).group())

def extract_from_page(page, name, element, elementClass, int_conversion = False):
    result = page.find(element, class_=elementClass)
    if int_conversion:
        c = convert_to_int(result.text)
        print("{name}: {result}".format(name=name, result=c))
        return c
    else:
        print("{name}: {result}".format(name=name, result=result.text))
        return result.text

def get_car_data(sess, url):
    sess.visit(url)
    page = bs.BeautifulSoup(sess.body(), 'lxml')

    # find car name
    name = extract_from_page(page, 'Make Model', 'p', 'vehicleLabel-makeModel')

    # find car location
    location = extract_from_page(page, 'Location', 'div', 'vehicleMapDetailsItem-description')

    # find car amenities
    amenities = [amenity.text for amenity in page.findAll('div', class_='labeledBadge-label')]
    if len(amenities) > 0:
        print("Amenities: {amenities}".format(amenities = ", ".join(amenities)))
    
    # find current reservation price
    reservation_price = int(extract_from_page(page, 'Reservation Price', 'span', 'reservationBoxVehiclePrice-amount'))

    # find trips so far from platform
    total_trips = extract_from_page(page, 'Trips', 'div', 'starRating-ratingLabel', int_conversion = True)

    # calculate total revenues
    revenues = total_trips * reservation_price
    print('Estimated Revenues: {revenues}'.format(revenues = '${:,.2f}'.format(revenues)))

    return {'name': name, 'amenities': amenities, 'location': location, 'reservation_price': reservation_price, 'total_trips': total_trips, 'revenues': int(revenues)}

car = get_car_data(sess, 'https://turo.com/rentals/suvs/nj/jersey-city/land-rover-range-rover-sport/84266')

for k, value in car.iteritems():
    print("{k} {value}".format(k=k, value=type(value)))

request = "INSERT INTO Cars VALUES(1, '{name}', '{amenities}', '{location}', {reservation_price}, {total_trips}, {revenues})".format(name=car['name'], amenities=" ,".join(car['amenities']), location=car['location'], reservation_price=car['reservation_price'], total_trips=car['total_trips'], revenues=car['revenues'])
model.execute(request)

# should be:
# cars = (
#     (1, 'Audi', 52642),
#     (2, 'Mercedes', 57127),
#     (3, 'Skoda', 9000)
# )
# model.executemany("INSERT INTO Cars VALUES(?, ?, ?)", cars)

# sess.render('{name}.png'.format(name=name))
# print('Screenshot written to {name}'.format(name=name))