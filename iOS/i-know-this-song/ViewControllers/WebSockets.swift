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
    
    func listen(completion: @escaping (String) -> ()) {
        webSocketTask!.receive { result in
            switch result {
            case .failure(let error):
                print(error)
            case .success(let message):
                switch message {
                case .string(let text):
                    completion(text)
                case .data(let data):
                    completion("Received data object not String")
                @unknown default:
                    fatalError()
                }
            }
        }
    }
    
    func getPlaylists(completion: @escaping () -> ()) {
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
            completion()
        }
    }
    
    func sendLyricQuery(playlists: String, query: String, completion: @escaping () -> ()) {
        let dic = ["action": "makeRequest", "requestType": "lyrics", "lyrics": "\(query)", "playlists": "\(playlists)"]
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
            completion()
        }
    }
}
    

