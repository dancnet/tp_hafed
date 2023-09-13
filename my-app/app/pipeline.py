import sys
import json
from kafka import KafkaConsumer
from pyspark import SparkConf, SparkContext
import happybase

def count_with_spark(data, devices, actions):
    '''Cette fonction calcule le nombre de fois qu'un evenement est survenu sur chaque appareil.'''
    conf = SparkConf().setAppName("count_device_actions").setMaster('spark://spark-master:7077')
    sc = SparkContext(conf=conf)
    rdd = sc.parallelize(data)
    count = {}
    for device in devices:
        count[device] = {}
        for action in actions:
            count[device][action] = rdd.filter(lambda x : x['action'] == action and x['device'] == device).count()
    sc.stop()
    return count

def save_to_hbase(data):
    '''Cette fonction enregistre dans la BD devices le count des actions pour chaque appareil.'''
    connection = happybase.Connection('hbase')
    table_name = 'devices'
    table = connection.table(table_name)
    for device in data:
        columns = {}
        for action in data[device]:
            columns[bytes('action:'+action.replace(' ', '_'), 'utf8')] = bytes(str(data[device][action]), 'utf8')
        table.put(
            bytes(device, 'utf-8'),
            columns
        )
    connection.close()

def process_received_data(data):
    '''Cette fonction est appelé chaque fois qu'un message est reçu dans Kafka.'''
    # Signal start
    print('Process started!')
    # JSON Parser
    parsed_data = json.loads(data)
    # Trouve les types d'actions et d'appareils
    devices = set([i['device'] for i in parsed_data])
    actions = set([i['action'] for i in parsed_data])
    # Compte
    count = count_with_spark(parsed_data, devices, actions)
    # Enregistre dans la BD
    save_to_hbase(count)
    # Signal end
    print('Process completed!')

# Lire les données à partir de Kafka
topic = 'data_capteurs'
consumer1 = KafkaConsumer(
    topic,
    bootstrap_servers=['kafka:9092'],
    auto_offset_reset='earliest',
    enable_auto_commit=True,
    group_id='my-group',
)
try:
    for message in consumer1:
        process_received_data(message.value)
except KeyboardInterrupt:
    sys.exit()