import paramiko
import time
import sys
import re
import socketio
import json

sio = socketio.Client()
username = sys.argv[1]
durationTime = int(sys.argv[2])
clienteId = sys.argv[3]
uploadData = []
downloadData = []


def GetInterfaceName(dados, ssh):
    for linha in dados:
        if 'pp0' in linha:
            interface = linha.split(' ')[0]
            return interface

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
            uploadData.append(inputBW)
            downloadData.append(outputBW)
            sio.emit('RunningTest', {'id': clienteId, 'upload': inputBW, 'download': outputBW, 'minUpload': min(uploadData), 'minDownload': min(downloadData), 'maxUpload': max(
                uploadData), 'maxDownload': max(downloadData), 'mediaUpload': round(sum(uploadData)/len(uploadData), 2), 'mediaDownload': round(sum(downloadData)/len(downloadData), 2)})
            break
    return


def main():

    try:

        sio.connect('http://localhost:3000')

    except Exception:
        print('Erro ao conectar', Exception)

    try:
        
        with open('loginJuniper.json', "r") as handler:
            login = json.load(handler)
            host = login['host']
            user = login['user']
            password = login['password']
            port = login['port']

        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(host, username=user, password=password, port=port)

        stdin, stdout, stderr = ssh.exec_command(
            f'show subscribers user-name {username} | no-more\n'.encode('utf-8'))
        time.sleep(.3)
        return_username = stdout.readlines()

        interfaceName = GetInterfaceName(return_username, ssh)
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

            if time.time() > inicial+durationTime+4:
                sio.emit('FinishTest', {'id': clienteId, 'status': 'sucesso',
                                        'message': 'Teste encerrado!'})
                executando = False

        ssh.close()
        sio.disconnect()

    except Exception as e:
        print(e)
        sys.exit()


if __name__ == "__main__":
    main()
