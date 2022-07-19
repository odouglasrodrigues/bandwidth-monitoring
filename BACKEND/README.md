# Bandwidth Monitoring

This app is for real-time monitoring of the bandwidth usage of PPPoE clients connected on BRAS/BNG - Juniper

## Installation

Clone the repository and enter the BACKEND folder and run:

#### Install dependencies
```bash
#Node JS dependencies

npm install
#or
yarn install


#Python dependencies

pip install paramiko
pip install "python-socketio[client]"

```  
> Change the values in the ```loginJuniper.json``` file according to your device's credentials.

#### To start the backend server run:

```node server.js```

