# -*- coding: utf-8 -*-
"""
Created on Fri Jun 26 17:09:15 2020

@author: Chris
"""

from splinter import Browser
import requests
from bs4 import BeautifulSoup
import pandas as pd


def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    # executable_path = {"executable_path": "/usr/local/bin/chromedriver"} # MAC USERS!
    executable_path = {"executable_path": "chromedriver.exe"} # WINDOWS USERS!
    browser = Browser("chrome", **executable_path, headless=False)
    return browser
    

def facts():
    url = 'https://space-facts.com/mars/'
    df_mars = pd.read_html(url)[0]
    df_mars.columns=["Description","Value"]
    df_mars.set_index("Description", inplace=True)
    return df_mars.to_html(classes="table table-bordered")


def scrape():
    info = {}

    url = 'https://mars.nasa.gov/news/'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    info["news_title"] = soup.find('div', class_="content_title").a.text
    info["news_p"] = soup.find('div', class_='rollover_description_inner').text
    
    browser = init_browser()
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    featured_image = soup.find_all('a', class_='fancybox')[1]['data-fancybox-href']
    info["featured_image_url"] = f'https://www.jpl.nasa.gov{featured_image}'
    
    info["facts_table"] = facts()
    
    info["hemisphere_image_urls"] = [
            {"title": "Valles Marineris Hemisphere", "img_url": "https://astropedia.astrogeology.usgs.gov/download/Mars/Viking/valles_marineris_enhanced.tif/full.jpg"},
            {"title": "Cerberus Hemisphere", "img_url": "https://astropedia.astrogeology.usgs.gov/download/Mars/Viking/cerberus_enhanced.tif/full.jpg"},
            {"title": "Schiaparelli Hemisphere", "img_url": "https://astropedia.astrogeology.usgs.gov/download/Mars/Viking/schiaparelli_enhanced.tif/full.jpg"},
            {"title": "Syrtis Major Hemisphere", "img_url": "https://astropedia.astrogeology.usgs.gov/download/Mars/Viking/syrtis_major_enhanced.tif/full.jpg"},
            ]
    
    browser.quit()
    
    return info

