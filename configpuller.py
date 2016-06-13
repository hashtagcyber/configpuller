#!/usr/bin/env python
import paramiko
import time
import sys
import socket
if len(sys.argv) != 3:
   print 'Usage is ./configpuller.py <hosts.list> <command.list>'
   sys.exit(1)

cmdlist=sys.argv[2]
hostlist=sys.argv[1]
#cmdlist=['terminal len 0','show run','show ip int brief']
def getdata(hostname):
   buff = sshshell.recv(1000)
   buff2= buff
   while len(buff) == 1000:
      buff = sshshell.recv(1000)
      buff2 +=buff
   f=open(hostname+'.results.txt','a')
   f.write(buff2 + '\n')
  # print buff2

def sendcmd(execute):
   sshshell.send("\n")
   sshshell.send(execute)
   time.sleep(2)

def gototown(server):
   hostname=server
#   print hostname
   ip = (socket.gethostbyname_ex(hostname))[2][0]
   sshclient=paramiko.SSHClient()
   sshclient.set_missing_host_key_policy(paramiko.AutoAddPolicy())
   sshclient.connect(ip, username=username, password=password, look_for_keys=False, allow_agent=False)
   print "SSH Connection established to %s" % hostname
   global sshshell
   sshshell = sshclient.invoke_shell()
   #print "Running Commands"
   #Comment out lines if you don't need enable mode
   #Update password if you do need to escalate
   sshshell.send('enable\n')
   sshshell.recv(10000)  
 #getdata(server)
   sshshell.send('password\n')
   sshshell.recv(1000)
  # getdata(server)
   doit=open(cmdlist,'r')
   for line in doit:
      print 'Executing command: ' + line
      sendcmd(line+'\n')
      getdata(server)
   doit.close()
   print 'Commands Complete, Closing Connection'
   sendcmd('exit\n')
   sshshell.close()

if __name__ == '__main__':
#   ip=raw_input('Target Device IP')
   username=raw_input('Username: ')
   password=raw_input('Password: ')
   hosts=open(hostlist,'r')
   for line in hosts:
      try:
         gototown(line.rstrip())
      except:
         print 'Error connecting to %s' % line.rstrip()
         pass
   print 'Finished... Check the current directory for results.txt'
   hosts.close()
   exit()
