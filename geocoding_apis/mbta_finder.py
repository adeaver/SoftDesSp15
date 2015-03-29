"""
Geocoding and Web APIs Project Toolbox exercise

Find the MBTA stops closest to a given location.

Full instructions are at:
https://sites.google.com/site/sd15spring/home/project-toolbox/geocoding-and-web-apis
"""

import urllib   # urlencode function
import urllib2  # urlopen function (better than urllib version)
import json
import re


# Useful URLs (you need to add the appropriate parameters for your requests)
GMAPS_BASE_URL = "https://maps.googleapis.com/maps/api/geocode/json"
MBTA_BASE_URL = "http://realtime.mbta.com/developer/api/v2/stopsbylocation"
MBTA_DEMO_API_KEY = "wX9NwuHnZU2ToO7GmGR9uw"


# A little bit of scaffolding if you want to use it

def get_json(url):
    """
    Given a properly formatted URL for a JSON web API request, return
    a Python JSON object containing the response to that request.
    """
    formaturl = re.sub(" ", "%20", url)
    f = urllib2.urlopen(formaturl)
    response_text = f.read()
    response_data = json.loads(response_text)
    return response_data


def get_lat_long(place_name):
    """
    Given a place name or address, return a (latitude, longitude) tuple
    with the coordinates of the given place.

    See https://developers.google.com/maps/documentation/geocoding/
    for Google Maps Geocode API URL formatting requirements.
    """
    url = GMAPS_BASE_URL + "?address=" + place_name
    request_json = get_json(url)

    info = request_json["results"]

    if(len(info) > 0):
        lat_long_json = info[0]["geometry"]["location"]
        latitude = lat_long_json["lat"]
        longitude = lat_long_json["lng"]
    else:
        latitude = "0"
        longitude = "0"

    return [str(latitude), str(longitude)]

def get_nearest_station(latitude, longitude):
    """
    Given latitude and longitude strings, return a (station_name, distance)
    tuple for the nearest MBTA station to the given coordinates.

    See http://realtime.mbta.com/Portal/Home/Documents for URL
    formatting requirements for the 'stopsbylocation' API.
    """
    url = MBTA_BASE_URL + "?api_key=" + MBTA_DEMO_API_KEY + "&lat=" + latitude + "&lon=" + longitude + "&format=json"
    request_json = get_json(url)

    stops_list = request_json['stop']

    if(len(stops_list) > 0):
        train_stop = stops_list[0]
        return (train_stop['stop_name'], train_stop['distance'])

    return ()


def find_stop_near(place_name):
    """
    Given a place name or address, print the nearest MBTA stop and the 
    distance from the given place to that stop.
    """
    latlong = get_lat_long(place_name)
    nearstop = get_nearest_station(latlong[0], latlong[1])

    if(len(nearstop) > 0):
        print nearstop[0] + " is the closest stop to " + place_name + " (" + nearstop[1] + " miles)"
    else:
        print "There is no stop near " + place_name + " or " + place_name + " was not found."

start = "a"

while True:
    start = raw_input("Where would you like to find a stop near? (Enter nothing to quit) ")
    if start == "":
        break
    find_stop_near(start)