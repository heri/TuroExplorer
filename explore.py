#!/usr/bin/python
# -*- coding: utf-8 -*-
 
import dryscrape
import sys
import bs4 as bs
import re
import datetime
import sqlite3 as lite
from sqlite3 import Error
import time

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
        cur.execute("CREATE TABLE Cars(Id INT, Url TEXT, Name TEXT, Year INT, Amenities TEXT, Location TEXT, ReservationPrice INT, TotalTrips INT, Revenues INT)")
        return cur

model = setup_model('explorer.db')

def convert_to_int(search):
    return int(re.search(r'\d+', search).group())

def extract_from_page(page, name, element, elementClass, int_conversion = False):
    result = page.find(element, class_=elementClass)

    try:
        if int_conversion:
            c = convert_to_int(result.text)
            print("{name}: {result}".format(name=name, result=c))
            return c
        else:
            print("{name}: {result}".format(name=name, result=result.text))
            return result.text
    except:
        res = "No {name} found".format(name=name)
        return 0 if int_conversion else res

def get_car_data(row_number, url):
    sess = dryscrape.Session()
    sess.set_attribute('auto_load_images', False)
    sess.visit(url)

    wait = 1
    # print("\nPause {wait}s - crawling {url}".format(wait=wait, url=url))
    time.sleep(wait)
    page = bs.BeautifulSoup(sess.body(), 'lxml')
    
    # find car name
    name = extract_from_page(page, 'Make Model', 'p', 'vehicleLabel-makeModel')

    # parsing unsuccessful 
    if name = "No Make Model found":
        print("{name} for {wait} sec loading".format(name=name, wait=wait))
        return

    # find year
    year = extract_from_page(page, 'Year', 'div', 'vehicleLabel-year', int_conversion= True)

    # find car location
    location = extract_from_page(page, 'Location', 'div', 'vehicleMapDetailsItem-description')

    # find car amenities
    search = [amenity.text for amenity in page.findAll('div', class_='labeledBadge-label')]
    amenities =  ", ".join(search)
    if len(amenities) > 0:
        print("Amenities: {amenities}".format(amenities = amenities))
    
    # find current reservation price
    reservation_price = extract_from_page(page, 'Reservation Price', 'span', 'reservationBoxVehiclePrice-amount', int_conversion = True)

    # find trips so far from platform
    total_trips = extract_from_page(page, 'Trips', 'div', 'starRating-ratingLabel', int_conversion = True)

    # calculate total revenues
    revenues = total_trips * reservation_price
    print('Estimated Revenues: {revenues}'.format(revenues = '${:,.2f}'.format(revenues)))

    # human visit, not a crawler
    more = sess.at_xpath('//*[contains(text(), "See more feedback")]')
    if more:
        more.click()

    # sess.render('{name}.png'.format(name=name))
    # print('Screenshot written to {name}'.format(name=name))

    return (row_number, name, year, amenities, location, reservation_price, total_trips, int(revenues), url)

car_list = (
    'https://turo.com/rentals/suvs/nj/jersey-city/land-rover-range-rover-sport/84266',
    'https://turo.com/rentals/cars/nj/jersey-city/alfa-romeo-4c/121327',
    'https://turo.com/rentals/suvs/nj/jersey-city/mazda-cx-9/84783',
    'https://turo.com/rentals/cars/nj/jersey-city/honda-accord/178749',
    'https://turo.com/rentals/cars/il/chicago/volkswagen-passat/152129',
    'https://turo.com/rentals/cars/nj/paterson/hyundai-sonata/98689',
    'https://turo.com/rentals/suvs/ma/boston/subaru-outback/49162',
    'https://turo.com/rentals/cars/nj/hasbrouck-heights/bmw-3-series/172636',
)

cars = ()
for idx, url in enumerate(car_list):
    car_data = get_car_data(idx + 1, url)
    if car_data:
        cars = cars + (car_data, )

query = model.executemany("INSERT INTO Cars VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)", cars)

# Check db
model.execute("SELECT * FROM Cars")
rows = model.fetchall()
for row in rows:
    print row