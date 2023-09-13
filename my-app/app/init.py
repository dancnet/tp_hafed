from kafka.admin import KafkaAdminClient, NewTopic
import happybase

# Create Kafka Topic
admin_client = KafkaAdminClient(
    bootstrap_servers='kafka:9092', 
    client_id='test'
)
topic_list = []
topic_list.append(NewTopic(name="data_capteurs", num_partitions=1, replication_factor=1))
admin_client.create_topics(new_topics=topic_list, validate_only=False)

# Create HBase table.
connection = happybase.Connection('hbase')
table_name = 'devices'
if table_name.encode() not in connection.tables():
    connection.create_table(
        table_name,
        {
            'action': dict(max_versions=10)
        }
    )