#!/usr/bin/env python


from __future__ import print_function
from future.standard_library import install_aliases
install_aliases()

from urllib.request import urlopen 


import json
import unicodedata
import datetime

movie = "fight club"
character = "The narrator"


#replace all spaces with +
sMovie,x,y = ""," ","+"
for char in movie:
    sMovie += y if char == x else char

#create search url with specific movie    
baseurl = "https://api.themoviedb.org/3/search/movie?api_key=9fe2fdf8fcbeeb11ecec17e5e4f0276a&query=" + sMovie

#Grab ID from specific movie
result = urlopen(baseurl).read()
data = json.loads(result) 
movieID = data['results'][0]['id']

#Use ID for new URL with movie details
idurl = "https://api.themoviedb.org/3/movie/" + str(movieID) + "?api_key=9fe2fdf8fcbeeb11ecec17e5e4f0276a"
result = urlopen(idurl).read()
data = json.loads(result)


creditsurl = "https://api.themoviedb.org/3/movie/" + str(movieID) + "/credits?api_key=9fe2fdf8fcbeeb11ecec17e5e4f0276a"
creditsResult = urlopen(creditsurl).read()
creditsData = json.loads(creditsResult)

#Getting fields from credit data
crew = creditsData.get('crew')
for d in crew:
   for key in d:
       if d[key] == 'Director':
          director = d.get('name')

#Main cast
castNames= []
cast = creditsData.get('cast')
count=0
for d in cast:
#     gets rid of accents in characters which throws error
      name = unicodedata.normalize('NFD', d.get("name")).encode('ascii', 'ignore')
      castNames.append(name)
      count+=1
      if(count >= 4): #only grabs first four cast names (main cast)
          break
castNames =  '{} and {}'.format(', '.join(castNames[:-1]), castNames[-1])

#Identify actor of character

for d in cast:
    for key in d:
        if d[key] == character.title():    
            actor = d.get('name')
            print(actor)

#Getting fields from JSON data
title = data.get('title')
budget = format(data.get('budget'),",d")
date = data.get('release_date')
date = datetime.datetime.strptime(date, '%Y-%m-%d').strftime('%m/%d/%Y')
revenue = format(data.get('revenue'), ",d")
#runtime = '{:02d}:{:02d}'.format(*divmod(data.get('runtime'), 60))
runtime = '{:d} hours and {:d} minutes'.format(*divmod(data.get('runtime'), 60))
#print(title + budget + runtime)
