import sys
import csv
import numpy as np
from keras.models import Sequential
from keras.layers import Dense, Activation
from keras.optimizers import SGD, Adagrad, Adadelta, Adam
from keras.models import load_model
import pickle

class kerasModel:
	'''
	use keras NN model

	trainModel(file, input_d, output_d)
	[parameters]
		file : path to the training data file (must be .csv file)
		input_d : feature dimension (int)
		output_d : number of classes/focus (int)
	[output]
		return : no return value
		file : save a model file (.h5 file)

	predictFocus(input)
	[parameters]
		input : a list of features (ex. [0, 1, 0, 0, 0, 1, 51, 8.7] if input_d is 8)
	[output]
		return : a sorted list of focus index (ex. [2, 4, 1, 0, 3] if output_d is 5)
	
	'''

	def trainModel(self, file, input_d, output_d):
		f = open(file, 'r')
		alldata = csv.reader(f)
		Data = []
		for data in alldata:
			try:
				Data.append(list(map(float, data)))
			except:
				print ('row error')
		Data = np.array(Data)
		f.close()
		data_length = len(Data)
		split_idx = int(data_length*0.8)

		X_train = Data[:split_idx, :input_d]
		train_max = X_train.max(axis=0)
		train_min = X_train.min(axis=0)
		X_train = (X_train - train_min) / (train_max - train_min)
		Y_train = Data[:split_idx, input_d:]
		X_valid = Data[split_idx:, :input_d]
		X_valid = (X_valid - train_min) / (train_max - train_min)
		Y_valid = Data[split_idx:, input_d:]

		with open('max.p', 'w') as fmax:
			pickle.dump(train_max, fmax)
		with open('min.p', 'w') as fmin:
			pickle.dump(train_min, fmin)

		#model
		model = Sequential()
		model.add(Dense(units=32, input_dim=input_d))
		model.add(Activation('relu'))
		model.add(Dense(units=output_d))
		model.add(Activation('sigmoid'))
		model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
		model.fit(X_train, Y_train, epochs=30, batch_size=8, validation_data=(X_valid, Y_valid))
		model.save('mymodel.h5')

	def predictFocus(self, input):
		train_max = pickle.load(open('max.p', 'r'))
		train_min = pickle.load(open('min.p', 'r'))
		x = (np.array([input]) - train_min) / (train_max - train_min)
		model = load_model('mymodel.h5')
		pred = model.predict(x)[0]
		sorted_pred = np.argsort(pred)[::-1]
		#print list(sorted_pred)
		return list(sorted_pred)


#trainModel('31_14.csv', 37, 14)
#ex = [0,1,1,0,1,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,1,0,0,0,0,0,0,0,0,78,158,90,163,203,147,4.3]
#m = kerasModel()
#m.predictFocus(ex)

