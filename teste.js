const shell = require('shelljs')

const cmd = `python conn.py deltaescritorio`

console.log('Execução do JS', shell.exec(cmd))