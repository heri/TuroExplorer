import dryscrape
import sys
import bs4 as bs
import re

if 'linux' in sys.platform:
    # start xvfb in case no X is running. Make sure xvfb 
    # is installed, otherwise this won't work!
    dryscrape.start_xvfb()

sess = dryscrape.Session()
sess.set_attribute('auto_load_images', False)

sess.visit('https://turo.com/rentals/suvs/nj/jersey-city/land-rover-range-rover-sport/84266')

page = bs.BeautifulSoup(sess.body(), 'lxml')

names = page.find('p', class_='vehicleLabel-makeModel')
if len(names) > 0:
    name = names.text
    print('Make Model: {name}'.format(name = name))

    reservation_price = page.find('span', class_='reservationBoxVehiclePrice-amount').text
    print('Reservation Price: ${reservation_price}'.format(reservation_price = reservation_price))
    
    trips = page.find('div', class_='starRating-ratingLabel')
    total_trips = int(re.search(r'\d+', trips.text).group())
    print('Trips: {total_trips}'.format( total_trips = total_trips ) )
    
    location = page.find('div', class_='vehicleMapDetailsItem-description').text
    print('Location: {location}'.format(location = location))

    revenues = total_trips * int(reservation_price)
    print('Revenues: {revenues}'.format(revenues = '${:,.2f}'.format(revenues)))

    amenities = page.findAll('div', class_='labeledBadge-label')
    if len(amenities) > 0:
        print("Amenities: ")
        for amenity in amenities:
            print(amenity.text)

    # TODO : save name, reservation_price, total_trips, revenues, amenities city to database

    sess.render('{name}.png'.format(name=name))
    print('Screenshot written to {name}'.format(name=name))