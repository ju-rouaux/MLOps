from confluent_kafka import Consumer, KafkaException, KafkaError

# Configuration du consommateur Kafka
conf = {
    'bootstrap.servers': 'localhost:9092',  # Adresse du serveur Kafka
    'group.id': 'mon-groupe-consommateur',  # Identifiant du groupe de consommateurs
    'auto.offset.reset': 'earliest',  # Lire tous les messages depuis le début
    'security.protocol': 'PLAINTEXT',  # Utiliser le mode de connexion non sécurisé
}

# Créer le consommateur
consumer = Consumer(conf)

# S'abonner au topic
consumer.subscribe(['test-topic'])

print("📡 En attente de messages Kafka...")

try:
    while True:
        msg = consumer.poll(1.0)  # Vérifie les messages toutes les secondes

        if msg is None:
            continue
        if msg.error():
            if msg.error().code() == KafkaError._PARTITION_EOF:
                continue
            else:
                raise KafkaException(msg.error())

        # Affiche le message reçu
        print(f"📥 Message reçu : {msg.value().decode('utf-8')}")

except KeyboardInterrupt:
    print("\n📴 Arrêt du consommateur")
finally:
    consumer.close()
