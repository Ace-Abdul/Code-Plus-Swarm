#create configuration file for CIF, name it cif.yml, and provide the token and remote host. 

f = open(".cif.yml", "w")
f.write("token: cfe7bf9c67ff38fc4b01424abfce57278fee9e40006d576553d2d471f20a9c3f7af46b57fcb49ff0" + "\n" + "remote: https://public-cif-stingar.security.duke.edu/")
f.close()
