//
//  WebSockets.swift
//  i-know-this-song
//
//  Created by Jordan Fleming on 4/5/21.
//

import Foundation



class WebSocketTaskConnection: NSObject {
    var webSocketTask: URLSessionWebSocketTask?
    var urlSession: URLSession!
    let delegateQueue = OperationQueue()
    var response: String
    
    init(url: URL) {
//        super.init()
//        urlSession = URLSession(configuration: .default, delegate: self, delegateQueue: delegateQueue)
        urlSession = URLSession(configuration: .default)
        webSocketTask = urlSession.webSocketTask(with: url)
        
        self.response = ""
    }
    
    func connect() {
        webSocketTask!.resume()
        
//        self.listen()
    }
    
    func disconnect() {
        webSocketTask!.cancel(with: .goingAway, reason: nil)
    }
    
    func send(text: String) {
        let dic = ["action": "sendMessage", "message": text]
        do {
            let jsonData = try JSONSerialization.data(withJSONObject: dic)
            let jsonString = String(data: jsonData, encoding: String.Encoding.ascii)!
            let message = URLSessionWebSocketTask.Message.string(jsonString)
            
            webSocketTask?.send(message) { error in
                if let error = error {
                    print(error)
                }
            }
        } catch {
            print(error)
        }
    }
    
    func listen(completion: @escaping (String) -> ()) {
        var response_text = ""
        webSocketTask!.receive { result in
            switch result {
            case .failure(let error):
                print(error)
            case .success(let message):
                switch message {
                case .string(let text):
                    response_text = text
                    completion(response_text)
                case .data(let data):
                    print("data is ", data)
                @unknown default:
                    fatalError()
                }
                
//                self.listen()
            }
        }
//        print("about to return")
        
//        return response_text
    }
    
    func getPlaylists(completion: @escaping (String) -> ()) {
        let dic = ["action": "makeRequest", "requestType": "playlists"]
        do {
            let jsonData = try JSONSerialization.data(withJSONObject: dic)
            let jsonString = String(data: jsonData, encoding: String.Encoding.ascii)!
            let message = URLSessionWebSocketTask.Message.string(jsonString)
            
            webSocketTask?.send(message) { error in
                if let error = error {
                    print(error)
                }
            }
        } catch {
            print(error)
        }

        listen(){response_text in
            self.response = response_text
            completion(response_text)
        }

    }
}
    

