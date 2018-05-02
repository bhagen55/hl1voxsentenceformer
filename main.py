# Takes strings as input and attempts to speak them
# using HL1 vox voice files.
import sys
from playsound import playsound

soundpath = "vox/"
filetype = ".wav"
comma = "_comma"
period = "_period"


# Takes a string and forms it into filepaths of sounds
def saysentence(saystring):
	words = saystring.split()

	for word in words:
		playsound(soundpath + word + filetype)


if __name__ == "__main__":
	saystring = sys.argv[1];
	saysentence(saystring)
