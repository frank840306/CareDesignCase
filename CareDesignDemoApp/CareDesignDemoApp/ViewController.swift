//
//  ViewController.swift
//  CareDesignDemoApp
//
//  Created by Bigyo on 06/07/2017.
//  Copyright © 2017 Bigyo. All rights reserved.
//

import UIKit

class ViewController: UIViewController, UITextFieldDelegate {

    var fullSize:CGSize!
    var featureList = ["胸悶", "疼痛", "呼吸困難", "蒼白", "血壓不穩", "步態不穩"]
    
    var featureModel = FeatureModel()
    var featureButtonView:FeatureButtonView!
    
    @IBOutlet weak var featureButtonViewPlaceholder: UIView!
    @IBOutlet weak var focusSelectViewPlaceholder: UIView!
    var focusSelectView:FocusSelectView!
    
    @IBOutlet weak var focusTextField: UITextField!
    @IBOutlet weak var confirm_btn: UIButton!
    @IBOutlet weak var clear_btn: UIButton!

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
        featureButtonView = FeatureButtonView(frame: featureButtonViewPlaceholder.frame)
        featureButtonView.setFeatureList(featureList: featureList)
        featureButtonView._setParentViewController(self)
        featureButtonViewPlaceholder.removeFromSuperview()
        self.view.addSubview(featureButtonView)
        
        focusSelectView = FocusSelectView(frame: focusSelectViewPlaceholder.frame)
        focusSelectView._setParentViewController(self)
        focusSelectViewPlaceholder.removeFromSuperview()
//        focusSelectView.isHidden = true
        self.view.addSubview(focusSelectView)
        
        featureModel._setParentViewController(self)
        
        setFocusTextField()
        
        // confirm button
//        let cbtn_width:CGFloat = 80
//        let cbtn_height:CGFloat = 25
//        let cbtn_border:CGFloat = 10
//        let confirm_btn = UIButton(frame: CGRect(x: fullSize.width -  cbtn_width - cbtn_border, y: fullSize.height - cbtn_height - cbtn_border, width: cbtn_width, height: cbtn_height))
//        confirm_btn.setTitle("完成", for: .normal)
////        confirm_btn.setTitle("點擊", for: .highlighted)
//        
//        // 按鈕文字顏色
//        confirm_btn.setTitleColor(care_color_green, for: .normal)
//        confirm_btn.setTitleColor(UIColor.lightGray, for: .highlighted)
//        // 按鈕是否可以使用
//        confirm_btn.isEnabled = true
//        // 按鈕背景顏色
////        confirm_btn.backgroundColor = .white
//        // 按鈕按下後的動作
        confirm_btn.addTarget(nil, action: #selector(ViewController.clickConfirmButton), for: .touchUpInside)
        
//
//        self.view.addSubview(confirm_btn)
        clear_btn.addTarget(nil, action: #selector(ViewController.clickClearButton), for: .touchUpInside)
        
        let tapGestureRecogniser = UITapGestureRecognizer(target: self, action: #selector(tap))
        view.addGestureRecognizer(tapGestureRecogniser)
    }
    
    func tap(sender: UITapGestureRecognizer) {
        if focusTextField.isFirstResponder {
            focusTextField.resignFirstResponder()
        }
    }
    
    func setFocusTextField(){
        
        focusTextField.delegate=self;
        // 尚未輸入時的預設顯示提示文字
        focusTextField.placeholder = "請輸入文字"
        
        // 輸入框的樣式 這邊選擇圓角樣式
        focusTextField.borderStyle = .roundedRect
        
        // 輸入框右邊顯示清除按鈕時機 這邊選擇當編輯時顯示
        focusTextField.clearButtonMode = .whileEditing
        
        // 輸入框適用的鍵盤 這邊選擇 適用輸入 Email 的鍵盤(會有 @ 跟 . 可供輸入)
        focusTextField.keyboardType = .default
        
        // 鍵盤上的 return 鍵樣式 這邊選擇 Done
        focusTextField.returnKeyType = .done
    }
    
    //without this, text field can't loose focus
    func textFieldShouldReturn(_ textField: UITextField) -> Bool {   //delegate method
        textField.resignFirstResponder()
        return true
    }

    override func didReceiveMemoryWarning() {
        super.didReceiveMemoryWarning()
        // Dispose of any resources that can be recreated.
    }
    
    func clickClearButton(){
        featureButtonView.clearFeatureButton()
        focusSelectView.clearFocusButton()
        focusTextField.text = ""
    }

    func clickConfirmButton(sender: UIButton){
        
//        sender.isHighlighted = true
//        UIView.transition(with: sender,
//                          duration: 0.1,
//                          options: .transitionCrossDissolve,
//                          animations: { sender.isHighlighted = false },
//                          completion: nil)
//        
    }
    
    func updatePredict(){
        let isFeatured = featureButtonView.getFeature()
        featureModel.getFocusPrediction(isFeatured)
    }
    
    func updataFocusButton(){
        let focusList = featureModel.getFocusList()
        focusSelectView.updateBtn(focusList)
    }
    
    func setFocusLabel(focus: String){
        focusTextField.text = focus
    }
}

