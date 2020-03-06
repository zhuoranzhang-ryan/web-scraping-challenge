import pandas as pd
from bs4 import BeautifulSoup
import requests
import pymongo
from splinter import Browser

def scrape():

    ### Scarpe news info from NASA website

    url_nasa = "https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest"
    response_nasa = requests.get(url_nasa)
    soup_nasa = BeautifulSoup(response_nasa.text, 'html.parser')

    news_title = soup_nasa.find('div', class_='content_title').text.strip()
    news_p = soup_nasa.find('div', class_='rollover_description_inner').text.strip()

    ### Use splinter to navigate page for featured image

    executable_path = {'executable_path': r'C:\bin\chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)

    url_jpl = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(url_jpl)
    browser.click_link_by_partial_text('FULL IMAGE')
    browser.click_link_by_partial_href('/spaceimages/details')

    html_jpl = browser.html
    soup_jpl = BeautifulSoup(html_jpl, 'html.parser')

    featured_image_url = 'https://www.jpl.nasa.gov/' + soup_jpl.find('img', class_="main_image")['src']

    ### Scrape Mars Weather twitter

    url_twtr = 'https://twitter.com/marswxreport?lang=en'
    response_twtr = requests.get(url_twtr)
    soup_twtr = BeautifulSoup(response_twtr.text, 'html.parser')

    mars_weathers = soup_twtr.find_all('p', class_="TweetTextSize")
    for tweet in mars_weathers:
        tweet.find('a').extract()
        if 'InSight sol' in tweet.text:
            mars_weather = tweet.text
            break

    ### Scrape Mars Facts

    url_fact = 'https://space-facts.com/mars/'
    tables = pd.read_html(url_fact)
    df_mars = tables[0]
    mars_facts = []
    for i in range(len(df_mars[0])):
        mars_facts.append([df_mars[0][i], df_mars[1][i]])
    mars_facts


    ### Scrape Mars Hemispheres

    url_hemi = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    response_hemi = requests.get(url_hemi)
    soup_hemi = BeautifulSoup(response_hemi.text, 'html.parser')

    # find all the titles
    results = soup_hemi.find_all('div', class_="description")
    hemisphere_image_urls = []
    info = {}
    # open url_hemi with splinter and ready to click
    browser_hemi = Browser('chrome', **executable_path, headless=False)

    for result in results:

        title = result.text
        
        browser_hemi.visit(url_hemi)
        browser_hemi.click_link_by_partial_text(title)
        html_img = browser_hemi.html
        soup_img = BeautifulSoup(html_img, 'html.parser')

        img_url = soup_img.find('li').a['href']
        
        info["title"] = title
        info["img_url"] = img_url
        
        hemisphere_image_urls.append(info)
        info = {}

    scrape_data = {
        "news_title": news_title,
        "news_p": news_p,
        "featured_img_url": featured_image_url,
        "mars_weather": mars_weather,
        "mars_facts": mars_facts,
        "hemisphere_image_urls": hemisphere_image_urls
    }

    return scrape_data

print('hello!')