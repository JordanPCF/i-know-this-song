//
//  ShowPlaylists.swift
//  i-know-this-song
//
//  Created by Jordan Fleming on 3/26/21.
//

import Foundation
import UIKit

class ShowPlaylists: UIViewController {
    @IBOutlet weak var ListOfPlaylists: UILabel!
    override func viewDidLoad() {
        super.viewDidLoad()
        print("view in ShowPlaylists has loaded")
    }

    func changeText(txt: String) {
        self.ListOfPlaylists.text = txt
    }
    
    @IBAction func testButton(_ sender: UIButton) {
        let api_caller = APIResponse()
//        api_caller.getResponse()
        api_caller.putResponse()
        
        DispatchQueue.main.asyncAfter(deadline: .now() + 2.0) {
            self.changeText(txt: api_caller.response_string)
            print(api_caller.response_string)
        }
        
    }

    
}
