import paramiko
import time
import sys
import re
import socketio


sio = socketio.Client()
try:
    sio.connect('http://localhost:3000')
except Exception:
    print('Erro ao conectar', Exception)

username = sys.argv[1]
durationTime = int(sys.argv[2])
clienteId = sys.argv[3]


def GetInterfaceName(dados):
    for linha in dados:
        if 'pp0' in linha:
            interface = linha.split(' ')[0]
            return interface

    print('Passou aqui')
    sio.emit('ErrorTest', {'id': clienteId, 'status': 'erro',
                           'message': 'O Usuário informado não está conectado'})
    ssh.close()
    sio.disconnect()
    sys.exit()


def GetBandwidthUsage(dados):
    for linha in dados:
        if 'Input' in linha and 'bps' in linha:
            s = linha.strip().replace(' ', ";")
            input = re.sub(r';[0-9]+;;', '', s).replace(';',
                                                        '').split(':')[1].replace('bps', '')

            inputBW = round(int(input)/1000/1000, 2)

        if 'Output' in linha and 'bps' in linha:
            s = linha.strip().replace(' ', ";")
            output = re.sub(r';[0-9]+;;', '', s).replace(';',
                                                         '').split(':')[1].replace('bps', '')

            outputBW = round(int(output)/1000/1000, 2)

            sio.emit('RunningTest', {'id': clienteId,
                     'upload': inputBW, 'download': outputBW})
            break
    return


ssh = paramiko.SSHClient()

ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

ssh.connect('45.189.223.0', username='douglas.rodrigues',
            password='thmpv77d6f', port=9824)


stdin, stdout, stderr = ssh.exec_command(
    f'show subscribers user-name {username} | no-more\n'.encode('utf-8'))
time.sleep(.3)
return_username = stdout.readlines()

interfaceName = GetInterfaceName(return_username)


executando = True

inicial = time.time()

while executando:
    stdin, stdout, stderr = ssh.exec_command(
        f'show interfaces {interfaceName} statistics detail | no-more\n'.encode('utf-8'))

    time.sleep(.5)
    return_bandwidth = stdout.readlines()
    time.sleep(.5)
    GetBandwidthUsage(return_bandwidth)
    time.sleep(.5)

    if time.time() > inicial+durationTime+3:
        sio.emit('FinishTest', {'id': clienteId, 'status': 'sucesso',
                 'message': 'Teste encerrado!'})
        executando = False


ssh.close()
sio.disconnect()
