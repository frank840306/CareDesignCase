import sys  
from sklearn.ensemble import RandomForestClassifier
import numpy as np
import pickle
import csv

class RandomForestModel:
	def __init__(self, modelname):
		self.name = modelname
		self.savepath = 'mdl/'
	def trainModel(self, file, input_d, output_d):
		f = open(file, 'r', encoding = "latin1")
		cr = csv.reader(f)
		data = []
		for i, line in enumerate(cr):
			if i == 0:
				continue
			else:
				data.append(list(map(float, line)))
		f.close()
		data = np.array(data)
		print (data)
		#data = pandas.read_csv(file, encoding = "latin1", header = None)
		#data = data.as_matrix()
		#len(data[0])
		inputdata = data[0: , :input_d]
		outputdata = data[0: , input_d:]
		inputdata2 = []
		outputdata2 = []
		for i, row in enumerate(inputdata):
			for j, element in enumerate(outputdata[i]):
				if element == 1:
					inputdata2.append(row)
					outputdata2.append(j)
		#singlelabeldata = np.c_[inputdata2, outputdata2]
		#df = pandas.DataFrame(data = singlelabeldata)
		#df.to_csv('suckmydick.csv', index=False, header=False, index_label=False)
		#print(len(outputdata2))
		#print(len(inputdata2))
		rf = RandomForestClassifier(n_estimators=80)
		rf.fit(inputdata2, outputdata2)
		with open(self.savepath + self.name + '.pkl', 'wb') as f:
			pickle.dump(rf, f)
	def predictFocus(self, input):
		try:
			with open(self.savepath + self.name + '.pkl', 'rb') as f:
				rf = pickle.load(f)
		except:
			print("You don't have the model file. Please train a model first.")
		try:
			#prediction = rf.predict(input)
			proba = rf.predict_proba(input)
		except:
			print ("the input format is wrong!")
		#print (proba)
		sorted_proba = np.argsort(proba)
		sorted_proba = sorted_proba.reshape([len(sorted_proba[0])])[::-1]
		count = 0 
		for ele in proba:
			for e in ele:
				if e == 0:
					count = count + 1
		used = len(proba[0]) - count
		outputlist = []
		for i in range(used):
			outputlist.append(sorted_proba[i])
		return outputlist
#print(type(inputdata2[0]))
#print(type(inputdata2))
