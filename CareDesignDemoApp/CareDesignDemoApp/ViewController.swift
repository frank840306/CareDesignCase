//
//  ViewController.swift
//  CareDesignDemoApp
//
//  Created by Bigyo on 06/07/2017.
//  Copyright © 2017 Bigyo. All rights reserved.
//

import UIKit

class ViewController: UIViewController {

    var fullSize:CGSize!
    var featureList = ["胸悶", "疼痛", "呼吸困難", "蒼白", "血壓不穩", "步態不穩"]
    
    var featureModel = FeatureModel()
    
    override func viewDidLoad() {
        super.viewDidLoad()
        // Do any additional setup after loading the view, typically from a nib.
        
        //取得螢幕尺寸
        fullSize = UIScreen.main.bounds.size
        
        self.title = "智慧紀錄"
        self.view.backgroundColor = UIColor.init(red: 1, green: 1, blue: 1, alpha: 1)
        
        // load feature model
        featureList = featureModel.getFeatureList()
        
        // add feature Button view
        let featureButtonView = FeatureButtonView(frame: CGRect(x:0,y:100,width:fullSize.width,height:200))
        featureButtonView.setFeatureList(featureList: featureList)
    
        self.view.addSubview(featureButtonView)
        
        // confirm button
        let cbtn_width:CGFloat = 80
        let cbtn_height:CGFloat = 25
        let cbtn_border:CGFloat = 10
        let confirm_btn = UIButton(frame: CGRect(x: fullSize.width -  cbtn_width - cbtn_border, y: fullSize.height - cbtn_height - cbtn_border, width: cbtn_width, height: cbtn_height))
        confirm_btn.setTitle("完成", for: .normal)
        
        // 按鈕文字顏色
        confirm_btn.setTitleColor(care_color_green, for: .normal)
        confirm_btn.setTitleColor(UIColor.darkGray, for: .selected)
        // 按鈕是否可以使用
        confirm_btn.isEnabled = true
        // 按鈕背景顏色
        confirm_btn.backgroundColor = .white
        // 按鈕按下後的動作
        confirm_btn.addTarget(nil, action: #selector(ViewController.clickButton), for: .touchUpInside)
        self.view.addSubview(confirm_btn)
    
    }

    override func didReceiveMemoryWarning() {
        super.didReceiveMemoryWarning()
        // Dispose of any resources that can be recreated.
    }

    func clickButton(){
        print("confirm button")
    }
}

