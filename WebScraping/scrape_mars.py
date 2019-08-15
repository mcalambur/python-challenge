#!/usr/bin/env python
# coding: utf-8

from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd

#Dict to store scraped values 
scrape_dict = {}

# # Open Chrome Browser

executable_path = {'executable_path': 'chromedriver.exe'}
browser = Browser('chrome', **executable_path, headless=False)

# ### Scrape NASA Mars News 

nasa_url = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest/'
browser.visit(nasa_url)

# Latest News title, date & para

html = browser.html
soup = BeautifulSoup(html, 'html.parser')

titles = soup.find_all('div', class_='content_title')
dates = soup.find_all('div', class_='list_date')
paras = soup.find_all('div', class_='article_teaser_body')

latest_title = titles[0].text
latest_date = dates[0].text
latest_para = paras[0].text

# Store in dict
scrape_dict['Nasa Mars News Title'] = latest_title
scrape_dict['Nasa Mars News Date'] = latest_date
scrape_dict['Nasa Mars News Para'] = latest_para

# ###  Scrape JPL Mars Space Images - Featured Image

jpl_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
browser.visit(jpl_url)

html = browser.html
soup = BeautifulSoup(html, 'html.parser')

# Locate the URL 
image_list = []
title_list = []
# Locate the URL 
for link in soup.find_all('img', limit = 5):
    src = link.get('src')
    title = link.get('title')
    if src.startswith("/spaceimages"): #check src starts with /spaceimages
        image_list.append('https://www.jpl.nasa.gov'+ src)
    if title: #check src starts with /spaceimages
        title_list.append(title)
    
scrape_dict['JPL Mars Image URL'] = image_list
scrape_dict['JPL Mars Image Title'] = title_list


# ### Scrape Mars Weather from Twitter 
weather_url = 'https://twitter.com/marswxreport?lang=en'
browser.visit(weather_url)

html = browser.html
soup = BeautifulSoup(html, 'html.parser')

# Locate the tweet text 
tweets = soup.find_all('div', class_= 'js-tweet-text-container', limit =2)
weather_tweet = tweets[1].text

scrape_dict['Mars Weather Tweet'] = weather_tweet


# ### Scrape Mars Facts
facts_url = 'https://space-facts.com/mars/'
# Get the tables 
tables = pd.read_html(facts_url)

# Get the 1st table & drop column on Earth 
df1 = tables[0]
del df1['Earth']
df1.rename({'Mars - Earth Comparison': 'Measurement'}, axis=1, inplace=True)

# As data continues in the 2nd table, get it into another dataframe
df2 = tables[1]
df2.columns = ['Measurement', 'Mars']

# Combine the two dataframes 
stats = pd.concat([df1, df2])
stats.set_index('Measurement', inplace=True)
print("Mars Facts:")
print(stats)


# ### Scrape images for Mars Hemispheres

usgs_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
browser.visit(usgs_url)

# Create an list, use h3 to locate titles, strip the h3 tags & save in list 
large_images_titles = []
html = browser.html
soup = BeautifulSoup(html, 'html.parser')
titles2 = soup.find_all('h3',  limit = 4)
for title in titles2: 
    x = str(title)
    large_images_titles.append(x[4:-5])

scrape_dict['Mars Hemisphere Titles'] = large_images_titles



# Create a list for the image URLs. 
# Use xpath in a for loop to locate and click to get URL of the high def images 
# Parse the URL for each image 

large_images = []
for dv in range(1, 5):
    xpath = '//*[@id="product-section"]/div[2]/div[' + str(dv) + ']/a/img'
    browser.find_by_xpath(xpath).click()
    browser.find_by_xpath('//*[@id="wide-image-toggle"]').click()
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    large_image_urls = soup.find_all('div', class_= 'wide-image-wrapper')
    p = str(large_image_urls[0])
    lg_begin = p.find('http://astropedia.astrogeology.usgs.gov')
    lg_end = p.find('jpg')
    lg_image = p[lg_begin:lg_end+3]
    large_images.append(lg_image)
    browser.visit(usgs_url)

scrape_dict['Mars Hemisphere Images'] = large_images


for x, y in scrape_dict.items():
  print(x, y) 