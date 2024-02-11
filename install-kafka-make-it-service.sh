wget https://archive.apache.org/dist/kafka/2.3.0/kafka_2.11-2.3.0.tgz
mv kafka_2.11-2.3.0 kafka
sudo mv kafka /opt/
# should be run inside the project, can change this to handle it
sudo cp tools/configuration/configurations/kafka_2.12-2.3.0/* /opt/kafka/config

# Make Apache Kafka a service: 
sudo apt install policykit-1
sudo cp tools/configuration/kafka/etc/init.d/kafka /etc/init.d
# will ask for password and user
update-rc.d kafka defaults
