SWARM, or the Shared Warning for Attack Response Management, aims to protect home users and small businesses from malicious traffic by pulling from the Duke STINGAR threat intelligence feed, which contains dangerous IP addresses that have tried to attack Duke's network. Using the pfSense firewall and pfBlockerNG package, IP addresses from STINGAR can be blocked from users' home networks. 

There are two servers: one is a local server on a user's pfSense network to display blocked IP statistics, and the other is an global admin server from which pfBlockerNG will pull a blocklist.

For the local user server, pfSense will likely need to come preinstalled with the LocalServer folder. Shell scripts and Python scripts will automate the necessary installation to boot up the server. Once the server is running, statCompiler.py will compile the blocked IP data from pfBlockerNG's native unified.log, feed variables into app.py, render an html template using those variables, and display the appropriate data on a webpage only accessible within the home user's network. Users should first log in with the default username and password (username: user, password: pfsense). They are then directed to change their password and relogin to access the webpage to see statistics about their local network activity. 

For the global admin server, shell scripts and Python scripts will automate installing and pulling IP addresses from CIF and setting up a global server. The IP list updates every minute to give users the most protection. Users should be able to access this global server with their individual authentication token to see the malicious IP list. There will also be an admin interface, where admin will be able to generate tokens for approved home users to access the global server. Admin will also be able to add co-admins and modify users' information, such as password and token.


![Updated_Diagram](/uploads/a07fb9da9bc3a273d45f1226ab347859/Updated_Diagram.png)

Students: Ace Abdul, Sonya Patel, Brooks Robinson, Connie Vi, and Eric Xie
