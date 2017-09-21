//
//  FeatureButtonView.swift
//  CareDesignDemoApp
//
//  Created by Bigyo on 07/07/2017.
//  Copyright © 2017 Bigyo. All rights reserved.
//

import Foundation
import UIKit


class FeatureButton: UIButton{

    var isFeatured:Bool
    var index:Int
    
    required init(frame: CGRect, _ index: Int) {
        self.isFeatured = false
        self.index = index
        
        super.init(frame: frame)
        
        // set other operations after super.init, if required
        titleLabel!.font = UIFont.boldSystemFont(ofSize: 10)
        setTitleColor(.black, for: .normal)
        backgroundColor = .white
        
        isEnabled = true
        
        layer.borderWidth = 1.5
        layer.borderColor = care_color_white.cgColor
        addTarget(nil, action: #selector(self.click), for: .touchUpInside)
        
    }
    
    required init?(coder aDecoder: NSCoder) {
        fatalError("init(coder:) has not been implemented")
    }
    
    func click(){
        self.isFeatured = !self.isFeatured

        let _superview = self.superview as! FeatureButtonView
        _superview.click(self.index)
        changeColor()
    }
    
    func changeColor(){
        if(self.isFeatured){
            setTitleColor(.white, for: .normal)
            backgroundColor = care_color_green
        }else{
            setTitleColor(.black, for: .normal)
            backgroundColor = .white
        }
    }
    
    func disselect(){
        self.isFeatured = false
        
        changeColor()
    }
    
}



class FeatureFloat: UIView, UITextFieldDelegate{
    var label: UILabel
    var inputField: UITextField
    required init(frame: CGRect, _ index: Int){
        
        label = UILabel(frame: CGRect(x:0,y:0,width:frame.width/2,height:frame.height))
        inputField = UITextField(frame: CGRect(x:frame.width/2,y:0,width:frame.width/2,height:frame.height))
        inputField.text = "0"
        
        label.font = UIFont.boldSystemFont(ofSize: 10)
        label.textColor = .black
        
        label.layer.borderWidth = 1.5
        label.layer.borderColor = care_color_white.cgColor
        label.textAlignment = NSTextAlignment.center
        
        inputField.font = UIFont.boldSystemFont(ofSize: 10)
        inputField.textColor = .black
        
        inputField.layer.borderWidth = 1.5
        inputField.layer.borderColor = care_color_white.cgColor
        inputField.textAlignment = NSTextAlignment.center
        
        super.init(frame: frame)
        
        
        self.addSubview(label)
        self.addSubview(inputField)
        
        inputField.delegate = self
    }
    
    required init?(coder aDecoder: NSCoder) {
        fatalError("init(coder:) has not been implemented")
    }
    
    func setTitle(_ text: String){
        label.text = text
        inputField.text = defaultValue(feature: text)
    }
    
    func textFieldShouldReturn(_ textField: UITextField) -> Bool {   //delegate method
        textField.resignFirstResponder()
        return true
    }
    
    func defaultValue(feature: String) -> String{
        let features = ["age", "sbp", "dbp", "trig", "chol", "Na", "K"]
        let defaults = ["63", "154", "86", "99", "177", "138", "3.1"]
        
        if (features.contains(feature)){
            return defaults[features.index(of: feature)!]
        }else {
            return "0"
        }
    }
}

class FeatureButtonView: UIScrollView{
    // remember to set content size to make use of scroll view
    
    var featureList = [String]()
    var featureFloatList = [String]()
    var parentViewController: ViewController?
    var fullSize:CGRect!
    
    override init(frame: CGRect){
        
        
        super.init(frame: frame)
        
        self.fullSize = self.frame
        backgroundColor = .white
    }
    
    required init?(coder aDecoder: NSCoder) {
        fatalError("init(coder:) has not been implemented")
    }
    
    func setFeatureList(featureList: [String], featureFloatList: [String]){
        self.featureList = featureList
        self.featureFloatList = featureFloatList
        var offsetY:CGFloat = 0
        offsetY = setFeatureButton(offsetY)
        offsetY = setFeatureFloat(offsetY)
        
        
        //TODO: remake contentSize to make use of scrollview
        self.contentSize = CGSize(width: frame.width, height: max(frame.height, offsetY) )
    }
    
    func _setParentViewController(_ vc: ViewController){
        self.parentViewController = vc
    }
    
    
    var row_n:Int = 4
    let interval:CGFloat = 10
    let border:CGFloat = 20
    let btn_h:CGFloat = 20
    var btn_w:CGFloat!
    var buttons: [FeatureButton] = []
    var featureFloats:[FeatureFloat] = []
    var isFeatured: [Bool] = []
    
    func setFeatureButton(_ offsetY: CGFloat) -> CGFloat{
        buttons = []
        
        row_n = 4
        btn_w = (fullSize.width - 2 * border + interval) / CGFloat(row_n) - interval
        
        for (index, feature) in featureList.enumerated(){
            let pos_x = border + CGFloat(index%row_n) * (btn_w+interval)
            let pos_y = border + CGFloat(index/row_n) * (btn_h+interval) + offsetY
            let button = FeatureButton(frame: CGRect(x:pos_x, y:pos_y, width: btn_w, height: btn_h), index)
            button.setTitle(feature, for: .normal)
            buttons.append(button)
            isFeatured.append(false)
            self.addSubview(button)
        }
        
        let new_offsetY = (CGFloat((featureList.count-1)/row_n + 1) * (btn_h+interval) - interval + border)
        return new_offsetY
    }
    
    func setFeatureFloat(_ offsetY: CGFloat) -> CGFloat{
        featureFloats = []
        
        row_n = 2
        btn_w = (fullSize.width - 2 * border + interval) / CGFloat(row_n) - interval
        
        for (index, feature) in featureFloatList.enumerated(){
            let pos_x = border + CGFloat(index%row_n) * (btn_w+interval)
            let pos_y = border + CGFloat(index/row_n) * (btn_h+interval) + offsetY
            let featureFloat = FeatureFloat(frame: CGRect(x:pos_x, y:pos_y, width: btn_w, height: btn_h), index)
            //todo: set label
//            featureFloat.setTitle(feature)
            featureFloat.setTitle(feature)
            featureFloats.append(featureFloat)
            //add Subview
            self.addSubview(featureFloat)
        }
        
        let new_offsetY = CGFloat((featureFloatList.count-1)/row_n+1) * (btn_h+interval) - interval + border + offsetY
        return new_offsetY
    }
    
    func resignFistResponderForFields(){
        
        for featureFloat in featureFloats{
            let field = featureFloat.inputField
            if (field.isFirstResponder){
                field.resignFirstResponder()
            }
        }
    }
    
    func clearFeatureButton(){
        for (index,button) in buttons.enumerated(){
            button.disselect()
            isFeatured[index] = false
        }
    }
    
    func click(_ index: Int){
        isFeatured[index] = !isFeatured[index]
        parentViewController!.updatePredict()
    }
    
    func getFeature() -> [Bool]{
        return isFeatured
    }
    func getFloats() -> [Float]{
        var floats:[Float] = []
        for featureFloat in featureFloats{
            let field = featureFloat.inputField
            if let f = Float(field.text!){
                floats.append(f)
            }else{
                floats.append(Float(0))
            }
        }
        return floats
    }
}
