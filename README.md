# CareDesignCase

#install the requrivement
This command will install the libraries included with the pip
> $ pip install -r requirements.txt

#open server
1. >./run_server.sh clean
2. >./run_server.sh debug

#Use gunicorn to run the server
> $ env PYTHONPATH=$PYTHONPATH:$PWD/src gunicorn app2:app --log-file=-

#Project Folder Structure
.
├── CareDesignDemoApp
├── Procfile
├── README.md
├── app.py
├── app2.py  ** // the python code which gunicorn runs **
├── config
│   └── logging.json
├── data     
│   ├── example_14_6.csv
│   ├── example_37_14.csv
│   ├── ** // put .csv files here ** 
├── log      
│   ├── ** // server log will be saved here **
├── mdl      
│   ├── ** // model will be saved here **
├── requirements.txt
├── run_server.sh
├── runtime.txt
├── setup.sh
├── src
│   ├── ** // source codes are here **
│   ├── array2url.py
│   ├── casemodel.py
│   ├── hospitalManager.py
│   ├── logManager.py
│   ├── rfModel.py
│   ├── server.py
│   ├── trainingManager.py
│   └── utils.py
├── version2
│   ├── ** // this is the version2 which is not finished and stopped **
└── view
    ├── ** // this is the backstage view which is not finished and stopped **
    ├── admin.py
    └── view.py

#Training Data
Put the .csv training data into the path: [project_root]/data/

#API
Follow the step:

1. Add Hospital: http://127.0.0.1:8000/addHospital?hospital=NTU1
2. Add File: http://127.0.0.1:8000/addFile?hospital=NTU1&filename=example_37_14
	1. Default Model is random forest, if yout want to use keras nn, add `method=keras` in the url
	2. http://127.0.0.1:8000/addFile?hospital=NTU1&filename=example_37_14&method=keras
3. Get Feature: http://127.0.0.1:8000/feature?hospital=NTU1&filename=example_37_14
4. Predict: http://127.0.0.1:8000/predict?hospital=NTU1&filename=example_37_14&f1=1&f3=1&f7=1
	1. f1 means feature1, it start from 0 to the feature length
	2. another example: (the second row in example_37_14.csv) the out put should be `[ "體液電解質不平衡", "疲憊", "睡眠型態紊亂", "組織灌流不足" ]`
	3. http://127.0.0.1:8000/predict?hospital=NTU1&filename=example_37_14&f0=1&f4=1&f7=1&f13=1&f15=1.0&f17=1.0&f20=1.0&f25=1.0&f30=63.0&f31=154.0&f32=86.0&f33=99.0&f34=177.0&f35=138.0&f36=3.1'
5. http://127.0.0.1:8000/addFile?hospital=NTU1&filename=example_37_14_bool
6. http://127.0.0.1:8000/feature?hospital=NTU1&filename=example_37_14_bool
7. http://127.0.0.1:8000/predict?hospital=NTU1&filename=example_37_14_bool&f1=1&f3=1&f7=1
8. Remove Hospital: http://127.0.0.1:8000/removeHospital?hospital=NTU1
9. Remove File: http://127.0.0.1:8000/removeFile?hospital=NTU1&filename=example_37_14

