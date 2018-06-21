from selenium import webdriver
import re
import csv
import time
from selenium.common.exceptions import NoSuchElementException

driver = webdriver.Chrome('/Users/ottosharples/Downloads/chromedriver')
driver.get('https://www.tripadvisor.com/members/misopiso88')
        
def check_exists_by_selector(selector):
    try:
        driver.find_element_by_css_selector(selector)
    except NoSuchElementException:
        return False
    else:
    	return True

def scrape():
	print('Scrape page started')
	i = 4
	counter = 18
	while i < 55:

		# Go to correct span of reviews
		driver.execute_script("document.getElementsByClassName('cs-paginate-goto')[1].innerHTML = '"+str(counter)+"'")
		driver.find_element_by_css_selector('.cs-paginate-goto:nth-child(2)').click()

		time.sleep(1)

		# Build selector for link to click
		selector = '.modules-membercenter-content-stream .cs-review:nth-child('
		selector +=str(i) 
		selector += ') .cs-review-title'

		# Check if there are  elements left and if there aren't, go to next page, reset i, delay to allow page load, and build new selector. Also add one to counter that controls what set of reviews you are on
		if check_exists_by_selector(selector) == False :
			i = 1
			counter += 1

			selector = '.modules-membercenter-content-stream .cs-review:nth-child('
			selector +=str(i) 
			selector += ') .cs-review-title'

			driver.execute_script("document.getElementsByClassName('cs-paginate-goto')[0].innerHTML = '"+str(counter)+"'")
			driver.find_element_by_css_selector('.cs-paginate-goto:nth-child(1)').click()

			time.sleep(1)



		# Click on review link
		print('Scraping ', i)
		elem = driver.find_element_by_css_selector(selector);
		elem.click()

		# Get all elements
		if check_exists_by_selector('.sur_layout_redesign .surContent .HEADING'):

			rest = driver.find_element_by_css_selector('.sur_layout_redesign .surContent .HEADING').text
			title = driver.find_element_by_css_selector('.sur_layout_redesign #HEADING #PAGEHEADING').text

			ratingString = driver.find_element_by_css_selector('.ui_bubble_rating').get_attribute('class')
			p = re.compile('[1-5]');
			rating = p.search(ratingString).group()

			review = driver.find_element_by_css_selector('.partial_entry').text

		else:
			rest = driver.find_element_by_css_selector('span.ui_header').text
			title = driver.find_element_by_css_selector('#HEADING.title').text

			ratingString = driver.find_element_by_css_selector('span.ui_bubble_rating').get_attribute('class')			
			p = re.compile('[1-5]');
			rating = p.search(ratingString).group()

			review = driver.find_element_by_css_selector('.fullText').text

		row = [rest, title, rating, review]			
		writer.writerow(row)

		# Go back to review list
		driver.execute_script("window.history.go(-1)")

		i+=1

outfile = open("Desktop/reviews.csv", "w")
writer = csv.writer(outfile)
scrape()



