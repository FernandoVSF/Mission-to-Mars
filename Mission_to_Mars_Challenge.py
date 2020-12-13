# Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd


# Set the executable path and initialize the chrome browser in splinter
executable_path = {'executable_path': 'C:\\Users\\ferna\\.wdm\\drivers\\chromedriver\\win32\\87.0.4280.88\\chromedriver.exe'}
browser = Browser('chrome', **executable_path)


# ### Visit the NASA Mars News Site

# Visit the mars nasa news site
url = 'https://mars.nasa.gov/news/'
browser.visit(url)

# Optional delay for loading the page
browser.is_element_present_by_css("ul.item_list li.slide", wait_time=1)


# In[4]:


# Convert the browser html to a soup object and then quit the browser
html = browser.html
news_soup = soup(html, 'html.parser')

slide_elem = news_soup.select_one('ul.item_list li.slide')


# In[5]:


slide_elem.find("div", class_='content_title')


# In[6]:


# Use the parent element to find the first a tag and save it as `news_title`
news_title = slide_elem.find("div", class_='content_title').get_text()
news_title


# In[7]:


slide_elem.find("div", class_='content_title')


# In[8]:


# Use the parent element to find the paragraph text
news_p = slide_elem.find('div', class_="article_teaser_body").get_text()
news_p


# ### JPL Space Images Featured Image

# In[9]:


# Visit URL
url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
browser.visit(url)


# In[10]:


browser


# In[11]:


# Find and click the full image button
full_image_elem = browser.find_by_id('full_image')
full_image_elem.click()


# In[12]:


full_image_elem


# In[13]:


# Find the more info button and click that
browser.is_element_present_by_text('more info', wait_time=1)
more_info_elem = browser.links.find_by_partial_text('more info')
more_info_elem.click()


# In[14]:


more_info_elem


# In[15]:


# Parse the resulting html with soup
html = browser.html
img_soup = soup(html, 'html.parser')


# In[16]:


# find the relative image url
img_url_rel = img_soup.select_one('figure.lede a img').get("src")
img_url_rel


# In[17]:


# Use the base url to create an absolute url
img_url = f'https://www.jpl.nasa.gov{img_url_rel}'
img_url


# ### Mars Facts

# In[18]:


df = pd.read_html('http://space-facts.com/mars/')[0]

df.head()


# In[19]:


df.columns=['Description', 'Mars']
df.set_index('Description', inplace=True)
df


# In[20]:


df.to_html()


# ### Mars Weather

# In[21]:


# Visit the weather website
url = 'https://mars.nasa.gov/insight/weather/'
browser.visit(url)


# In[22]:


# Parse the data
html = browser.html
weather_soup = soup(html, 'html.parser')


# In[23]:


# Scrape the Daily Weather Report table
weather_table = weather_soup.find('table', class_='mb_table')
print(weather_table.prettify())


# # D1: Scrape High-Resolution Mars’ Hemisphere Images and Titles

# ### Hemispheres

# In[101]:


# 1. Use browser to visit the URL 
url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
browser.visit(url)
browser.is_element_present_by_css("ul.item_list li.slide", wait_time=1)


# In[102]:


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
    hemisphere = {"image_url":full_image_elem, "title":full_image_title}
    hemisphere_image_urls.append(hemisphere)


# In[103]:


# 4. Print the list that holds the dictionary of each image url and title.
hemisphere_image_urls


# In[104]:


# 5. Quit the browser
browser.quit()


# In[ ]:





# In[ ]:




