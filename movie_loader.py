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

def load_and_cut_frames(movieIds, xy=None, duration = 120):
	"""loads movies from filenames and cuts frames out"""
	data = load_from_movie(movieIds,xy,duration)
	frames = cut_frames(data)
	return frames

def load_movies_from_path(path,extensions=['.avi'],xy=None):
	"""loads all movies from a folder with given extensions"""
	ls = os.listdir(path)
	movies_to_load = []
	for i in ls:
		for ext in extensions:
			if ext in i:
				movies_to_load.append(path+i)
				break
	return load_from_movie(movies_to_load,xy)

def cut_frames(d):
	"""gets data loaded from movies in RGB and cuts frames longer than 4 seconds out"""
	frames = []
	for data in d:	
		diffs = np.mean(np.mean(np.abs(np.diff(data,axis=2)),axis=0),axis=0).ravel()	
		thresh = 0.5*(np.mean(diffs)+np.max(diffs))
		inds = np.where(diffs>thresh)[0]
		st = 0
		for i in inds:
			if i-st > 100: #disregard too short frames
				frames.append(data[:,:,st:i-1]) #add to list of frames
			st = i
		if len(data[0,0,:])- i>100:
			frames.append(data[:,:,i:])
	return frames
