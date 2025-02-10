from confluent_kafka import Producer

conf = {'bootstrap.servers': 'localhost:9092'}
producer = Producer(conf)

def delivery_report(err, msg):
    if err is not None:
        print(f"Erreur: {err}")
    else:
        print(f"Message envoyé: {msg.value().decode()}")

for i in range(5):
    producer.produce('test-topic', f'Message {i}', callback=delivery_report)

producer.flush()
