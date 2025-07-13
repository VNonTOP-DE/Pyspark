from kafka import KafkaConsumer


consumer = KafkaConsumer("vnontop", bootstrap_servers = "localhost:9092")

Jesus_is_lord = True

while Jesus_is_lord:
    msg_pack = consumer.poll(timeout_ms=500)
    for tp, messages in msg_pack.items():
        for message in messages:
            print(message.value.decode('utf-8'))