# Takes strings as input and attempts to speak them
# using HL1 vox voice files.

# Alarm sounds:
#	- deeoo
#	- doop
#	- woop
#	- bizwarn
#	- buzwarn
import sys
# from playsound import playsound
from pydub import AudioSegment
from slugify import slugify
import os
from pathlib import Path

soundpath = "static/"
filetype = ".mp3"
combined_path = "static/cache/"

comma = "_comma"
period = "_period"
ing = "ing"


# Takes sentence and seperates into individual words
# converts commas and periods into their respective word
def convert_sentence(sentence):
	words = sentence.split()
	gen_output = []
	sent_output = []

	for word in words:
		if word[-1:] == "," and check_available(word[:-1]):
			gen_output.append(word[:-1])
			gen_output.append(comma)
			sent_output.append(word)
		elif word[-1:] == "." and check_available(word[:-1]):
			gen_output.append(word[:-1])
			gen_output.append(period)
			sent_output.append(word)
		elif check_available(word):
			gen_output.append(word)
			sent_output.append(word)
	return {'generate': gen_output, 'sentence': str.join(" ", sent_output)}


def check_available(word):
	return os.path.isfile(soundpath + word + filetype)


# # Play sentence
# def playwords(sentence):
#     words = convertsentence(sentence)
#     for word in words:
#         play(word)


# # Wrapper to add path and filetype
# def play(word):
#     playsound(soundpath + word + filetype)


# Save sentence as an mp3 with the final text included
def savetomp3(sentence):
	converted = convert_sentence(sentence)
	print(converted)
	sentence = " ".join(converted['generate'])
	if os.path.isfile(combined_path + slugify(sentence) + ".mp3"):
		print("Sentence already in cache, not re-creating")
		path = combined_path + slugify(sentence) + ".mp3"
	elif os.path.isfile(soundpath + slugify(sentence) + ".mp3"):
		print("Sentence is a static word, not adding to cache")
		path = soundpath + slugify(sentence) + ".mp3"
	else:
		words = converted['generate']
		playlist = AudioSegment.silent(duration=500)
		for word in words:
			if not os.path.isfile(soundpath + word + filetype):
				print(word + " does not exist, skipping")
				sentence = sentence.replace(word, '')
			else:
				word_mp3 = AudioSegment.from_mp3(soundpath + word + filetype)
				playlist = playlist.append(word_mp3)
				playlist = playlist.append(AudioSegment.silent(duration=300))
		if not playlist:
			print("Cannot say any of the sentence")
			path = None
		else:
			playlist.export(combined_path + slugify(sentence) + ".mp3", format="mp3", bitrate="100k")
			path = combined_path + slugify(sentence) + ".mp3"
	return {'path': path, 'sentence': converted['sentence']}


def getcachedsentences():
	return os.listdir(combined_path)
