import pickle, json, xlrd, csv, os

default_path = {
	'ROOT_DIR'		: '.',
	'DATA_DIR'		: './data',
	'SRC_DIR'		: './src',
	'MDL_DIR'		: './mdl',
	'HOSPITALJSON'	: './data/hospitalList.json',
	'HOSPITAL2MODELJSON'	: './data/hospital2model.json',	# default file size = 10 / hospital, 
															# default model size = 5 / file, from old to new
															# type = dict
															# ex: hospital2model['NTU']['example_31_14'] = 
															# 	['NTU_example_31_14_20170711', 'NTU_example_31_14_20170712', 'NTU_example_31_14_20170713']
															# 
	'TRAININGQUEUEJSON'		: './data/trainingQueue.json',		# default size = 5 / file, type = list, from old to new
}

default_config = {
	'FILE_NUM_PER_HOSPITAL'	: 10,		# the limit of CSV file maintained in a hospital
	'MODEL_NUM_PER_FILE'	: 5,		# the limit of history model number in a CSV file 
	'TRAINING_QUEUE_SIZE'	: float('inf'),	# the limit of the size of training queue
	'TRAINING_SKIP_NUM'		: 10,		# no task found after #iter will terminate the thread
	'TRAINING_METHOD'		: 'rf'		# random forest		
}

status = {
	'NoTask'	: 'NoTask',
	'Opened'	: 'Opened', 
	'Ongoing'	: 'Ongoing', 
	'Closed'	: 'Closed', 
	'Suspended'	: 'Suspended', 
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
