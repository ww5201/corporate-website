import paramiko
import sys

c = paramiko.SSHClient()
c.set_missing_host_key_policy(paramiko.AutoAddPolicy())
c.connect("8.138.218.146", 22, "root", "ww0987654.")

# Check node version
stdin, stdout, stderr = c.exec_command("node --version")
print("Node:", stdout.read().decode().strip())

# Check if payment route is actually mounted
cmd = """cd /root/backend && node -e "
const express = require('express');
const paymentRouter = require('./routes/payment');
console.log('Router type:', typeof paymentRouter);
console.log('Router stack length:', paymentRouter.stack ? paymentRouter.stack.length : 'no stack');
if (paymentRouter.stack) {
  paymentRouter.stack.forEach((l, i) => {
    console.log(i, l.route ? l.route.path : 'middleware', l.route ? Object.keys(l.route.methods) : '');
  });
}
"
"""
stdin, stdout, stderr = c.exec_command(cmd)
print(stdout.read().decode('utf-8', 'replace'))
err = stderr.read().decode('utf-8', 'replace')
if err:
    print("STDERR:", err)

c.close()
