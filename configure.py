

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
        total_string += "\t" + i + "\n"
    return total_string + "\t"+ "]"


def datasender_conf(ip_port_tuple_list,input_paths=["~/Benchmarks/ESB/Data/5MinutesMachine1.csv",
	"~/Benchmarks/ESB/Data/5MinutesMachine2.csv",
	"~/Benchmarks/ESB/Data/production_times.csv"],read_in_ram=True):
    kafka_bootstrap_servers = get_string_from_ip_port_list(ip_port_tuple_list,9092)
    input_paths_arr = string_array_from(input_paths)
    file_content = f"""
    {property_equals("kafka-producer-config.bootstrap-servers",kafka_bootstrap_servers)}
    {property_equals("kafka-producer-config.key-serializer-class",kafka_key_serializer_class())}
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

def property_equals(property_name, val):
    return f"{property_name} = {val}"

def kafka_key_serializer_class():
    return "org.apache.kafka.common.serialization.StringSerializer"
def kafka_value_serializer_class():
    return "org.apache.kafka.common.serialization.StringSerializer"

print("hello world")

print(datasender_conf([("192.168.69.4")]))


# This is needed to generate consistent configs for ESPBench
