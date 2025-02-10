from confluent_kafka import Consumer, KafkaException, KafkaError

# Configuration du consommateur
conf = {
    'bootstrap.servers': 'localhost:9092',  # adresse du broker Kafka
    'group.id': 'python-consumer-group',
    'auto.offset.reset': 'earliest'
}

# Création de l'objet Consommateur
consumer = Consumer(conf)

# Souscription au topic
topic = 'test_topic'
consumer.subscribe([topic])

# Consommer des messages
try:
    while True:
        msg = consumer.poll(1.0)  # Attente d'un message pendant 1 seconde
        if msg is None:
            # Pas de message reçu dans le délai imparti
            continue
        if msg.error():
            if msg.error().code() == KafkaError._PARTITION_EOF:
                # Fin de partition
                print(f"Atteint la fin de la partition: {msg.topic()} [{msg.partition()}] à offset {msg.offset()}")
            else:
                raise KafkaException(msg.error())
        else:
            # Message reçu
            print(f"Message reçu: {msg.value().decode('utf-8')}")

except KeyboardInterrupt:
    pass
finally:
    # Fermeture propre
    consumer.close()
