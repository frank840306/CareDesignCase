//
//  FocusSelectView.swift
//  CareDesignDemoApp
//
//  Created by Bigyo on 09/07/2017.
//  Copyright © 2017 Bigyo. All rights reserved.
//

import Foundation
import UIKit

class FocusButton: UIButton{
    
    var isFeatured:Bool
    var index:Int
    
    required init(frame: CGRect, _ index: Int){
        
        self.isFeatured = false
        self.index = index
        
        super.init(frame: frame)
        
        titleLabel!.font = UIFont.boldSystemFont(ofSize: 10)
        setTitleColor(.black, for: .normal)
        backgroundColor = .white
        
        setTitle("", for: .normal)
        titleLabel?.text = ""
        titleLabel?.frame = frame
        
        isEnabled = true
        
        layer.borderWidth = 1.5
        layer.borderColor = care_color_white.cgColor
        addTarget(nil, action: #selector(self.click), for: .touchUpInside)
    }
    
    required init?(coder aDecoder: NSCoder) {
        fatalError("init(coder:) has not been implemented")
    }
    
    func click(){
        if (!isFeatured){
            isFeatured = true
            changeColor()
        }
        let superview = self.superview as! FocusSelectView
        superview.click(self.index)
    }
    
    func changeColor(){
        if(isFeatured){
            setTitleColor(.white, for: .normal)
            backgroundColor = care_color_green
        }else{
            setTitleColor(.black, for: .normal)
            backgroundColor = .white
        }
    }
}

class FocusSelectView: UIView{
    var inputField:UITextField!
    let focusRecommendNum = 5
    let focusButtonList:[FocusButton]! = []
    
    var fullSize:CGRect!
    let row_n:Int = 3
    let interval:CGFloat = 10
    let border:CGFloat = 20
    let btn_h:CGFloat = 20
    var btn_w:CGFloat!
    var buttons: [FeatureButton] = []
    var isFeatured: [Bool] = []
    
    var parentViewController: ViewController?
    
    override init(frame: CGRect){
        
        
        
        super.init(frame: frame)
        
        self.fullSize = self.frame
        self.btn_w = (fullSize.width - 2 * border + interval) / CGFloat(row_n) - interval
        
        for index in 0...focusRecommendNum-1{
            
            let pos_x = border + CGFloat(index%row_n) * (btn_w+interval)
            let pos_y = border + CGFloat(index/row_n) * (btn_h+interval)
            let focusBtn = FocusButton(frame: CGRect(x:pos_x, y:pos_y, width: btn_w, height: btn_h), index)
            
            focusButtonList?.append(focusBtn)
            
            self.addSubview(focusBtn)
        }
        print("FocusSelectView init")
        
    }
    
    required init?(coder aDecoder: NSCoder) {
        fatalError("init(coder:) has not been implemented")
    }
    
    func _setParentViewController(_ vc: ViewController){
        self.parentViewController = vc
    }
    
    func updateBtn(_ focusList: [String]){
        
        for index in 0...focusRecommendNum-1{
            focusButtonList[index].setTitle(focusList[index], for: .normal)
            focusButtonList[index].titleLabel!.text = focusList[index]
            focusButtonList[index].changeColor()
//            self.backgroundColor = .red
        }
        print("updateBtn done")
    }
    
    func click(_ index: Int){
//        focusButtonList[index].setTitle("test2", for: .normal)
        
        for i in 0...focusRecommendNum-1{
            if i != index{
                focusButtonList[i].isFeatured = false
                focusButtonList[i].changeColor()
            }
        }
        
        if let focusString = (focusButtonList[index].titleLabel!.text){
            print(focusButtonList[index].titleLabel!.text ?? "no title")
            parentViewController?.setFocusLabel(focus: focusString)
        }
    }
    
    func clearFocusButton(){
        for index in 0...focusRecommendNum-1{
            focusButtonList[index].setTitle("", for: .normal)
            focusButtonList[index].titleLabel!.text = ""
            focusButtonList[index].isFeatured = false
            focusButtonList[index].changeColor()
        }

    }
    
}
