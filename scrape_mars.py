from splinter import Browser
from bs4 import BeautifulSoup as bs
import requests
import pandas as pd


def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    #executable_path = {"executable_path": "/Users/andra/Documents/PREWORK_AM/10-Web Scraping and Mongo Homework/chromedriver.exe"}
    return Browser("chrome", headless=False)


def scrape_info():
    browser = init_browser()

    #Nasa Mars News scrape
    url = "https://mars.nasa.gov/news/"
    browser.visit(url)

    html = browser.html
    soup = bs(html,"html.parser")

    title = soup.find('div', class_='content_title').text.strip()
    teaser = soup.find('div', class_="article_teaser_body").text

   #JPL Mars Space Images - Featured Image
    image_url_featured = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(image_url_featured)

    html_image = browser.html
    soup = bs(html_image,"html.parser")

    featured_image_url  = soup.find('article')['style'].replace('background-image: url(','').replace(');', '')[1:-1]
    main_url = 'https://www.jpl.nasa.gov'
    featured_image_url = main_url + featured_image_url

    #Mars Weather
    weather_url ='https://twitter.com/marswxreport?lang=en'
    browser.visit(weather_url)

    html_weather = browser.html
    soup = bs(html_weather, 'html.parser')

    mars_weather = soup.find('p', class_='TweetTextSize TweetTextSize--normal js-tweet-text tweet-text').text
    

    #Mars Facts
    facts_url = 'http://space-facts.com/mars/'

    tables = pd.read_html(facts_url)   

    mars_facts = tables[0]
    mars_facts.columns = ["Description", "Values"]
    mars_facts.set_index(["Description"])
    html_table = mars_facts.to_html()
    html_table.replace('\n', '')

    # Mars_Hemispheres - commented
    hemisphere_image_urls = [
        'https://astrogeology.usgs.gov/search/map/Mars/Viking/valles_marineris_enhanced',
        'https://astrogeology.usgs.gov/search/map/Mars/Viking/cerberus_enhanced',
        'https://astrogeology.usgs.gov/search/map/Mars/Viking/schiaparelli_enhanced',
        'https://astrogeology.usgs.gov/search/map/Mars/Viking/syrtis_major_enhanced'
    ]

    img_data = []
    for data in hemisphere_image_urls:
        browser.visit(data)
        html_hemisphere = browser.html
        soup = bs(html_hemisphere, 'html.parser')
        img = soup.find('div', id='wide-image').find('img', class_='wide-image')['src']
        img_url = 'https://astrogeology.usgs.gov' + img
        title = soup.find('title').text.split()[0]
        dicts = {'title': title, 'img_url': img_url}
        img_data.append(dicts)

    mars_data = {
        "img_data":img_data,
        "html_table":html_table,
        "mars_weather":mars_weather,
        "featured_image_url":featured_image_url,
        "teaser": teaser,
        "title":title
    }

    browser.quit()
    return (mars_data)

if __name__ == "__main__":
    scrape_info()












