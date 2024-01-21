# Author: Apostolos Halis 2024 <tolishalis@gmail.com>
#!/bin/bash

# List nodes here
# Please change according to your configuaration
USER=benchmarker
NODES=("benchmarker@192.168.122.77" "benchmarker@192.168.122.77" "benchmarker@192.168.122.77") 

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

