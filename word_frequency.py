import pandas as pd 
import numpy as np
from matplotlib import pyplot as plt 
import json
import jieba

def unique(path):
	with open(path, 'r') as f:
		text = json.load(f)
	s = pd.Series(text)
	s = list(s.unique())
	print('delete %d comments'%(len(text)- len(s)))
	return s

def cut(s):
	cut_comments = []
	for sentence in s:
		cut_comments.append(list(jieba.cut(sentence)))
	return cut_comments


def filter_stopword(processed_comments):
	stop = pd.read_csv('./stoplist.txt', sep='tim', header=None)
	stop = [' ', ' ', None] + list(stop[0])
	dataframe = pd.DataFrame(processed_comments)
	my_func = lambda x: x if x not in stop else 'null'
	dataframe = dataframe.applymap(my_func)
	words = []
	for row in dataframe.values:
		for v in row:
			if v not in ['\n', 'null'] :
				words.append(v)
	return words


s = unique('./comments.json')
processed_comments = cut(s)
words = filter_stopword(processed_comments)
s = pd.Series(words)
frequency = s.value_counts()
with open('./frequency.csv', 'w') as f:
	frequency.to_csv(f, header=['frequency'])

