import re
import math
import multiprocessing as mp
import sqlite3
from janome.tokenizer import Tokenizer
import sys
import random

def cul(wordlists):
	datanum = 0
	connector = sqlite3.connect("1.db")
	cur = connector.cursor()
	total = cur.execute("SELECT COUNT(num) FROM subdata") .fetchone()
	k = 0
	while k < total[0]:
		count = 0
		data = cur.execute('SELECT * FROM subdata WHERE num=?',(repr(k),)).fetchone()
		for wordlist in wordlists:
			if wordlist in data[2]:
				count += 1
		if data[1]==0:
			x = 0
		else:
			#ヒット数/単語総数
			x = count/data[1]
		if x == 0:
			#スムージング
			x = 1/500
		newvalue = math.log(x)
		if k ==0:
			value = newvalue
			datanum = 0
		elif value < newvalue:
			value = newvalue
			datanum = k
		k += 1
	#ヒットするレスが一つもなければランダムで選ぶ
	if datanum == 0:
		datanum = random.randint(1,total[0])
	return(datanum)

if __name__ == '__main__':
	topscore=0
	words=[]
	conn = sqlite3.connect("1.db")
	cursol = conn.cursor()
	argvs = sys.argv
	if len(argvs) != 2:
		print("Usage: python3 ai.py [word]")
		exit()
	sentence = argvs[1]
	t = Tokenizer()
	tokens = t.tokenize(sentence)
	for token in tokens:
		partOfSpeech = token.part_of_speech.split(",")[0]
		if partOfSpeech == "名詞" or partOfSpeech == "動詞":
			words.append(token.surface)
	#名詞、動詞が一つもなければランダムで選ぶ
	if len(words) == 0:
		totalnum = cursol.execute("SELECT COUNT(num) FROM data") .fetchone()
		topscore = random.randint(1,totalnum[0])
	else:
		topscore = cul(words)
	result = cursol.execute('SELECT * FROM data WHERE num=?',(repr(topscore),)).fetchone()
	answer = result[3]
	print(answer)