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
    
    override init(frame: CGRect) {
        self.isFeatured = false
        
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
        isFeatured = !isFeatured
        changeColor()
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

class FeatureButtonView: UIScrollView{
    var featureList = [String]()
    
    override init(frame: CGRect){
        super.init(frame: frame)
        
        backgroundColor = .white
    }
    
    required init?(coder aDecoder: NSCoder) {
        fatalError("init(coder:) has not been implemented")
    }
    
    func setFeatureList(featureList: [String]){
        self.featureList = featureList
        setFeatureButton()
    }
    
    let fullSize = UIScreen.main.bounds.size
    let row_n:Int = 4
    let interval:CGFloat = 10
    let border:CGFloat = 20
    let btn_h:CGFloat = 20
    var btn_w:CGFloat!
    
    func setFeatureButton(){
        btn_w = (fullSize.width - 2 * border + interval) / CGFloat(row_n) - interval
        
        for (index, feature) in featureList.enumerated(){
            let pos_x = border + CGFloat(index%row_n) * (btn_w+interval)
            let pos_y = border + CGFloat(index/row_n) * (btn_h+interval)
            let button = FeatureButton(frame: CGRect(x:pos_x, y:pos_y, width: btn_w, height: btn_h))
            button.setTitle(feature, for: .normal)
            self.addSubview(button)
        }
    }
    
}
