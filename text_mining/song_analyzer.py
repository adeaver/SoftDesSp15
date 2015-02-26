from pattern.web import *
from pattern.en import *
import xml.etree.ElementTree as ET
import random, re, os

def get_friends(user, ulist, depth):
	"""
	Gets a list of friends starting at one friend and getting all of their friends and all of their friends etc
	"""

	if(depth > 0):
		url = "http://ws.audioscrobbler.com/2.0/?method=user.getfriends&user=" + user + "&api_key=ef2bd13225a0b04c4dd5c000f548ab0c"
		friends_data = []
		friend = []
		
		try:
			friends	= URL(url).download()
		except URLTimeout:
			friends = ""
		
		doc = ET.fromstring(friends)

		for child in doc:
			for users in child:
				for user_info in users:
					if(user_info.tag == "name" or user_info.tag == "country"):
						friend.append(user_info.text)
					if(user_info.tag == "name" and user_info.tag in ulist):
						friend = []
						break
					if(user_info.tag == "country" and user_info.text == None):
						friend = []
						break
				if(len(friend) > 0):
					friends_data.append(friend)
					friend = []

		for x in friends_data:
			if(len(friends_data) > 10000):
				break
			friends_data += get_friends(x[0], friends_data, depth-1)

		return friends_data
	return []

def get_songs(user):
	"""
	gets a users recent tracks
	"""

	songs_url = "http://ws.audioscrobbler.com/2.0/?method=user.getrecenttracks&user=" + user + "&api_key=ef2bd13225a0b04c4dd5c000f548ab0c"
	songs = URL(songs_url).download()

	doc = ET.fromstring(songs)

	tracks = []

	artist = ""
	track = ""
	album = ""

	for child in doc:
		for children in child:
			for track_info in children:
				if(track_info.tag == "artist"):
					artist = track_info.text
				elif(track_info.tag == "name"):
					track = track_info.text
				elif(track_info.tag == "album"):
					album = track_info.text
			tracks.append([artist, track, album])

	return tracks

def save_user_data(users):
	"""
	Writes user data to a text file so that it can be accessed later without accessing the internet
	"""

	fout = open("user_data.txt", "w")

	for user in users:
		fout.write(user[0] + "/" + user[1] + "\n")

	fout.close()

def unpack_user_data():
	"""
	Reads the user data
	"""

	fin = open("user_data.txt", "r")

	lines = fin.readlines()
	data = []

	for line in lines:
		user = line.split("/")
		name = re.sub("\n", "", user[0])
		country = re.sub("\n", "", user[1])
		data.append([name, country])

	fin.close()

	return data

def song_data(users):
	"""
	Gets every user's listening history and organizes it by country
	"""

	song_frequency = {}
	counter = 0.0

	for user in users:
		counter += 1.0
		os.system("clear")
		print "Fetching data: " + str(counter/len(users)*100) + "%"
		country_frequency = song_frequency.get(user[1], {})
		try:
			recent_tracks = get_songs(user[0])

			for track in recent_tracks:
				song = track[1] + " by " + track[0]
				freq = country_frequency.get(song, 0)+1
				country_frequency[song] = freq

			song_frequency[user[1]] = country_frequency
		except:
			continue

	return song_frequency

def pack_song_data(dictionary):
	"""
	Packs information about frequency into an xml file so that the internet does not need to be accessed
	"""

	fout = open("song_data.xml", "w")

	fout.write('<?xml version="1.0" encoding="utf-8"?>\n')

	fout.write("<data>\n")

	for entry in dictionary:
		fout.write("\t<country name = '" + entry + "'>\n")
		for element in dictionary[entry]:
			try:
				fout.write("\t\t<song>\n")
				fout.write("\t\t\t<title>" + re.sub('[^A-Za-z0-9\s]', '', element) + "</title>\n")
				fout.write("\t\t\t<frequency>" + str(dictionary[entry][element]) + "</frequency>\n")
				fout.write("\t\t</song>\n")
			except:
				continue
		fout.write("\t</country>\n")

	fout.write("</data>")
	fout.close()

def unpack_song_data():
	"""
	Reads the xml file about song frequency
	"""
	fin = open("song_data.xml", "r")

	freq_dictionary = {}
	current_country = ""
	current_data = []
	data_string = ''.join(fin.readlines())
	doc = ET.fromstring(data_string)

	for child in doc:
		current_country = child.attrib['name']
		for songs in child:
			for elements in songs:
				current_data.append(elements.text)
				if(len(current_data) == 2):
					song = current_data[0]
					freq = int(current_data[1])
					current = freq_dictionary.get(current_country, ['', 0])

					if(freq > current[1]):
						freq_dictionary[current_country] = [song, freq]

					current_data = []

	fin.close()
	return freq_dictionary

def unique_info(ulist):
	new_ulist = []
	usernames = []

	for user in ulist:
		if(user[0] not in usernames):
			usernames.append(user[0])
			new_ulist.append(user)

	return new_ulist

user = "My_Sharona" # Base user (this user was selected because they have a lot of friends)

# os.system("clear")
# print "Collecting Data..."
# users = get_friends(user, [], 2)

# os.system("clear")
# print "Saving User Data..."
# save_user_data(users)

os.system("clear")
print "Unpacking User Data"
user_data = unique_info(unpack_user_data())

country_count = {}

for user in user_data:
	country_count[user[1]] = country_count.get(user[1], 0)+1

for country in country_count:
	print country + " -- " + str(country_count[country])

os.system("clear")
print "Getting song data"
frequency_data = song_data(user_data)

os.system("clear")
print "Packing data into XML"
pack_song_data(frequency_data)

os.system("clear")
print "Unpacking XML Data"
frequency_data = unpack_song_data()

os.system("clear")
print "Final Frequency Data:"
for key in frequency_data:
	print key + " -- " + frequency_data[key][0]