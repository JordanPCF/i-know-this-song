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
        
        var socketConnection = WebSocketTaskConnection(url: URL(string: "wss://l7pgtq5sw5.execute-api.us-west-2.amazonaws.com/production")!)
        socketConnection.connect()
//        socketConnection.send(text: "Hello")
        socketConnection.getPlaylists { responseString in
//            print("callback: ", responseString)
            print("socket response:", socketConnection.response)
        }
//        print(socketConnection.response)

//        DispatchQueue.main.asyncAfter(deadline: .now() + 20.0) {
//            print("response: ")
//            print(socketConnection.response)
//        }
        
    }

    func changeText(txt: String) {
        self.ListOfPlaylists.text = txt
    }
    
    @IBAction func testButton(_ sender: UIButton) {
//        let api_caller = RESTAPIResponse()
//        api_caller.putResponse()
//
//        DispatchQueue.main.asyncAfter(deadline: .now() + 2.0) {
//            self.changeText(txt: api_caller.response_string)
//            print(api_caller.response_string)
//        }
        
    }

    
}
