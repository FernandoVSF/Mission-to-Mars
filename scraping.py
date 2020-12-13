# Import Splinter, BeautifulSoup, and Pandas
from splinter import Browser
from bs4 import BeautifulSoup as soup   
import pandas as pd
import datetime as dt


def scrape_all():
    # Initiate headless driver for deployment
    browser = Browser("chrome", executable_path="C:\\Users\\ferna\\.wdm\\drivers\\chromedriver\\win32\\87.0.4280.88\\chromedriver.exe", headless=True)

    news_title, news_paragraph = mars_news(browser)

    # Run all scraping functions and store results in a dictionary
    data = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image": featured_image(browser),
        "facts": mars_facts(),
        "last_modified": dt.datetime.now(),
        "hems_dict": hems_img(browser)
    }

    # Stop wehbdriver and return data
    browser.quit()
    return data


def mars_news(browser):

    # Scrape Mars News
    # Visit the mars nasa news site
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)

    # Optional delay for loading the page
    browser.is_element_present_by_css("ul.item_list li.slide", wait_time=1)

    # Convert the browser html to a soup object and then quit the browser
    html = browser.html
    news_soup = soup(html, 'html.parser')

    # Add try/except for error handling
    try:
        slide_elem = news_soup.select_one("ul.item_list li.slide")
        # Use the parent element to find the first 'a' tag and save it as 'news_title'
        news_title = slide_elem.find("div", class_="content_title").get_text()
        # Use the parent element to find the paragraph text
        news_p = slide_elem.find("div", class_="article_teaser_body").get_text()

    except AttributeError:
        return None, None

    return news_title, news_p


def featured_image(browser):
    # Visit URL
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)

    # Find and click the full image button
    full_image_elem = browser.find_by_id('full_image')[0]
    full_image_elem.click()

    # Find the more info button and click that
    browser.is_element_present_by_text('more info', wait_time=1)
    more_info_elem = browser.links.find_by_partial_text('more info')
    more_info_elem.click()

    # Parse the resulting html with soup
    html = browser.html
    img_soup = soup(html, 'html.parser')

    # Add try/except for error handling
    try:
        # Find the relative image url
        img_url_rel = img_soup.select_one('figure.lede a img').get("src")

    except AttributeError:
        return None

    # Use the base url to create an absolute url
    img_url = f'https://www.jpl.nasa.gov{img_url_rel}'

    return img_url

def mars_facts():
    # Add try/except for error handling
    try:
        # Use 'read_html' to scrape the facts table into a dataframe
        df = pd.read_html('http://space-facts.com/mars/')[0]

    except BaseException:
        return None

    # Assign columns and set index of dataframe
    df.columns=['Description', 'Mars']
    df.set_index('Description', inplace=True)

    # Convert dataframe into HTML format, add bootstrap
    return df.to_html(classes="table table-striped")

if __name__ == "__main__":

    # If running as script, print scraped data
    print(scrape_all())
    

def hems_img(browser):

    # 1. Use browser to visit the URL 
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)
    browser.is_element_present_by_css("ul.item_list li.slide", wait_time=1)


    # 2. Create a list to hold the images and titles.
    hemisphere_image_urls = []

    # 3. Write code to retrieve the image urls and titles for each hemisphere.
    html = browser.html
    html_soup = soup(html, 'html.parser')
    hems = html_soup.find_all('div', class_='item')
    for hem in hems:
        hemispheres = {}
        url_tag = hem.find('a', class_='itemLink product-item')
        url = url_tag.get('href')
        url_string = f'https://astrogeology.usgs.gov{url}'
        hem_html = browser.visit(url_string)
        browser.is_element_present_by_css("ul.item_list li.slide", wait_time=1)
        hem_html = browser.html
        hem_soup = soup(hem_html, 'html.parser')
        full_image_elem = hem_soup.find('div', class_ = 'wide-image-wrapper').find('a').get('href')
        full_image_title = hem_soup.find('div', class_ = 'content').find('h2').text
        hemispheres = {"image_url":full_image_elem, "title":full_image_title}
        hemisphere_image_urls.append(hemispheres)


    # 4. Print the list that holds the dictionary of each image url and title.
    return hemisphere_image_urls
