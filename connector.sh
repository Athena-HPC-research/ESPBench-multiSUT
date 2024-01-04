# Author: Apostolos Halis 2024 <tolishalis@gmail.com>
#!/bin/bash

# List nodes here
# Please change according to your configuaration
USER=controller 
NODES=("controller@192.168.122.213" "controller@192.168.122.187" "controller@192.168.122.163") 

# Looping through nodes
for NODE in "${NODES[@]}"; do 
	scp "./execution.sh" "$NODE:/home/$USER/"
	ssh $NODE 'bash -s' < "execution.sh"
done

