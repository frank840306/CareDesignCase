# CareDesignCase

#install the requrivement
下述指令會將所需的 libraries 透過 pip 套件管理系統安裝
> $ pip install -r requirements.txt

#open server
1. >./run_server.sh clean
2. >./run_server.sh debug

#Use gunicorn to run the server
> $ env PYTHONPATH=$PYTHONPATH:$PWD/src gunicorn app2:app --log-file=-

#Project Folder Structure
![alt text](https://github.com/frank840306/CareDesignCase/blob/master/img/tree.png)

#Training Data
**檔案需放置於 `[project_root]/data` 路徑底下**

#API
Follow the step:

1. 新增醫院: 
	- api 名稱 `addHospital`
	- 功能：新增醫院
	- 參數：
		- `hospital=[醫院名稱]`
	- 範例：http://127.0.0.1:8000/addHospital?hospital=NTU1
2. 新增檔案: 
	- api 名稱 `addFile`
	- 功能：新增檔案
	- 參數：
		- `hospital=[醫院名稱]`
		- `filename=[檔案名稱]`	**檔案需放置於 /data 路徑底下**
	- 範例：http://127.0.0.1:8000/addFile?hospital=NTU1&filename=example_37_14
	- 預設的 model 是 random forest, 如果要選擇 keras NN model，在 url 中加上 `method=keras` 的參數 
	- 例如：http://127.0.0.1:8000/addFile?hospital=NTU1&filename=example_37_14&method=keras
3. 取得 Feature: 
	- api 名稱 `feature`
	- 功能：取得 model 的 feature，以 json 格式回傳
	- 參數：
		- `hospital=[醫院名稱]`
		- `filename=[檔案名稱]`
	- 範例：http://127.0.0.1:8000/feature?hospital=NTU1&filename=example_37_14
4. 預測: 
	- api 名稱 `predict`
	- 功能：新增檔案
	- 參數：
		- `hospital=[醫院名稱]`
		- `filename=[檔案名稱]`
		- `f0=1` 布林值型別
		- `f31=154.0` 浮點數型別
		- 空著的 feature 預設為 `0` 或 `False`
		- feature index 從零開始
	- 範例：http://127.0.0.1:8000/predict?hospital=NTU1&filename=example_37_14&f1=1&f3=1&f7=1
	- 另一個範例（example_37_14.csv 檔案裡的第二筆資料），預測輸出為`[ "體液電解質不平衡", "疲憊", "睡眠型態紊亂", "組織灌流不足" ]`
	- http://127.0.0.1:8000/predict?hospital=NTU1&filename=example_37_14&f0=1&f4=1&f7=1&f13=1&f15=1.0&f17=1.0&f20=1.0&f25=1.0&f30=63.0&f31=154.0&f32=86.0&f33=99.0&f34=177.0&f35=138.0&f36=3.1'
5. 新增另一筆醫院檔案
	- http://127.0.0.1:8000/addFile?hospital=NTU1&filename=example_14_6
	- http://127.0.0.1:8000/feature?hospital=NTU1&filename=example_14_6
	- http://127.0.0.1:8000/predict?hospital=NTU1&filename=example_14_6&f1=1&f3=1&f7=1
8. 刪除醫院
	- api 名稱 `removeHospital`
	- 功能：刪除指定醫院
	- 參數：
		- `hospital=[醫院名稱]`
	- 範例：http://127.0.0.1:8000/removeHospital?hospital=NTU1
9. 刪除檔案
	- api 名稱 `removeFile`
	- 功能：刪除指定檔案
	- 參數：
		- `hospital=[醫院名稱]`
		- `filename=[檔案名稱]`
	- 範例：Remove File: http://127.0.0.1:8000/removeFile?hospital=NTU1&filename=example_37_14

