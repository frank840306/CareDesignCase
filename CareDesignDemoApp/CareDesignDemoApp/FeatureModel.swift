//
//  FeatureModel.swift
//  CareDesignDemoApp
//
//  Created by Bigyo on 07/07/2017.
//  Copyright © 2017 Bigyo. All rights reserved.
//

import Foundation

class FeatureModel{
    
    var documentsPath :String!
    let debug_url = "http://127.0.0.1:5000/"
    var my_url:String!
    var feature_url:String!
    var predict_url:String!
    var featureList:[String]! = ["沒連上線","胸悶", "疼痛", "呼吸困難", "蒼白", "血壓不穩", "步態不穩", "肢體無力", "心律不整", "冰冷", "瘀斑", "暈眩", "焦慮", "潰瘍", "心電圖異常"]
    var focusList:[String]! = ["沒連上線", "急性疼痛", "心輸出量減少", "低效呼吸型態", "高危險性出血", "高危險性跌倒 ", "組織灌流不足"]
    
    var parentViewController: ViewController?
    
    init(){
        my_url = debug_url
        feature_url = my_url + "feature"
        predict_url = my_url + "predict"
    }
    
    func _setParentViewController(_ vc: ViewController){
        self.parentViewController = vc
    }
    
    func getFeatureList() -> [String]{
        var taskFlag:Bool = false
        
        let task = URLSession.shared.dataTask(with: URL(string: feature_url)!) { data, response, error in
            guard error == nil else {
                print(error!)
                
                return
            }
            guard let data = data else {
                print("Data is empty")
                return
            }
            
            if let json = try? JSONSerialization.jsonObject(with: data, options: []){
                self.featureList = json as! [String]
            }else{
                print("json failed")
            }
            taskFlag = true
        }
        task.resume()
        
        while(!taskFlag) {
        }
        return self.featureList
    }
    
    func getFocusPrediction(_ isFeatured:[Bool]){
        var taskFlag:Bool = false
        
        let task = URLSession.shared.dataTask(with: URL(string: predict_url)!){
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
                print(json)
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
