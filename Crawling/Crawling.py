#!/usr/bin/env python
# coding: utf-8

# This Jupyter Include Crawling five tables from IMDB Top 250 movies page with python libraries : beautifulsoup and html

# # **import libraries**

# In[23]:


import pandas as pd
from bs4 import BeautifulSoup
import requests 
import time
from lxml import html
from tqdm import tqdm
import lxml.etree as LE
import time
import numpy as np


# # **Get The Main page url with request library**

# In[24]:


imdb_page=requests.get('https://www.imdb.com/chart/top/?ref_=nv_mv_250')
tree = html.fromstring(imdb_page.content)
soup = BeautifulSoup(imdb_page.content, 'html.parser')


# # **save all 250 movies link in links list**

# In[25]:


links=[]
trs=soup.findAll('tr')
for tr in trs:
    td=tr.find('td')
    try:
        link=td.find('a').attrs
        link='https://www.imdb.com'+link['href']
        links.append(link)
    except AttributeError:
        pass


# # **Create first table named "MOVIE" with 6 column and 250 rows**

# In[26]:


headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.93 Safari/537.36',
           "Accept-Language": "en-US,en;q=0.5"}


# In[ ]:


movie_id=[]
titles=[]
years=[]
runtimes=[]
parental_guides=[]
canada_us=[]
for link in links:


  #movie imdb id
  id=link.split('https://www.imdb.com/title/')[1].split('tt')[1].replace('/',"")
  if id in movie_id:
      print('NOT unique Primery Key')
  else:
      movie_id.append(id)

  #get link url with request library
  page = requests.get(link, headers=headers)
  soup = BeautifulSoup(page.content, 'html.parser')
  tree = html.fromstring(page.content)
  # movie title
  title=tree.xpath('//*[@id="__next"]/main/div/section[1]/section/div[3]/section/section/div[2]/div[1]/h1/span/text()')[0]
  titles.append(title)

  #year
  year=tree.xpath('//*[@id="__next"]/main/div/section[1]/section/div[3]/section/section/div[2]/div[1]/ul/li[1]/a/text()')[0]
  years.append(year)

  #runtime
  try:
      runtime=tree.xpath('//*[@id="__next"]/main/div/section[1]/section/div[3]/section/section/div[2]/div[1]/ul/li[3]/text()')[0]
  except:
      runtime=tree.xpath('//*[@id="__next"]/main/div/section[1]/section/div[3]/section/section/div[2]/div[1]/ul/li[2]/text()')[0]

  try:
      hour=int(runtime.split('h')[0])

      try:
          runtime=hour *60 + int(runtime.split('h')[1].split('m')[0].lstrip())
          runtimes.append(runtime)
      except:
          runtime=int(runtime.split('h')[0])*60 
          runtimes.append(runtime)
             
  except:
      minutes=int(runtime.split('m')[0].lstrip())
      runtimes.append(minutes)

  #parental_guide
  try:
      parental_guide=tree.xpath('//*[@id="__next"]/main/div/section[1]/section/div[3]/section/section/div[2]/div[1]/ul/li[2]/a/text()')[0]
      parental_guides.append(parental_guide)
  except:
      parental_guide=np.nan
      parental_guides.append(parental_guide)

  #gross canada us
  box_office = soup.find_all('li',attrs={'data-testid': 'title-boxoffice-grossdomestic'})
  if box_office==[]:
      gross=np.nan
      canada_us.append(gross)
  else:
      for data in box_office:
          gross=data.find('div').find('ul').find('li').find('span').text
          gross=int(gross.replace('$','').replace(',',''))
          canada_us.append(gross)


# # Create a dataframe for Movie table

# In[ ]:


movie={}
movie['id']=movie_id
movie['title']=titles
movie['year']=years
movie['runtime']=runtimes
movie['parental_guide']=parental_guides
movie['gross_us_canada']=canada_us
movie=pd.DataFrame(data=movie)


# In[ ]:


movie['parental_guide']=movie['parental_guide'].str.replace('Not Rated','Unrated').replace(np.nan,'Unrated')


# In[ ]:


movie['gross_us_canada']=movie['gross_us_canada'].replace(np.nan,0)


# In[ ]:


movie['gross_us_canada']=movie['gross_us_canada'].astype(int)


# In[ ]:


movie['parental_guide'].unique() 


# # save as a csv file

# In[ ]:


movie.to_csv('movie.csv', index=False)


# # Table 2: person

# TWO columns that we should crawl person_id and full_name

# In[ ]:


full_names=[]
person_id=[]
for link in links:

  #get link url with request library
  page = requests.get(link, headers=headers)
  soup = BeautifulSoup(page.content, 'html.parser')
  tree = html.fromstring(page.content)
  
  #append All directors to full_name
  ul=tree.xpath('//*[@id="__next"]/main/div/section[1]/section/div[3]/section/section/div[3]/div[2]/div[1]/section/div[2]/div/ul/li[1]/div/ul/li')
  xpath='//*[@id="__next"]/main/div/section[1]/section/div[3]/section/section/div[3]/div[2]/div[1]/section/div[2]/div/ul/li[1]/div/ul/li'
  for i in range(1,len(ul)+1):
      xpath_d=xpath+str([i])+'/a/text()'
      director=tree.xpath(xpath_d)[0]
      full_names.append(director)

      href_d=xpath+str([i])+'/a/@href'
      id=tree.xpath(href_d)[0]
      id=id.split('/')[2].split('nm')[1]
      person_id.append(id)

  #append All writers
  ul=tree.xpath('//*[@id="__next"]/main/div/section[1]/section/div[3]/section/section/div[3]/div[2]/div[1]/section/div[2]/div/ul/li[2]/div/ul/li')
  xpath='//*[@id="__next"]/main/div/section[1]/section/div[3]/section/section/div[3]/div[2]/div[1]/section/div[2]/div/ul/li[2]/div/ul/li'
  for i in range(1,len(ul)+1):
      xpath_w=xpath+str([i])+'/a/text()'
      href_w=xpath+str([i])+'/a/@href'

      writer=tree.xpath(xpath_w)[0]
      full_names.append(writer)

      id=tree.xpath(href_w)[0]
      id=id.split('/')[2].split('nm')[1]
      person_id.append(id)

  # stars full_name and person id
  ul=tree.xpath('//*[@id="__next"]/main/div/section[1]/section/div[3]/section/section/div[3]/div[2]/div[1]/section/div[2]/div/ul/li[3]/div/ul/li')
  xpath='//*[@id="__next"]/main/div/section[1]/section/div[3]/section/section/div[3]/div[2]/div[1]/section/div[2]/div/ul/li[3]/div/ul/li'
  for i in range(1,len(ul)+1):
      xpath_s=xpath+str([i])+'/a/text()'
      star=tree.xpath(xpath_s)[0]
      full_names.append(star)

      id_xpath=xpath+str([i])+'/a/@href'
      id=tree.xpath(id_xpath)
      
      if id==[]:
          print('Warning')
      else:
          id=id[0].split('/')[2].split('nm')[1]
          person_id.append(id)


# In[ ]:


print(len(full_names))
print(len(person_id))


# Create a dataframe for person table

# In[ ]:


person_dict={} 
person_dict['person_id']=person_id
person_dict['name']=full_names
person=pd.DataFrame(data=person_dict)


# In[ ]:


person=person.drop_duplicates(keep='first')
person


# Save the dataframe as csv file

# In[ ]:


person.to_csv('person.csv', index=False)


# # **table 3: Cast**

# In[ ]:


import time
movie_ids=[]
person_id=[]
for link in links:

  #movie imdb id
  movie_id=link.split('https://www.imdb.com/title/')[1].split('tt')[1].replace('/',"")


  #get link url with request library
  page = requests.get(link, headers=headers)
  soup = BeautifulSoup(page.content, 'html.parser')
  tree = html.fromstring(page.content)
  # stars person id
  ul=tree.xpath('//*[@id="__next"]/main/div/section[1]/section/div[3]/section/section/div[3]/div[2]/div[1]/section/div[2]/div/ul/li[3]/div/ul/li')
  xpath='//*[@id="__next"]/main/div/section[1]/section/div[3]/section/section/div[3]/div[2]/div[1]/section/div[2]/div/ul/li[3]/div/ul/li'
  for i in range(1,len(ul)+1):
      id_xpath=xpath+str([i])+'/a/@href'
      id=tree.xpath(id_xpath)
      if id==[]:
          print('Warning')
      else:
          id=id[0].split('/')[2].split('nm')[1]
          person_id.append(id)
          movie_ids.append(movie_id)


# In[ ]:


print(len(person_id))
print(len(movie_ids))


# In[ ]:


cast_dict={}
cast_dict['person_id']=person_id
cast_dict['movie_id']=movie_ids
cast=pd.DataFrame(data=cast_dict) 


# In[ ]:


cast=cast.drop_duplicates(keep='first')
cast


# save the cast table as csv files

# In[ ]:


cast.to_csv('cast.csv', index=False)


# # Table 4: genre  

# containing two columns that should be crawl (movie_id and genre)

# In[ ]:


movie_ids=[]
genres=[]
for link in links:

  #movie imdb id
  movie_id=link.split('https://www.imdb.com/title/')[1].split('tt')[1].replace('/',"")


  #get link url with request library
  page = requests.get(link, headers=headers)
  soup = BeautifulSoup(page.content, 'html.parser')
  tree = html.fromstring(page.content)
  genre_elm=tree.xpath('//*[@id="__next"]/main/div/section[1]/section/div[3]/section/section/div[3]/div[2]/div[1]/section/div[1]/div[2]/a')
  xpath='//*[@id="__next"]/main/div/section[1]/section/div[3]/section/section/div[3]/div[2]/div[1]/section/div[1]/div[2]/a'
  if len(genre_elm)==1:
      g_xpath=xpath+'/span/text()'
      genre=tree.xpath(g_xpath)[0]
      genres.append(genre)
      movie_ids.append(movie_id)
  else:
      for i in range(1,len(genre_elm)+1):
           g_xpath=xpath+str([i])+'/span/text()'
           genre=tree.xpath(g_xpath)[0]
           genres.append(genre)
           movie_ids.append(movie_id)


# In[ ]:


print(len(genres))
print(len(movie_ids))


# In[ ]:


genre_dict={}
genre_dict['genre']=genres
genre_dict['movie_id']=movie_ids
genre=pd.DataFrame(data=genre_dict)
genre.tail(20)


# In[ ]:


genre.to_csv('genre.csv', index=False)


# # table 5: (directors and writers) 

# This table includes this columns: 
# 1. movie_id
# 2. person_id
# 3. role

# In[ ]:


movie_ids=[]
person_id=[]
roles=[]

for link in links:
  #movie imdb id
  movie_id=link.split('https://www.imdb.com/title/')[1].split('tt')[1].replace('/',"")

  #get link url with request library
  page = requests.get(link, headers=headers)
  soup = BeautifulSoup(page.content, 'html.parser')
  tree = html.fromstring(page.content)
  
  #append All directors person id and roles with movie id
  ul=tree.xpath('//*[@id="__next"]/main/div/section[1]/section/div[3]/section/section/div[3]/div[2]/div[1]/section/div[2]/div/ul/li[1]/div/ul/li')
  xpath='//*[@id="__next"]/main/div/section[1]/section/div[3]/section/section/div[3]/div[2]/div[1]/section/div[2]/div/ul/li[1]/div/ul/li'
  for i in range(1,len(ul)+1):
      href_d=xpath+str([i])+'/a/@href'
      id=tree.xpath(href_d)[0]
      id=id.split('/')[2].split('nm')[1]
      person_id.append(id)
      roles.append('Director')
      movie_ids.append(movie_id)

  #append All writers person id,role with movie id
  ul=tree.xpath('//*[@id="__next"]/main/div/section[1]/section/div[3]/section/section/div[3]/div[2]/div[1]/section/div[2]/div/ul/li[2]/div/ul/li')
  xpath='//*[@id="__next"]/main/div/section[1]/section/div[3]/section/section/div[3]/div[2]/div[1]/section/div[2]/div/ul/li[2]/div/ul/li'
  for i in range(1,len(ul)+1):
      href_w=xpath+str([i])+'/a/@href'
      id=tree.xpath(href_w)[0]
      id=id.split('/')[2].split('nm')[1]
      person_id.append(id)
      movie_ids.append(movie_id)
      roles.append('Writer')   


# Create a DataFrame with Crawled Data

# In[ ]:


crew_dict={}
crew_dict['movie_id']=movie_ids
crew_dict['person_id']=person_id
crew_dict['role']=roles
crew=pd.DataFrame(data=crew_dict)
crew


# Save the DataFrame as a CSV File

# In[ ]:


crew.to_csv('crew.csv', index=False)

