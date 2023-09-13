from os import listdir
from os.path import isfile, join
import time
from kafka import KafkaProducer

# Kafka functions
def error_callback(exc):
    raise Exception('Error while sendig data to kafka: {0}'.format(str(exc)))

def write_to_kafka(topic_name, items):
    count=0
    producer = KafkaProducer(bootstrap_servers=['kafka:9092'])
    for key, message in items:
        producer.send(topic_name, key=key.encode('utf-8'), value=message.encode('utf-8')).add_errback(error_callback)
        count+=1
    producer.flush()
    print("Wrote {0} messages into topic: {1}".format(count, topic_name))

# For every file in capteurs_data...
path = './capteurs_data'
files = [f for f in listdir(path) if isfile(join(path, f))]
for file in files:
    with open(join(path,file)) as f:
        # ... send the file contents to kafka
        data = f.read()
        write_to_kafka("data_capteurs", ((file, data),))
    # wait 20 seconds before sending more to simulate batch...
    time.sleep(20)