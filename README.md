# Bandwidth Monitoring

This app is for real-time monitoring of the bandwidth usage of PPPoE clients connected on BRAS/BNG - Juniper

## Installation

* [Backend](#Installation-backend)
* [Frontend](#Installation-frontend)
* [Images](#images)


## Installation Backend
Clone the repository and enter the BACKEND folder and run:

#### Install dependencies
```bash
npm install
#or
yarn install
```  
> Change the values in the ```loginJuniper.json``` file according to your device's credentials.

#### To start the backend server run:

```node server.js```



## Installation Frontend

Clone the repository and enter the FRONTEND folder and run:

#### Install dependencies
```bash
yarn install
```  

#### Run on developer mode
```bash
quasar dev
#or
yarn quasar dev
```  
#### To build for production

```bash
quasar build
#or
yarn quasar build
```  
If you are going to run in production mode, change the backend server host in the ```FRONTEND/src/boot/socket.js``` file.
Change the variable ```const socket = io('http://localhost:3000')``` to ```const socket = io('http://YOUR-IP-ADDRES-OR-HOSTNAME:3000' )```

## Images


