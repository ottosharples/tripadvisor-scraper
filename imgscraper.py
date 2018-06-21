from selenium import webdriver
import re
import csv
import time
from selenium.common.exceptions import NoSuchElementException

driver = webdriver.Chrome('/Users/ottosharples/Downloads/chromedriver')
driver.get('https://www.tripadvisor.com/members/misopiso88')
driver.find_element_by_xpath('//li[@data-filter="PHOTOS_ALL"]').click()
        
def check_exists_by_selector(selector):
    try:
        driver.find_element_by_css_selector(selector)
    except NoSuchElementException:
        return False
    else:
    	return True

def scrape():
	print('Scrape page started')
	i = 1
	counter = 1
	other_counter = 1
	while i < 55:

		# Build selector for img
		selector = '.cs-photo:nth-child('
		selector += str(i)
		selector += ') img'

		# Check if there are  elements left and if there aren't, go to next page, reset i, delay to allow page load, and build new selector. Also add one to counter that controls what set of reviews you are on
		if check_exists_by_selector(selector) == False :
			i = 1
			counter += 1

			selector = '.cs-photo:nth-child('
			selector += str(i)
			selector += ') img'

			if counter == 2:
				driver.execute_script("document.getElementsByClassName('cs-paginate-goto')[1].innerHTML = '"+str(counter)+"'")
				driver.find_element_by_css_selector('.cs-paginate-goto:not(.active):nth-child(2)').click()
			else:
				driver.execute_script("document.getElementsByClassName('cs-paginate-goto')[0].innerHTML = '"+str(counter)+"'")
				driver.find_element_by_css_selector('.cs-paginate-goto:not(.active):nth-child(1)').click()

			time.sleep(1)



		print('Scraping ', other_counter)
		other_counter += 1

		img = driver.find_element_by_css_selector(selector)

		# Get all elements
		img_src = img.get_attribute('src')

		selector = '.cs-photo:nth-child('
		selector += str(i)
		selector += ') .cs-photo-location a'

		img_review = driver.find_element_by_css_selector(selector).get_attribute('innerHTML')

		row = [img_src, img_review]				
		writer.writerow(row)

		i+=1

outfile = open("./imgs.csv", "w")
writer = csv.writer(outfile)
scrape()



