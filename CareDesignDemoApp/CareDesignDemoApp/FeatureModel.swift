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
    var url:URL!
    var featureList:[String]! = ["假的","胸悶", "疼痛", "呼吸困難", "蒼白", "血壓不穩", "步態不穩", "肢體無力", "心律不整", "冰冷", "瘀斑", "暈眩", "焦慮", "潰瘍", "心電圖異常"]
    
    init(){
        my_url = debug_url
        feature_url  = debug_url+"feature"
        url = URL(string: feature_url)
    }
    
    func getFeatureList() -> [String]{
        var taskFlag:Bool = false
        
        let task = URLSession.shared.dataTask(with: url!) { data, response, error in
            guard error == nil else {
                print(error!)
                
                return
            }
            guard let data = data else {
                print("Data is empty")
                return
            }
            
            if let json = try? JSONSerialization.jsonObject(with: data, options: []){
                print(json)
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
}
