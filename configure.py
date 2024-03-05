
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
        total_string += "\t" + wrap_string(i) + "\n"
    return total_string + "\t"+ "]"


def datasender_conf(ip_port_tuple_list,input_paths=["~/Benchmarks/ESB/Data/5MinutesMachine1.csv",
	"~/Benchmarks/ESB/Data/5MinutesMachine2.csv",
	"~/Benchmarks/ESB/Data/production_times.csv"],read_in_ram=True):
    #i am including a comma more than needed
    kafka_bootstrap_servers = get_string_from_ip_port_list(ip_port_tuple_list,9092)
    input_paths_arr = string_array_from(input_paths)
    file_content = f"""
    {property_equals("kafka-producer-config.bootstrap-servers",wrap_string(kafka_bootstrap_servers))}
    {property_equals("kafka-producer-config.key-serializer-class",wrap_string(kafka_key_serializer_class()))}
    {property_equals("kafka-producer-config.value-serializer-class",1)}
    {property_equals("kafka-producer-config.acks",1)}
    {property_equals("kafka-producer-config.batch-size",16384)}
    {property_equals("kafka-producer-config.buffer-memory-size",33554432)}
    {property_equals("kafka-producer-config.linger-time",0)}
    {property_equals("data-reader-config.data-input-path",input_paths_arr)}
    {property_equals("data-reader-config.read-in-ram","false")}
"""
    return file_content

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


def tpc_gen_properties_conf(number_of_warehouses,output_dir):
    return f"""
    {property_equals("NUMBER_OF_WAREHOUSES",number_of_warehouses)}
    {property_equals("OUTPUT_DIR",wrap_string(output_dir))} 
    """

def apache_beam_properties(system,parallelism,spark_master,kafka_bootstrap_servers,db_url,db_name,db_user,db_password):
    spark_m = f"spark://{spark_master}:7077"
    jdbc_url = f"jdbc:postgresql://{db_url}:5432/{db_name}"
    kafka_servers = ",".join(list(map(lambda x: f"{x}:9092",kafka_bootstrap_servers)))
    return f"""
    {property_equals("system",system)}
    {property_equals("parallelism",parallelism)}
    {property_equals("spark-master",wrap_string(spark_m))}
    {property_equals("kafka-bootstrap-servers",wrap_string(kafka_servers))}
    {property_equals("db-user",wrap_string(db_user))}
    {property_equals("db-password",wrap_string(db_password))}
    """
print("hello world")

def commons_conf(topic_prefix,benchmark_run,query_configs_arr,kafka_bootstrap_servers,zookeeper_servers,sending_interval=10000000,sending_interval_time_unit="NANOSECONDS",duration=10,duration_time_unit="Minutes"):
    kafka_servers = ",".join(list(map(lambda x: f"{x}:9092",kafka_bootstrap_servers)))
    zookeeper = ",".join(list(map(lambda x: f"{x}:2181",zookeeper_servers)))
    queries = ",\n".join(list(map(lambda x: obj(x,2),query_configs_arr)))
    query_configs_str = "[" + "\n" + queries + "\n"+ "  ]"
    return f"""
    {property_equals("topic-prefix",wrap_string(topic_prefix))}
    {property_equals("benchmark-run",benchmark_run)}
    {property_equals("query-configs",query_configs_str)}
    {property_equals("sending-interval",sending_interval)}
    {property_equals("sending-interval-time-unit",wrap_string(sending_interval_time_unit))}
    {property_equals("duration",duration)}
    {property_equals("duration-time-unit",wrap_string(duration_time_unit))}
    {property_equals("kafka-bootstrap-servers",wrap_string(kafka_servers))}
    {property_equals("zookeeper-servers",wrap_string(zookeeper))}
    """

DRY_RUN = True
def output_file_in(file_content,path,label):
    if not DRY_RUN:
        generate_file_in(file_content,path)
    else:
        print(f"Generating in path {path}")
        print_string_with_filename_and_separator(label,file_content)

def main():
    ds_conf = datasender_conf([("192.168.69.4")])
    ds_conf_path = "./tools/datasender/datasender.conf"
    output_file_in(ds_conf,ds_conf_path,"datasender.conf")    
    tpc_gen_file = tpc_gen_properties_conf(3,"data")
    tpc_gen_file_path = "./tools/tpc-c_gen/tpc-c.properties"
    output_file_in(tpc_gen_file, tpc_gen_file_path,"tpc-c.properties")       
    apache_beam_file = apache_beam_properties("spark",1,"192.168.68.3",["192.168.69.4"],"192.168.69.5","hessebench","benchmarker","benchmark")
    apache_beam_file_path = "./implementation/beam/src/main/resources/beam.properties"
    output_file_in(apache_beam_file,apache_beam_file_path,"beam.properties")
    commons_conf_file = commons_conf("HPC-TEAM",1,[{"name":"Identity","number-of-streams":1}],["192.168.69.4"],["192.168.69.4"])
    commons_conf_file_path = "./tools/commons/commons.conf"
    output_file_in(commons_conf_file,commons_conf_file_path,"commons.conf")

main()


    

# This is needed to generate consistent configs for ESPBench
