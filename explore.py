import dryscrape
import sys

if 'linux' in sys.platform:
    # start xvfb in case no X is running. Make sure xvfb 
    # is installed, otherwise this won't work!
    dryscrape.start_xvfb()

site = 'https://turo.com'
sess = dryscrape.Session(base_url = site)
sess.set_attribute('auto_load_images', False)

sess.visit('/rentals/suvs/nj/jersey-city/land-rover-range-rover-sport/84266')
name = sess.xpath("//p[@class='vehicleLabel-makeModel']//text()")
if len(name) > 0:
    print name[0]
price = sess.xpath("//span[@class='reservationBoxVehiclePrice-amount']//text()")
if len(price) > 0:
    print price[0]

trips = sess.xpath("//div[@class='starRating-ratingLabel']//text()")
if len(trips) > 0:
    print trips[0]

sess.render('land-rover.png')
print('Screenshot written to land-rover')