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
    var featureFloatList = [String]()
    var featureDict:[String:[String]]?
    
    var featureModel = FeatureModel()
    var featureButtonView:FeatureButtonView!
    
    @IBOutlet weak var featureButtonViewPlaceholder: UIView!
    @IBOutlet weak var focusSelectViewPlaceholder: UIView!
    var focusSelectView:FocusSelectView!
    
    @IBOutlet weak var focusTextField: UITextField!
    @IBOutlet weak var confirm_btn: UIButton!
    @IBOutlet weak var clear_btn: UIButton!

    var fileInputName:String? = "example_37_14"
    @IBOutlet weak var fileInputField: UITextField!
    @IBOutlet weak var fileInputBtn: UIButton!
    var hospitalName:String? = "NTU1"
    @IBOutlet weak var hospitalInputField: UITextField!
    @IBOutlet weak var hospitalInputBtn: UIButton!
    override func viewDidLoad() {
        super.viewDidLoad()
        // Do any additional setup after loading the view, typically from a nib.
        
        //取得螢幕尺寸
        fullSize = UIScreen.main.bounds.size
        
        self.title = "智慧紀錄"
        self.view.backgroundColor = UIColor.init(red: 1, green: 1, blue: 1, alpha: 1)
        
        //        featureButtonViewPlaceholder.removeFromSuperview()
        featureButtonViewPlaceholder.isHidden = true
        updateFeatureButton()
        
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
        
        setButtons()
        
        let tapGestureRecogniser = UITapGestureRecognizer(target: self, action: #selector(tap))
        view.addGestureRecognizer(tapGestureRecogniser)
    }
    
    func tap(sender: UITapGestureRecognizer) {
        resignFirstResponderFromTextField()
    }
    func resignFirstResponderFromTextField(){
        let textFieldList = [focusTextField, hospitalInputField, fileInputField]
        
        for textFiled in textFieldList{
            if (textFiled != nil){
                if (textFiled!.isFirstResponder) {
                    textFiled!.resignFirstResponder()
                }
            }
        }
        
        featureButtonView.resignFistResponderForFields()
    }
    
    func setButtons(){
        clear_btn.addTarget(nil, action: #selector(ViewController.clickClearButton), for: .touchUpInside)
        
        hospitalInputBtn.addTarget(nil, action: #selector(ViewController.clickHospitalButton), for: .touchUpInside)
        
        fileInputBtn.addTarget(nil, action: #selector(ViewController.clickHospitalButton), for: .touchUpInside)
    }
    
    func setFocusTextField(){
        
        focusTextField.delegate=self;
        // 尚未輸入時的預設顯示提示文字
        focusTextField.placeholder = "請輸入焦點"
        
        // 輸入框的樣式 這邊選擇圓角樣式
        focusTextField.borderStyle = .roundedRect
        
        // 輸入框右邊顯示清除按鈕時機 這邊選擇當編輯時顯示
        focusTextField.clearButtonMode = .whileEditing
        
        // 輸入框適用的鍵盤 這邊選擇 適用輸入 Email 的鍵盤(會有 @ 跟 . 可供輸入)
        focusTextField.keyboardType = .default
        
        // 鍵盤上的 return 鍵樣式 這邊選擇 Done
        focusTextField.returnKeyType = .done
        
        fileInputField.delegate = self;
        hospitalInputField.delegate = self;
        
        hospitalInputField.placeholder = "請輸入醫院"
        hospitalInputField.text = hospitalName
        fileInputField.placeholder = "請輸入醫院"
        fileInputField.text = fileInputName
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
    
    func clickHospitalButton(){
        if let new_name = hospitalInputField.text{
            hospitalName = new_name
        }
        if let new_name = fileInputField.text{
            fileInputName = new_name
        }
        
        //update feature button for this hospital
        updateFeatureButton()
        
        resignFirstResponderFromTextField()
    }
    
    func clickClearButton(){
        featureButtonView.clearFeatureButton()
        focusSelectView.clearFocusButton()
        focusTextField.text = ""
        
        resignFirstResponderFromTextField()
    }

    func clickConfirmButton(sender: UIButton){
        
//        sender.isHighlighted = true
//        UIView.transition(with: sender,
//                          duration: 0.1,
//                          options: .transitionCrossDissolve,
//                          animations: { sender.isHighlighted = false },
//                          completion: nil)
//        
        resignFirstResponderFromTextField()
    }
    
    func updatePredict(){
        let isFeatured = featureButtonView.getFeature()
        let floats = featureButtonView.getFloats()
        featureModel.getFocusPrediction(isFeatured, floats)
    }
    
    func updateFeatureButton(){
        // load feature model
        featureModel.setHospital(hospital: self.hospitalName!)
        featureModel.setFileName(fileName: self.fileInputName!)
        print("update feature")
        
        featureDict = featureModel.getFeatureDict()
        featureList = (featureDict?["Bool"]) ?? ["feature","list","error"]
        featureFloatList = (featureDict?["Float"]) ?? ["feature","float","error"]
        
        // add feature Button view
//        featureButtonView.removeFromSuperview()
        featureButtonView = FeatureButtonView(frame: featureButtonViewPlaceholder.frame)
        featureButtonView.setFeatureList(featureList: featureList, featureFloatList: featureFloatList)
        featureButtonView._setParentViewController(self)
        self.view.addSubview(featureButtonView)
    }
    
    func updataFocusButton(){
        let focusList = featureModel.getFocusList()
        focusSelectView.updateBtn(focusList)
    }
    
    func setFocusLabel(focus: String){
        focusTextField.text = focus
    }
}

