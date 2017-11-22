import dryscrape
import sys
import bs4 as bs
import re
import datetime

if 'linux' in sys.platform:
    # start xvfb in case no X is running. Make sure xvfb 
    # is installed, otherwise this won't work!
    dryscrape.start_xvfb()

def convert_to_int(search):
    return int(re.search(r'\d+', search).group())

def get_from_page(page, name, element, elementClass):
    result = page.find(element, class_=elementClass)
    print("{name}: {result}".format(name=name, result=result.text))
    return result.text

sess = dryscrape.Session()
sess.set_attribute('auto_load_images', False)

sess.visit('https://turo.com/rentals/suvs/nj/jersey-city/land-rover-range-rover-sport/84266')

page = bs.BeautifulSoup(sess.body(), 'lxml')

name = get_from_page(page, 'Make Model', 'p', 'vehicleLabel-makeModel')

amenities = [amenity.text for amenity in page.findAll('div', class_='labeledBadge-label')]
if len(amenities) > 0:
    print("Amenities: {amenities}".format(amenities = ", ".join(amenities)))

# mileage = page.find('div', class_='reservationBoxMileage-distance')
# included_mileage = convert_to_int(mileage.text)
# print('Included mileage: {included_mileage}'.format(included_mileage = included_mileage))

location = get_from_page(page, 'Location', 'div', 'vehicleMapDetailsItem-description')

today = datetime.date.today()
print('Date: {date}'.format(date = today.strftime('%d, %b %Y')))

reservation_price = get_from_page(page, 'Reservation Price', 'span', 'reservationBoxVehiclePrice-amount')

trips = page.find('div', class_='starRating-ratingLabel')
total_trips = convert_to_int(trips.text)
print('Trips: {total_trips}'.format( total_trips = total_trips ) )

revenues = total_trips * int(reservation_price)
print('Estimated Revenues: {revenues}'.format(revenues = '${:,.2f}'.format(revenues)))

# TODO : save name, reservation_price, total_trips, revenues, amenities city to database

sess.render('{name}.png'.format(name=name))
print('Screenshot written to {name}'.format(name=name))