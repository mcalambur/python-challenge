#!/usr/bin/env python
# coding: utf-8

from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
from flask import Flask, render_template, request, redirect, session, url_for
import pymongo
from pymongo import MongoClient
import time
import re

# Create an instance of Flask app.
app = Flask(__name__)

# Define the scrape function that will scrape the data 
def scrape():
    #Dict to store scraped values 
    mars_data_dict = {}
    mars_facts_dict = {}

    # # Open Chrome Browser

    executable_path = {'executable_path': 'chromedriver.exe'}
    # Keep "headless = False" - helps in troubleshooting & is simple switch for real website
    browser = Browser('chrome', **executable_path, headless=False)

    # ### Scrape NASA Mars News 

    nasa_url = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest/'
    browser.visit(nasa_url)
    time.sleep(12)

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
    mars_data_dict['Nasa Mars News Title'] = latest_title
    mars_data_dict['Nasa Mars News Date'] = latest_date
    mars_data_dict['Nasa Mars News Para'] = latest_para

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
    
    mars_data_dict['JPL Mars Image URL'] = image_list
    mars_data_dict['JPL Mars Image Title'] = title_list


    # ### Scrape Mars Weather from Twitter 
    weather_url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(weather_url)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

     # Locate the tweet text

    tweets = soup.find_all(text=re.compile("InSight"))
    weather_tweet = tweets[0]
    #store the tweet data
    mars_data_dict['Mars Weather Tweet'] = weather_tweet


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
    #stats.set_index('Measurement', inplace=True)
    
    # Add these into the main dict that is gathering all data
    for index, row in stats.iterrows():
        mars_facts_dict[row['Measurement']] = row['Mars']

    
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

    mars_data_dict['Mars Hemisphere Titles'] = large_images_titles



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
        #parse out the URLs
        p = str(large_image_urls[0])
        lg_begin = p.find('http://astropedia.astrogeology.usgs.gov')
        lg_end = p.find('jpg')
        lg_image = p[lg_begin:lg_end+3]
        large_images.append(lg_image)
        browser.visit(usgs_url)

    mars_data_dict['Mars Hemisphere Images'] = large_images
    # Combine the two disctionaries (1) for the text/images & (2) Tabular data     
    mars_data_dict.update(mars_facts_dict)
    browser.quit()
    # return the complete dict
    return(mars_data_dict)


# Create an instance of Flask app.
app = Flask(__name__)

# Initialize PyMongo to work with MongoDBs
conn = 'mongodb://localhost:27017'
client = pymongo.MongoClient(conn)

@app.route("/")
def index():
    #Create an empty list 
    marz = []
    #open database connection
    db = client['mars_db']
    #open the cursor in the collection and populate the list 
    mdata = db.mcoll.find()
    for m in mdata: 
        marz.append(m)
        # render home page with data provided by the list, obtained from mongo db collection  
    return render_template("index.html", mars_list=marz)

#Scrape to store in MongoDB
@app.route("/scrape/")
def getData():
    marscrape = {} 
    #Execute the scrape function receive all the data in a dict
    marscrape = scrape()
    #open db & collection
    db = client['mars_db']
    mcoll = db['mars_collection']
    # collection has data (left over connection), renove all documents
    if mcoll:
        print("Remove collection")
        db.mcoll.remove({})
        
##  indsert into a mongo db collection 
    for x, y in marscrape.items():
        db.mcoll.insert_one({x:y})   
    # go back to index.html so it can reference the mongo db collection and populate 
    return redirect(url_for('index', **request.args))


if __name__ == "__main__":
    app.run(host='127.0.0.1',port='5500', debug=True)

