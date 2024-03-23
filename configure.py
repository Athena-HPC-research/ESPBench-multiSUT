import json
import sys
def read_json_into_dict(filename):
    with open(filename,'r') as f:
        return json.load(f)
def print_string_with_filename_and_separator(filename,content):
    print(f"===========File: {filename} =============")
    print(content)
    print("-------------------------------------------")
def get_string_from_ip_port_list(ip_port_tuple_list,default_port):
    total_string = ""
    for ip_port in ip_port_tuple_list:
        if(len(ip_port) != 2):
            port = default_port
        else:
            port = ip_port[1]
        server = ip_port + ":" + str(port)
        total_string += server + ","
    return total_string

def string_array_from(elems):
    total_string = "[" + "\n"
    for i in elems:
        total_string += "\t" + wrap_string(i) + "," +"\n"
    # get rid of the extra comma
    total_string = total_string[:-2] + "\n"
    return total_string + "\t"+ "]"

def generate_file_in(content,path):
    with open(path,'w') as file:
        file.write(content)
def obj(obj_to_output,tabs):
    total_string = ((tabs-1) * "\t") + "{" + "\n"
    for property_name,property_value in obj_to_output.items():
        val = property_value
        if isinstance(val,str):
            val = wrap_string(val)
        # can add support for more later
        total_string = total_string + (tabs * "\t") + property_equals(property_name,val) + "\n"
    return total_string + ((tabs-1) * "\t") + "}"
def property_equals(property_name, val):
    return f"{property_name} = {val}"

def wrap_string(string):
    return f'"{string}"'
def kafka_key_serializer_class():
    return "org.apache.kafka.common.serialization.StringSerializer"
def kafka_value_serializer_class():
    return "org.apache.kafka.common.serialization.StringSerializer"

def ansible_host(machine_name,ip):
    return f"{machine_name} ansible_host={ip}"

def read_from_json(filename):
    return json.load(filename)



class DatasenderConf:
    def __init__(self,info_json,write_to_file=False):
        self.to_file = write_to_file
        self.json = info_json

        self.file_path = "./tools/datasender/datasender.conf"
        self.label = "datasender.conf"
        self.description = "Provides the kafka config to the datasender and the giant csv files that are meant to be streamed"

    def file_content(self,ip_port_tuple_list,input_paths=["~/Benchmarks/ESB/Data/5MinutesMachine1.csv",
	"~/Benchmarks/ESB/Data/5MinutesMachine2.csv",
	"~/Benchmarks/ESB/Data/production_times.csv"],read_in_ram=True):
    #i am including a comma more than needed
        kafka_bootstrap_servers = get_string_from_ip_port_list(ip_port_tuple_list,9092)
        input_paths_arr = string_array_from(input_paths)
        content = f"""
        kafka-producer-config.bootstrap-servers = {wrap_string(kafka_bootstrap_servers)}
        kafka-producer-config.key-serializer-class = {wrap_string(kafka_key_serializer_class())}
        kafka-producer-config.value-serializer-class = {wrap_string(kafka_value_serializer_class())}
        kafka-producer-config.acks = 1
        kafka-producer-config.batch-size = 16384
        kafka-producer-config.buffer-memory-size = 33554432
        kafka-producer-config.linger-time = 0
        data-reader-config.data-input-path = {input_paths_arr}
        data-reader-config.read-in-ram = false
        """
        return content

    def read_from_json(self):
        # in self.json should be the file string, or the parsed thing to only do it once
        return "",""

    def output_file(self):
        args_for_file = self.read_from_json()
        file_content=""
        if self.to_file:
            generate_file_in(file_content,self.file_path)
        else:
            print_string_with_filename_and_separator(self.label,file_content)
class DatasenderAppConf:
    def __init__(self,info_json,write_to_file=False):
        self.to_file = write_to_file
        self.json = info_json
        self.file_path = "./tools/datasender/src/main/resources/application.conf"
        self.label = "Datasender application.conf"
        self.description = "Provides the database info for the datasender to connect"

    def file_content(self,db_name,db_user,db_password,server_name,num_threads=20):

        return f"""
        postgres = {{
            dataSourceClass = "org.postgresql.ds.PGSimpleDataSource"
            properties = {{
                databaseName = "{db_name}"
                user = "{db_user}"
                password = "{db_password}"
                serverName = "{server_name}"
            }}
            numThreads = {num_threads}
        }}
        """

    def read_from_json(self):
        #the parsed thing to only do it once
        db_info = self.json["database"]
        return db_info["db_name"],db_info["db_user"],db_info["db_password"],db_info["server_name"],20

    def output_file(self):
        db_name,db_user,db_password,server_name,num_threads = self.read_from_json()
        file_content=self.file_content(db_name,db_user,db_password,server_name,num_threads)
        if self.to_file:
            generate_file_in(file_content,self.file_path)
        else:
            print_string_with_filename_and_separator(self.label,file_content)

class TpcGenPropertiesConf:
    def __init__(self,info_json,write_to_file=False):
        self.to_file = write_to_file
        self.json = info_json

        self.file_path = "./tools/tpc-c_gen/tpc-c.properties"
        self.label = "tpc-c.properties"
        self.description = "For the generation of the business data it provides the number of warehouses and in what folder to output the data"

    def file_content(self,number_of_warehouses,output_dir):
        return f"""
        NUMBER_OF_WAREHOUSES={number_of_warehouses}
        OUTPUT_DIR={output_dir}
        """

    def read_from_json(self):
        #the parsed thing, just do self.json["prop"]
        return "",""

    def output_file(self):
        args_for_file = self.read_from_json()
        file_content=""
        if self.to_file:
            generate_file_in(file_content,self.file_path)
        else:
            print_string_with_filename_and_separator(self.label,file_content)


class AnsibleHostsConf:
    def __init__(self,info_json,write_to_file=False):
        self.to_file = write_to_file
        self.json = info_json

        self.file_path = "./tools/configuration/hosts"
        self.label = "hosts"
        self.description = "Ansible hosts file, provides the IP for all the subsystems of the benchmark"

    def file_content(self,spark_m,spark_servers,kafka_ips,db_ip):
        index = 1;
        # need to somehow create a lambda that modifies the index
        machine_prefix = "bench"
        spark_master = ansible_host(machine_prefix + "0" + str(index),spark_m)
        spark_slaves_str = ""
        for spark_host in spark_servers:
            index = index + 1
            spark_slaves_str = spark_slaves_str + ansible_host(machine_prefix + "0" + str(index),spark_host) + "\n"
        kafka_str = ""
        for kafka_host in kafka_ips:
            index = index + 1
            kafka_str = kafka_str + ansible_host(machine_prefix + "0" + str(index),kafka_host) + "\n"
        index = index + 1
        db_host = ansible_host(machine_prefix + "0" + str(index),db_ip)

        return f"""
[all_nodes:children]
streaming_cluster
kafka_cluster
erp_db

[streaming_cluster:children]
master
slaves

[master]
{spark_master}

[slaves]
{spark_slaves_str}

[kafka_cluster]
{kafka_str}

[erp_db]
{db_host}
"""

    def read_from_json(self):
        # in self.json should be the file string, or the parsed thing to only do it once
        spark_ips = self.json["spark"]["servers"]
        spark_master = self.json["spark"]["master"]
        db_ip = self.json["database"]["server"]
        kafka = self.json["kafka"]["servers"]
        return spark_master,spark_ips,kafka,db_ip

    def output_file(self):
        spark_m,spark_ips,kafka,db_ip = self.read_from_json()
        file_content= self.file_content(spark_m,spark_ips,kafka,db_ip)
        if self.to_file:
            generate_file_in(file_content,self.file_path)
        else:
            print_string_with_filename_and_separator(self.label,file_content)

class ESPBenchCommonsConf:
    def __init__(self,info_json,write_to_file=False):
        self.to_file = write_to_file
        self.json = info_json

        self.file_path = "./tools/commons/commons.conf"
        self.label = "commons.conf"
        self.description = "Provides the actual ESPBench configuration, not the tools, but the whole benchmark, how many runs, queries etc."

    def file_content(self,topic_prefix,benchmark_run,query_configs_arr,kafka_bootstrap_servers,zookeeper_servers,sending_interval=10000000,sending_interval_time_unit="NANOSECONDS",duration=10,duration_time_unit="Minutes"):
        kafka_servers = ",".join(list(map(lambda x: f"{x}:9092",kafka_bootstrap_servers)))
        zookeeper = ",".join(list(map(lambda x: f"{x}:2181",zookeeper_servers)))
        if query_configs_arr == None:
            queries = ""
        else:
            queries = ",\n".join(list(map(lambda x: obj(x,2),query_configs_arr)))
        query_configs_str = "[" + "\n" + queries + "\n"+ "  ]"
        return f"""
        topic-prefix = {wrap_string(topic_prefix)}
        benchmark-run = {benchmark_run}
        query-configs = {query_configs_str}
        sending-interval = {sending_interval}
        sending-interval-time-unit = {wrap_string(sending_interval_time_unit)}
        duration = {duration}
        duration-time-unit = {wrap_string(duration_time_unit)}
        kafka-bootstrap-servers = {wrap_string(kafka_servers)}
        zookeeper-servers = {wrap_string(zookeeper)}
        """

    def read_from_json(self):
        # in self.json should be the file string, or the parsed thing to only do it once
        topic_prefix = self.json["benchmark"]["topic-prefix"]
        benchmark_run = self.json["benchmark"]["benchmark-run"]
        sending_interval = self.json["benchmark"]["sending-interval"]
        sending_interval_time_unit = self.json["benchmark"]["sending-interval-time-unit"]
        duration = self.json["benchmark"]["duration"]
        duration_time_unit = self.json["benchmark"]["duration-time-unit"]
        kafka_servers = self.json["kafka"]["servers"]
        zookeeper_servers = self.json["zookeeper"]["servers"]
        queries = self.json["benchmark"]["queries"]
        return topic_prefix,benchmark_run,queries,sending_interval,sending_interval_time_unit,duration,duration_time_unit,kafka_servers,zookeeper_servers

    def output_file(self):
        t_prefix,b_run,queries,s_interval,s_interval_time_unit,d,d_time_unit,kafka,zookeeper = self.read_from_json()
        file_content=self.file_content(t_prefix,b_run,queries,kafka,zookeeper,s_interval,s_interval_time_unit,d,d_time_unit)
        if self.to_file:
            generate_file_in(file_content,self.file_path)
        else:
            print_string_with_filename_and_separator(self.label,file_content)

class ApacheBeamConf:
    def __init__(self,info_json,write_to_file=False):
        self.to_file = write_to_file
        self.json = info_json
        self.file_path = "./implementation/beam/src/main/resources/beam.properties"
        self.label = "beam.properties"
        self.description = "Provides all the needed data to the SUT(db->url,user,password,kafka-servers->IPs) and what system to use(Spark,HazelCast) and where is the master of that system->IP"

    def file_content(self,system,parallelism,spark_master,kafka_bootstrap_servers,db_url,db_name,db_user,db_password):
    #i am including a comma more than needed
        spark_m = f"spark://{spark_master}:7077"
        jdbc_url = f"jdbc:postgresql://{db_url}:5432/{db_name}"
        kafka_servers = ",".join(list(map(lambda x: f"{x}:9092",kafka_bootstrap_servers)))
        return f"""
        system = {system}
        parallelism = {parallelism}
        spark-master = {wrap_string(spark_m)}
        jdbc_url = {jdbc_url}
        kafka-bootstrap-servers = {wrap_string(kafka_servers)}
        db-user = {wrap_string(db_user)}
        db-password = {wrap_string(db_password)}
        """

    def read_from_json(self):

        # in self.json should be the file string, or the parsed thing to only do it once
        return "spark",self.json["spark"]["parallelism"],self.json["spark"]["master"],self.json["kafka"]["servers"],self.json["database"]["server"],self.json["database"]["db_name"],self.json["database"]["db_user"],self.json["database"]["db_password"]

    def output_file(self):
        system,parallelism,spark_master,kafka,db_url,db_name,db_user,db_password = self.read_from_json()
        file_content = self.file_content(system,parallelism,spark_master,kafka,db_url,db_name,db_user,db_password)
        if self.to_file:
            generate_file_in(file_content,self.file_path)
        else:
            print_string_with_filename_and_separator(self.label,file_content)

def main():
    if len(sys.argv) < 2:
        raise ValueException("did not provide a json file for config")
    json_config = sys.argv[1]
    print("Reading from argument: ", sys.argv[1])
    json_data = read_json_into_dict(sys.argv[1])
    print("The data is: ", json_data)
    ds_conf = DatasenderConf(json_data)
    ds_app_conf = DatasenderAppConf(json_data)
    ds_app_conf.output_file()
    content = ds_conf.file_content([("192.168.69.4")])
    tpc_conf = TpcGenPropertiesConf(json_data)
    # content = tpc_conf.file_content(3,"data")
    # print(content)
    esp_conf = ESPBenchCommonsConf(json_data)
    esp_conf.output_file()
    ansible_conf = AnsibleHostsConf(json_data)
    ansible_conf.output_file()
    apache_beam_conf = ApacheBeamConf(json_data)
    apache_beam_conf.output_file()
main()


    

# This is needed to generate consistent configs for ESPBench
