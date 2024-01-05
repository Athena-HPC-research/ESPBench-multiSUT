# Author: Apostolos Halis 2024 <tolishalis@gmail.com>
#!/bin/bash

# Latest Apache Kafka version & tar file, please changes this accordingly
KAFKA_VERSION=3.6.1
KAFKA_TAR=kafka_2.13-3.6.1.tgz
OPENJDK_VERSION=17
FILE="./pass"

# Getting password from the file named pass tha came with this one
# ofcourse this is a bad practice but this is not a production enviroment
if [ -e $FILE ]; then
    while IFS= read -r line; do
        PASSWORD=$line
	echo "Current password: " $PASSWORD
    done < "$FILE"
else
    echo "File not found: $FILE"
fi

######################
#requirements install#
######################
# git
printf "%s" $PASSWORD | sudo -S apt install git 

# openjdk
printf "%s" $PASSWORD | sudo -S apt install openjdk-$OPENJDK_VERSION-jre

# sbt
echo "deb https://dl.bintray.com/sbt/debian/" | sudo tee -a /etc/apt/sources.list.d/sbt.list
printf "%s" $PASSWORD | sudo -S apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv 2EE0EA64E40A89B84B2DF73499E82A75642AC823
printf "%s" $PASSWORD | sudo -S apt update
printf "%s" $PASSWORD | sudo -S apt install sbt

# I wronngly named my nodes controller, this part should be removed if you correctly named your nodes
printf "%s" $PASSWORD | sudo -S usermod -l benchmarker controller

#printf $PASSWORD | sudo -S printf $PASSWORD | passwd --stdin benchmarker

# Add user to sudo group, again you may have done that already, comment this
printf "%s" $PASSWORD | sudo -S adduser benchmarker sudo

# Finishing up, you can now use the scipt like normal to every configuration
printf "%s" $PASSWORD | su -c benchmarker

# Noticed there are no home folders 
mkdir ~/Downloads

##################
#installing Kafka#
##################
echo "Installing Apache Kafka version: $KAFKA_VERSION" 
curl "https://downloads.apache.org/kafka/$KAFKA_VERSION/$KAFKA_TAR" -o ~/Downloads/$KAFKA_TAR
printf "%s" $PASSWORD | sudo -S tar -xvzf ~/Downloads/$KAFKA_TAR /opt/ --strip 1

########################
#making Kafka a service#
########################
echo "Starting Apache Kafka as service" 
printf "%s" $PASSWORD | sudo -S apt install policykit-1
cp tools/configuration/kafka/etc/init.d/kafka /etc/init.d/
update-rc.d kafka defaults

#####################
#installing ESPBench#
#####################
echo "Installing ESPBench-multiSUT" 
mkdir ~/Benchmarks 
git clone https://github.com/TolisSth/ESPBench-multiSUT.git ~/Benchmarks/
printf "%s" $PASSWORD | sudo -S apt install sbt
sbt assembly ~/Benchmarks/ESPBench-multiSUT/
