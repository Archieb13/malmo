# ------------------------------------------------------------------------------------------------
# Copyright (c) 2016 Microsoft Corporation
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and
# associated documentation files (the "Software"), to deal in the Software without restriction,
# including without limitation the rights to use, copy, modify, merge, publish, distribute,
# sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all copies or
# substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT
# NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
# DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
# ------------------------------------------------------------------------------------------------

# Used for integration tests.

import os
import platform
import socket
import subprocess
import sys
import time

sys.stdout = os.fdopen(sys.stdout.fileno(), 'w', 0)  # flush print output immediately
minecraft_path = os.path.dirname(os.path.abspath(__file__))

def PortHasListener( port ):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    result = sock.connect_ex( ('127.0.0.1',port) )
    sock.close()
    return result == 0

ports = [int(port_arg) for port_arg in sys.argv[1:]]
if len(ports) == 0:
    ports = [10000] # Default

for port in ports:
    if PortHasListener( port ):
        print 'Something is listening on port',port,'- will assume Minecraft is running.'
        continue
        
    print 'Nothing is listening on port',port,'- will attempt to launch Minecraft from a new terminal.'
    if os.name == 'nt':
        subprocess.Popen([minecraft_path + '/launchClient.bat', '-port', str(port)], creationflags=subprocess.CREATE_NEW_CONSOLE, close_fds=True)
    elif sys.platform == 'darwin':
        subprocess.Popen(['open', '-a', 'Terminal.app ' + minecraft_path + '/launchClient.sh', '-port', str(port)])
    elif platform.linux_distribution()[0] == 'Fedora':
        subprocess.Popen( minecraft_path + "/launchClient.sh -port " + str(port), close_fds=True, shell=True, stdin = subprocess.PIPE, stdout = subprocess.PIPE, stderr = subprocess.PIPE )
    else:
        subprocess.Popen( minecraft_path + "/launchClient.sh -port " + str(port), close_fds=True, shell=True, stdin = subprocess.PIPE, stdout = subprocess.PIPE, stderr = subprocess.PIPE )
    print 'Giving Minecraft some time to launch... '
    launched = False
    for i in xrange( 100 ):
        print '.',
        time.sleep( 3 )
        if PortHasListener( port ):
            print 'ok'
            launched = True
            break
    if not launched:
        print 'Minecraft not yet launched. Giving up.'
        exit(1)
