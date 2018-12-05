# plotting tools
import Tkinter as tk
from matplotlib import pyplot,transforms
import matplotlib.pyplot as plt
import numpy as np
# grabbing data from API
import json, ast
import requests
# Gtk + GUI builder
import sys
import os
import gi
import re
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk





def toCelcius(fahrenheit):
    '''
    Convert a fahrenheit value into celcius
    '''
    celsius = (fahrenheit - 32) * 5.0/9.0
    return celsius
   
# text format functions # source : https://www.quora.com/How-can-I-make-this-sentence-in-python-multiple-lines
#SENTENCE_REGEX = re.compile('[^!,?\.]+[!,?\.]') 
 
def parse_sentences(text):
	"""
	Split a text block into a list of sentences.
 
	:input text: String
	:return: List Sentences of text as strings.
	"""
        words = text.split()
        new_text = ""
        word_count = 0
        for word in words:
            new_text += word + " "
            word_count += 1
            if word_count == 4 or "." in word:
                new_text += "\n"
                word_count = 0    
	return new_text #[x.lstrip() for x in SENTENCE_REGEX.findall(text)]
 
 
def join_sentences(sentences):
	"""
	Print sentences in script-fashion with new lines between.
	
	:input sentences: List (of) Strings to be output
	"""
	return '\n\n'.join(sentences)


def set_location(country):
   # only returns for Nigeria or the United Kingdom, 
   # could not find a list of all countries and locations as a dictionary,
   # so I settled for demonstrating with two options
   '''
   Set the Latitude and Longitude of the country
   '''
   countryDict = {'Nigeria':[9.081999, 8.675277],
                  'NGA':[9.081999, 8.675277],
                  'United Kingdom': [55.378051, -3.435973],
                  'UK': [55.378051, -3.435973],
                  }
   print(country+" : ")
   print(countryDict[country])
   return  countryDict[country]

def DarkSky_URL(location):
    '''
    Return the url to be used for the API call
    '''
    key = '<INSERT YOUR KEY HERE>'
    longitude = location[1]
    latitude = location[0]
    url = 'https://api.darksky.net/forecast/' + key +'/' + str(latitude) + ','+ str(longitude)
    print(requests.get(url))
    return url

def data_fetch(DarkSky_URL):
    '''
    Calls the API with the url, fetches the JSON and converts to a dictionary
    '''
    url = requests.get(DarkSky_URL)
    url_json = url.json()
    data = ast.literal_eval(json.dumps(url_json)) # returns a dictionary :>> print type( output ) : <class : dict>
    url.close()
    return data

def get_weather(data):
        '''
        Filters weather info from the data provided
        '''
        daily_summary = ''
        daily_icon = ''
        timezone = ''
        for k, v in data['daily'].items(): # only interested in the daily forecast
            
            if k == 'icon':
                daily_icon = v
            if k == 'summary':
                daily_summary = v
        #  print(k, v)

        for k,v in data.items():
            if k == 'timezone':
                timezone = v

        print(timezone)
        print(daily_summary)
        print(daily_icon)
        return [timezone,daily_summary,daily_icon]

def display_weather(entry1):
    '''
    Displays weather info from the data provided
    '''
    location = set_location(entry1.get_text())
    url = DarkSky_URL(location)
    data = data_fetch(url)
    weather = get_weather(data)
    
    zone = builder.get_object("zone_value")
    summary = builder.get_object("summary_value")

    # parsing sentences
    weather_summary = parse_sentences(weather[1])
    #
    zone.set_text(weather[0])
    summary.set_text(weather_summary)
    
def weather_chart(entry2):
    '''
    Further filters the data provided and,
    creates a graph image to display
    '''
    location = set_location(entry2.get_text())
    url = DarkSky_URL(location)
    data = data_fetch(url)

    # data extraction
    group_data=[]
    for dict in data['hourly']['data']:
        if 'temperature' in dict:
            group_data.append(toCelcius(dict['temperature']))
    
    # chart plotting
    # group_data = toCelcius(group_data)
    # just removing the last item since there are 49 objects in the hourly feed
    group_data.remove(group_data[48])
    group_names =  [i for i in range(48)]
    # print group_names
    fig, ax = plt.subplots(figsize=(5,3))

    # first of all, the base transformation of the data points is needed
    base = pyplot.gca().transData 
    rot = transforms.Affine2D().rotate_deg(90)
    ax.barh(group_names, group_data,  transform= rot + base)    
    # chart saving
    plt.savefig('weatherplot.png', bbox_inches='tight')
    # image setting
    plot = builder.get_object("graph")
    plot.set_from_file("weatherplot.png")




# GUI #####################
builder = Gtk.Builder()
builder.add_from_file("interface.glade")

header = Gtk.HeaderBar(title="Weather App")
header.set_subtitle("Technical Interview :MoonSot_CVE")
header.props.show_close_button = True

handlers = {
    "on_button1_clicked": display_weather,
    "on_button2_clicked": weather_chart
}
builder.connect_signals(handlers)


window = builder.get_object("window1")
window.connect("delete-event", Gtk.main_quit)
window.show_all()

Gtk.main()