import sqlite3
from janome.tokenizer import Tokenizer


t = Tokenizer()
connector = sqlite3.connect("1.db")
cur = connector.cursor()
cur.execute("CREATE TABLE subdata(num int,totalwords int,word text);")
total = cur.execute("SELECT COUNT(num) FROM data") .fetchone()
k = 0
while k < total[0]:
	words=[]
	count=0
	data = cur.execute('SELECT * FROM data WHERE num=?',(k,)).fetchone()
	if isinstance(data[2],type(None)):
		cur.execute("INSERT INTO subdata(num,totalwords,word) VALUES (?,0,0)",(k,))
		k +=1
		continue
	tokens = t.tokenize(data[2])
	for token in tokens:
		partOfSpeech = token.part_of_speech.split(",")[0]
		if partOfSpeech == "名詞":
			count += 1
			words.append(token.surface)
		elif partOfSpeech == "動詞":
			count += 1
			words.append(token.surface)
	if len(words)==0:
		words.append("0")
	cur.execute("INSERT INTO subdata(num,totalwords) VALUES (?,?)",(k,count,))
	renketu=""
	for word in words:
		renketu =renketu + " " + word
	cur.execute("UPDATE subdata SET word = ? WHERE num=?",(renketu,k))
	k += 1
connector.commit()