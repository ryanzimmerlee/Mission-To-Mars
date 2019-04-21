# Import Dependencies
from bs4 import BeautifulSoup as bs
from splinter import Browser
import requests
import pandas as pd
# from urllib.parse import urlsplit

def init_browser():
    executable_path = {"executable_path":"chromedriver.exe"}
    browser = Browser("chrome", **executable_path)
    return browser

def scrape():
    # Create blank dictionary
    marsInfoDict = {}

    # Initialize browser
    browser = init_browser()
    html = browser.html
    soup = bs(html,"html.parser")

    ######## NASA Mars News ######## 
    url = "https://mars.nasa.gov/news/"
    response = requests.get(url)
    soup = bs(response.text, 'html.parser')
    first_title = soup.find(class_="content_title").text.strip()
    first_para = soup.find(class_="rollover_description_inner").text.strip()

    # Store in the dictionary
    marsInfoDict['LatestNewsTitle'] = first_title
    marsInfoDict['LatestNewsParagraph'] = first_para

    ######## JPL Mars Space Images ########
    url_jpl = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    response2 = requests.get(url_jpl)
    soup = bs(response2.text, 'html.parser')
    footer = soup.find(class_="button fancybox")
    feature_img = footer["data-fancybox-href"]
    featured_image_url = "https://www.jpl.nasa.gov" + feature_img

    # Store in the dictionary
    marsInfoDict['JPLMarsFeaturedImage'] = featured_image_url

    ######## Mars Weather ########
    twitter_url = "https://twitter.com/marswxreport?lang=en"
    response3 = requests.get(twitter_url)
    soup = bs(response3.text, 'html.parser')
    first_tweet = soup.find(class_="TweetTextSize TweetTextSize--normal js-tweet-text tweet-text").text.strip()
    
    # Store in the dictionary
    marsInfoDict['CurrentMarsWeather'] = first_tweet

    ######## Mars Facts ########
    marsfacts_url = "https://space-facts.com/mars/"
    mars_tables = pd.read_html(marsfacts_url)
    marsfacts_df = mars_tables[0]
    marsfacts_renamed = marsfacts_df.rename(columns={0:"Type",1:"Info"})
    marsfacts_renamed.set_index("Type",inplace=True)
    marsfacts_html = marsfacts_renamed.to_html()
    marsfacts_html = marsfacts_html.replace("\n", "")

    # Store in the dictionary
    marsInfoDict['MarsFactsHTML'] = marsfacts_html

    ######## Mars Hemispheres ########
    hemisphere_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    # hemisphere_base_url = "{0.scheme}://{0.netloc}/".format(urlsplit(hemisphere_url))
    hemisphere_base_url = "https://astrogeology.usgs.gov/"
    browser.visit(hemisphere_url)
    list_of_products = soup.find('div', class_='collapsible results')
    products = list_of_products.find_all(class_='item') 

    # Create empty list to store the urls that need to be visited to find the large image links
    product_url_list = []

    # For loop
    for product in products:
        href_url = product.find('a')['href']
        product_url_list.append(href_url[1:])
    smallSizeImage_url_list = [hemisphere_base_url + url for url in product_url_list]

    # Create empty list to store the dictionary items containing each large image url and image title
    wide_image_url_list = []

    # For loop
    for url in smallSizeImage_url_list:
        browser.visit(url)
        img_html = browser.html
        soup = bs(img_html, 'html.parser')
        image_div = soup.find('div', class_='wide-image-wrapper ')
        image_pic = image_div.find('img', class_='wide-image')['src']
        text_div = soup.find('div', class_='content')
        text_title = text_div.find('h2', class_='title')
        dictItem = {"Title":text_title, "Image URL":hemisphere_base_url + image_pic[1:]}
        wide_image_url_list.append(dictItem)

    # Store list of dictionary items in the dictionary
    marsInfoDict['MarsHemispheresLrgImgsList'] = wide_image_url_list

    return marsInfoDict