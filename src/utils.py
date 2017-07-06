import pickle
import json

def writeFile(data, fout):
	f = open(fout, 'w')
	f.truncate()
	for line in data:
		f.write(line + '\n')
	f.close()
	return

def readFile(fin):
	with open(fin) as file:
		content = file.read()
	return content.splitlines()

def writePickle(data, fout):
	with open(fout, 'wb') as file:
		pickle.dump(data, file)
	return

def readPickle(fin):
	with open(fin, 'rb') as file:
		content = pickle.load(file)
	return content

def readJson(fin):
	with open(fin) as file:
		text = json.load(file)
	# content = json.loads(text)
	# print(content)
	return text

def writeJson(data, fout):
	# text = json.dumps(data)
	# print (text)
	with open(fout, 'w') as file:
		json.dump(data, file)
	return