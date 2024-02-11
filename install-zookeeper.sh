sudo adduser zookeeper
su - zookeeper
# do all of this as zookeeper user
wget https://archive.apache.org/dist/zookeeper/zookeeper-3.4.12/zookeeper-3.4.12.tar.gz
tar -xzvf zookeeper-3.4.12.tar.gz
echo export ZOO_LOG_DIR=/var/log/zookeeper >> ~/.bashrc
source ~/.bashrc
sudo mkdir /var/lib/zookeeper ; cd /var/lib ; sudo chown zookeeper:zookeeper zookeeper/
sudo mkdir /var/log/zookeeper ; cd /var/log ; sudo chown zookeeper:zookeeper zookeeper/

# different for each node
sudo sh -c "echo '1' > /var/lib/zookeeper/myid"
cd zookeeper-3.4.13/conf/
cp zoo_sample.cfg zoo.cfg
nano zoo.cfg
# those node1-3 names should be in /etc/hosts
# dataDir=/var/lib/zookeeper
# server.1=node1:2888:3888
# server.2=node2:2888:3888
# server.3=node3:2888:3888
# configure zookeeper to your liking
nano log4j.properties
# zookeeper.log.dir=/var/log/zookeeper
# zookeeper.tracelog.dir=/var/log/zookeeper
# log4j.rootLogger=INFO, CONSOLE, ROLLINGFILE

sudo ./bin/zkServer.sh  start

# for test
# echo stat | nc node1 2181
# echo mntr | nc node1 2181
# echo srvr | nc localhost 2181


