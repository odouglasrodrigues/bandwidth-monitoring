import paramiko
import time
import sys
import re
import socketio


sio = socketio.Client()
try:
    sio.connect('http://localhost:3000')
except Exception :
    print('Erro ao conectar', Exception)

username = sys.argv[1]
clienteId = sys.argv[2]

def GetInterfaceName(dados):
    for linha in dados:
        if 'pp0' in linha:
            interface = linha.split(' ')[0]
            return interface

def GetBandwidthUsage(dados):
    for linha in dados:
        if 'Input' in linha and 'bps' in linha:
            s = linha.strip().replace(' ', ";")
            input = re.sub(r';[0-9]+;;', '', s).replace(';','').split(':')[1].replace('bps', '')

            inputBW=round(int(input)/1000/1000, 2)

            
        if 'Output' in linha and 'bps' in linha:
            s = linha.strip().replace(' ', ";")
            output = re.sub(r';[0-9]+;;', '', s).replace(';','').split(':')[1].replace('bps', '')

            outputBW=round(int(output)/1000/1000, 2)

            sio.emit('RunningTest', {'id':clienteId, 'upload':inputBW, 'download':outputBW})
            break
    return

ssh = paramiko.SSHClient()

ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

ssh.connect('45.189.223.0', username='douglas.rodrigues', password='thmpv77d6f', port=9824)


stdin, stdout, stderr = ssh.exec_command(f'show subscribers user-name {username} | no-more\n'.encode('utf-8'))
time.sleep(.3)
return_username = stdout.readlines()

interfaceName = GetInterfaceName(return_username)


executando = True

inicial=time.time()        

while executando:
    stdin, stdout, stderr = ssh.exec_command(f'show interfaces {interfaceName} statistics detail | no-more\n'.encode('utf-8'))

    time.sleep(.3)

    return_bandwidth = stdout.readlines()

    GetBandwidthUsage(return_bandwidth)

    if time.time()> inicial+10:
        executando = False



ssh.close()
sio.disconnect()