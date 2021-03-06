//
//  ViewController.swift
//  i-know-this-song
//
//  Created by Jordan Fleming on 3/22/21.
//

import Amplify
import AmplifyPlugins
import UIKit

class ViewController: UIViewController {

    override func viewDidLoad() {
        super.viewDidLoad()
        

//        let an_api_call = RESTAPIResponse()
//        an_api_call.getResponse()
//
//        print(an_api_call.response_string)
//        DispatchQueue.main.asyncAfter(deadline: .now() + 3.0) {
//            print(an_api_call.response_string)
//        }
    }
}


class RESTAPIResponse {
    var response_string : String
    
    init() {
        self.response_string = ""
    }
    
    func getResponse() {
        let queryParameters = ["action": "increment", "number": "3"]
        let request = RESTRequest(path: "/api", queryParameters: queryParameters)
        
        Amplify.API.get(request: request) { result in
            switch result {
            case .success(let data):
                self.response_string = String(decoding: data, as: UTF8.self)
                print("Success \(self.response_string)")
            case .failure(let apiError):
                switch apiError {
                case .httpStatusError(_, let response):
                    print("\(response.statusCode)")
                default:
                    print("No response from server")
                }
            }
        }
    }
    
    func putResponse() {
        let queryParameters = ["num": "3"]
        let request = RESTRequest(path: "/api", queryParameters: queryParameters)
        
        Amplify.API.put(request: request) { result in
            switch result {
            case .success(let data):
                self.response_string = String(decoding: data, as: UTF8.self)
                print("Success \(self.response_string)")
            case .failure(let apiError):
                switch apiError {
                case .httpStatusError(_, let response):
                    print("\(response.statusCode)")
                default:
                    print("No response from server")
                }
            }
        }
    }
}

