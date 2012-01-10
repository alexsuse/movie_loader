import numpy as np
from PIL import Image
import os

def load_from_movie(movieIds, xy = None, duration = 120):
	allImg = []
	if 'temp' not in os.listdir('./'):
		os.mkdir('./temp')
	else:
		os.system('rm -rf ./temp/*')
	for id in movieIds:
		imgArray=[]
		command = 'ffmpeg -i '+id+' -t '+str(duration)+' ./temp/output%5d.png'
		os.system(command)
		filenames = os.listdir('./temp')
		for fi in filenames:
			try:
				img = Image.open('./temp/'+fi)
				print "Reading " + fi
				if xy is not  None:
					h = img.resize(xy,Image.ANTIALIAS)
					imgArray.append(h.getdata())
				else:
					imgArray.append(img.getdata())
			except EOFError:
				pass
		os.system('rm -rf ./temp/output*')
		imgArray = np.array(imgArray,np.int16)
		imgArray = imgArray.T
		allImg.append(imgArray)
	os.system('rm -rf ./temp')
	allImg = np.array(allImg)
	return allImg	

def load_movies_from_path(path,extensions=['.avi'],xy=None):
	ls = os.listdir(path)
	movies_to_load = []
	for i in ls:
		for ext in extensions:
			if ext in i:
				movies_to_load.append(path+i)
				break
	return load_from_movie(movies_to_load,xy)

