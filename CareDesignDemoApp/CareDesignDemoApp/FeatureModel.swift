//
//  FeatureModel.swift
//  CareDesignDemoApp
//
//  Created by Bigyo on 07/07/2017.
//  Copyright © 2017 Bigyo. All rights reserved.
//

import Foundation

class FeatureModel{
    
    var hospital :String = "NTU1"
    var fileName: String = "example_37_14_bool"
    var documentsPath :String!
    let debug_url = "http://127.0.0.1:8000/"
    var my_url:String!
    var feature_url:String!
    var predict_url:String!
    var featureList:[String]! = ["沒連上線","胸悶", "疼痛", "呼吸困難", "蒼白", "血壓不穩", "步態不穩", "肢體無力", "心律不整", "冰冷", "瘀斑", "暈眩", "焦慮", "潰瘍", "心電圖異常"]
    var featureDict:[String: [String]] = ["Bool": ["沒連上線","胸悶", "疼痛", "呼吸困難", "蒼白", "血壓不穩", "步態不穩", "肢體無力", "心律不整", "冰冷", "瘀斑", "暈眩", "焦慮", "潰瘍", "心電圖異常"], "Float": ["age", "sbp", "dbp", "trig", "chol", "Na", "K"]]
    var focusList:[String]! = ["沒連上線", "急性疼痛", "心輸出量減少", "低效呼吸型態", "高危險性出血", "高危險性跌倒 ", "組織灌流不足"]
    
    var parentViewController: ViewController?
    
    init(){
        my_url = debug_url
        feature_url = my_url + "feature"
        predict_url = my_url + "predict"
    }
    
    func setHospital(hospital: String){
        self.hospital = hospital
    }
    func setFileName(fileName: String){
        self.fileName = fileName
    }
    
    func _setParentViewController(_ vc: ViewController){
        self.parentViewController = vc
    }
    
    func getFeatureDict() -> [String: [String]]{
        var taskFlag:Bool = false
        let url_arg:String = "?hospital="+hospital+"&filename="+fileName
        let request_url = feature_url+url_arg
        print("request = " + request_url)
        
        let task = URLSession.shared.dataTask(with: URL(string: request_url)!) { data, response, error in
            guard error == nil else {
                print(error!)
                
                return
            }
            guard let data = data else {
                print("Data is empty")
                return
            }
            
            if let json = try? JSONSerialization.jsonObject(with: data, options: []){
                self.featureDict = json as! [String: [String]]
            }else{
                print("json failed")
            }
            taskFlag = true
        }
        task.resume()
        
        while(!taskFlag) {
        }
        return self.featureDict
    }
    
    func getFocusPrediction(_ isFeatured:[Bool], _ floats: [Float]){
        var taskFlag:Bool = false
        var url_arg:String = "?hospital="+hospital+"&filename="+fileName
        for index in 0...isFeatured.count-1{
            if(isFeatured[index]){
                url_arg += "&f"+String(index)+"=1"
            }
        }
        for (index, float) in floats.enumerated(){
            let f_index = index + isFeatured.count
            url_arg += "&f"+String(f_index)+"="+String(float)
        }
        
        let request_url = predict_url+url_arg
        print("request = " + request_url)
        
        let task = URLSession.shared.dataTask(with: URL(string: request_url)!){
            data, response, error in
            guard error == nil else {
                print(error!)
                return
            }
            guard let data = data else {
                print("Data is empty")
                return
            }
            
            if let json = try? JSONSerialization.jsonObject(with: data, options: []){
                self.focusList = json as! [String]
                print("self.focusList = ", self.focusList)
                print("json success")
            }else{
                print("json failed")
            }
            taskFlag = true
            
        }
        task.resume()
        while(!taskFlag) {
        }
        self.parentViewController?.updataFocusButton()
    }
    
    func getFocusList()->[String]{
        return focusList
    }
    
    
}
