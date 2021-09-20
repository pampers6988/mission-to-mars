#!/usr/bin/env python
# coding: utf-8

# In[1]:


# Import Splinter, BeautifulSoup, and Pandas
from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd
from webdriver_manager.chrome import ChromeDriverManager


# In[2]:


# Set the executable path and initialize Splinter
executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path)


# ### Visit the NASA Mars News Site

# In[3]:


# Visit the mars nasa news site
url = 'https://redplanetscience.com/'
browser.visit(url)

# Optional delay for loading the page
browser.is_element_present_by_css('div.list_text', wait_time=1)


# In[4]:


# Convert the browser html to a soup object and then quit the browser
html = browser.html
news_soup = soup(html, 'html.parser')

slide_elem = news_soup.select_one('div.list_text')


# In[5]:


slide_elem.find('div', class_='content_title')


# In[6]:


# Use the parent element to find the first a tag and save it as `news_title`
news_title = slide_elem.find('div', class_='content_title').get_text()
news_title


# In[7]:


# Use the parent element to find the paragraph text
news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
news_p


# ### JPL Space Images Featured Image

# In[8]:


# Visit URL
url = 'https://spaceimages-mars.com'
browser.visit(url)


# In[9]:


# Find and click the full image button
full_image_elem = browser.find_by_tag('button')[1]
full_image_elem.click()


# In[10]:


# Parse the resulting html with soup
html = browser.html
img_soup = soup(html, 'html.parser')
img_soup


# In[11]:


# find the relative image url
img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
img_url_rel


# In[12]:


# Use the base url to create an absolute url
img_url = f'https://spaceimages-mars.com/{img_url_rel}'
img_url


# ### Mars Facts

# In[13]:


df = pd.read_html('https://galaxyfacts-mars.com')[0]
df.head()


# In[14]:


df.columns=['Description', 'Mars', 'Earth']
df.set_index('Description', inplace=True)
df


# In[15]:


df.to_html()


# # D1: Scrape High-Resolution Mars’ Hemisphere Images and Titles

# ### Hemispheres

# In[16]:


# 1. Use browser to visit the URL 
url = 'https://marshemispheres.com/'
browser.visit(url)


# In[18]:


# Parse the resulting html with soup
html = browser.html
link_soup = soup(html, 'html.parser')
type(link_soup)


# In[19]:


link = link_soup.find('a', class_='itemLink product-item')['href']
link


# In[20]:


image_url = f'https://marshemispheres.com/{link}'
image_url


# In[24]:


# 2. Create a list to hold the images and titles.
image_urls = []

# 3. Write code to retrieve the image urls and titles for each hemisphere.
results = link_soup.find_all('div', class_ = 'item')
for result in results:
    # Retreive image urls
    link = result.find('a', class_='itemLink product-item')['href']
   
    # Create image url by appending to the base url
    image_url = f'https://marshemispheres.com/{link}'
    image_urls.append(image_url)
    
    print('--------------------------------------------------------')
    print(image_url)


# In[23]:


# 4. Print the list that holds the dictionary of each image url and title.
image_urls


# In[25]:


import time
# 2b. Create a list to hold the images and titles.Step 2
hemisphere_image_urls = []

for url in image_urls:
    hemispheres = {}
    # Visit the url using browser
    browser.visit(url)
    # Click on toggle open button
    button = browser.find_by_id("wide-image-toggle")
    button.click()
    # Time lapse
    time.sleep(1)
    # Parse the resulting html with soup
    html = browser.html
    img_soup = soup(html, 'html.parser')
    
    # 3. Write code to retrieve the image urls and titles for each hemisphere.
    # Retreiving titles
    title = img_soup.find('h2', class_= "title").text
    hemispheres["title"]= title
   
    # Retreiving rel image url
    rel_img = img_soup.find('img',class_= "wide-image").get('src')
    img_url = f'https://marshemispheres.com/{rel_img}'
    hemispheres["img_url"]= img_url
    hemisphere_image_urls.append(hemispheres)
    browser.back()
    
    print('------------------------------------------------------------------------------------------------------')
    print(title)
    print(img_url)


# In[26]:



# 4. Print the list that holds the dictionary of each image url and title.
print(hemisphere_image_urls)


# In[27]:


from IPython.display import Image
from IPython.core.display import HTML 
Image(url= 'https://marshemispheres.com/images/f5e372a36edfa389625da6d0cc25d905_cerberus_enhanced.tif_full.jpg')


# In[28]:


Image(url= 'https://marshemispheres.com/images/3778f7b43bbbc89d6e3cfabb3613ba93_schiaparelli_enhanced.tif_full.jpg')


# In[29]:


Image(url= 'https://marshemispheres.com/images/555e6403a6ddd7ba16ddb0e471cadcf7_syrtis_major_enhanced.tif_full.jpg')


# In[30]:


Image(url= 'https://marshemispheres.com/images/b3c7c6c9138f57b4756be9b9c43e3a48_valles_marineris_enhanced.tif_full.jpg')


# In[ ]:


# 5. Quit the browser
browser.quit()

