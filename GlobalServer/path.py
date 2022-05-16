#add CIF commands to the permanent path by exporting the file path into .bashrc 

import getpass

username = getpass.getuser()
f = open("/home/" + username + "/.bashrc", "a")
f.write('\n' + '\n' + 'export PATH="$PATH:/home/' + username + '/.local/bin"')
f.close()
