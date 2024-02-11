wget https://archive.apache.org/dist/spark/spark-2.4.4/spark-2.4.4-bin-hadoop2.7.tgz
tar -xzf spark-2.4.4-bin-hadoop2.7.tgz
mv spark-2.4.4-bin-hadoop2.7 spark
sudo mv spark /opt/
sudo cp tools/configuration/configurations/spark-2.4.4-bin-hadoop2.7/* /opt/spark/conf/
echo "export PATH=/opt/spark/bin:\$PATH" >> ~/.bashrc
source ~/.bashrc
