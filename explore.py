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
prices = sess.at_xpath("//span[@class='reservationBoxVehiclePrice-amount']")

# view all car prices
for element in prices:
    print(element)

sess.render('land-rover.png')
print('Screenshot written to land-rover')