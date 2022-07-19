## Installation

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

#### Initial Screen
![Initial_Screen](/images/initial.png?raw=true "Initial")

#### Chart Screen
![Chart_Screen](/images/chart.png?raw=true "Chart")
