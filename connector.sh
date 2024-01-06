# Author: Apostolos Halis 2024 <tolishalis@gmail.com>
#!/bin/bash

# List nodes here
# Please change according to your configuaration
USER=controller
NODES=("controller@192.168.122.213" "controller@192.168.122.187" "controller@192.168.122.163") 

# I made my machines share the same password, even though it promotes poor securtiy
# I suggest the same, just because this is not a production grade enviroment
rm pass
read -p "Password of machines: " PASSWORD
echo $PASSWORD >> pass 

# Looping through nodes
for NODE in "${NODES[@]}"; do 
	echo "Connecting on node: " $NODE
	scp -r "./execution.sh" "./pass" "$NODE:/home/$USER/"
	ssh $NODE 'bash -s' < "execution.sh"
done

