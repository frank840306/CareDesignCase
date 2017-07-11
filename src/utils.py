import pickle, json, xlrd, csv, os

default_path = {
	'ROOT_DIR'		: '.',
	'DATA_DIR'		: './data',
	'SRC_DIR'		: './src',
	'MDL_DIR'		: './mdl',
	'HOSPITALJSON'	: './data/hospitalList.json',
	'HOSPITAL2MODELJSON'		: './data/hospital2model.json',	# default size = 5 / hospital, from old to new
}

def XLSX2CSV(xlsx):
	wb = xlrd.open_workbook(xlsx)
	sh = wb.sheet_by_name('Sheet1')
	print(xlsx)
	print(xlsx.split('.', 1)[0] + '.csv')
	your_csv_file = open(xlsx.replace('xlsx', 'csv'), 'w', newline='')
	wr = csv.writer(your_csv_file, quoting=csv.QUOTE_NONE)

	for rownum in range(sh.nrows):
		# print(sh.row_values(rownum))
		# print(type(sh.row_values(rownum)))
		wr.writerow(sh.row_values(rownum))
		# wr.writerow([bytes(val, 'UTF-8') for val in sh.row_values(rownum)])

	your_csv_file.close()

	# with open(xlsx.split('.', 1)[0] + '.csv', 'w', newline='') as file:
	# 	writer = csv.writer()		

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
	return text

def writeJson(data, fout):
	with open(fout, 'w') as file:
		json.dump(data, file)
	return
