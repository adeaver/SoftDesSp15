import re, operator

def readBook():
	f = open('TheWaroftheWorlds.txt', 'r')

	lines = f.readlines()
	full_text = ""

	for line in lines:
		line = re.sub("\n", " ", line)
		line = re.sub("\r", "", line)
		full_text += line

	return full_text

def getWords(text):
	edited_text = re.sub('[^\sA-Za-z0-9]', '', text)

	return edited_text.split()

def analyze_words(words):
	word_count = dict()
	for w in words:
		word_count[w.lower()] = word_count.get(w.lower(), 0) + 1

	return word_count

count_dict = analyze_words(getWords(readBook()))
sorted_dict = sorted(count_dict.items(), key=operator.itemgetter(1))
sorted_dict.reverse()

for x in range(0, 100):
	print sorted_dict[x][0] + " -- " + str(sorted_dict[x][1])