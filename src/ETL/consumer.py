from kafka import KafkaConsumer, KafkaProducer
import json
from databases.mysql_connect import MySQLConnect
from config.database_config import get_database_config

def validate_record(record, expected_count):
    message_id = f"{record.get('user_id', 'unknown')}_{record.get('log_timestamp', 'unknown')}"
    if 'count_number' not in record or not isinstance(record['count_number'], int) or record['count_number'] <= 0:
        return False, message_id, f"Invalid count_number: {record.get('count_number')}", expected_count
    if record['count_number'] == expected_count:
        return True, message_id, None, expected_count + 1
    elif record['count_number'] == 1:
        return True, message_id, None, 2
    else:
        return False, message_id, f"Count number mismatch: expected {expected_count}, got {record['count_number']}", expected_count

def consume_and_validate():
    config = get_database_config()
    expected_count = 1
    valid_record_count = 0  # Track valid records in current batch
    total_valid_records = 0  # Track total valid records across all batches

    with MySQLConnect(config["mysql"].host, config["mysql"].port, config["mysql"].user,
                      config["mysql"].password) as mysql_client:
        consumer = KafkaConsumer(
            "vnontop",
            bootstrap_servers="192.168.2.26:9092",
            group_id="my_consumer_group",
            auto_offset_reset="latest",
            value_deserializer=lambda x: json.loads(x.decode('utf-8')),
            enable_auto_commit=False
        )
        dlq_producer = KafkaProducer(
            bootstrap_servers="192.168.2.26:9092",
            value_serializer=lambda x: json.dumps(x).encode('utf-8')
        )
        spark_producer = KafkaProducer(
            bootstrap_servers="192.168.2.26:9092",
            value_serializer=lambda x: json.dumps(x).encode('utf-8')
        )

        for message in consumer:
            record = message.value
            print(f"Received record: {record}")
            is_valid, message_id, error_reason, expected_count = validate_record(record, expected_count)

            if is_valid:
                spark_producer.send("spark_input", record)
                spark_producer.flush()
                valid_record_count += 1
                total_valid_records += 1
                print(f"Sent valid record to spark_input topic: message_id {message_id}")
                print(f"Valid records in current batch: {valid_record_count}")
                print(f"Total valid records processed: {total_valid_records}")
                if record['count_number'] == 1 and valid_record_count > 1:
                    print(f"Completed batch with {valid_record_count} records")
                    valid_record_count = 1  # Reset for new batch
            else:
                invalid_record = {
                    "original_record": record,
                    "error_reason": error_reason,
                    "timestamp": message.timestamp,
                    "topic": message.topic,
                    "partition": message.partition,
                    "offset": message.offset
                }
                dlq_producer.send("vnontop_dead_letter_queue", invalid_record)
                dlq_producer.flush()
                print(f"Sent invalid record to dead-letter queue: {invalid_record}")

            consumer.commit()

if __name__ == "__main__":
    consume_and_validate()
