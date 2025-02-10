from confluent_kafka import Producer
import sys

# Configuration du producteur
conf = {
    'bootstrap.servers': 'localhost:9092',  # adresse du broker Kafka
    'client.id': 'python-producer'
}

# Création de l'objet Producteur
producer = Producer(conf)

# Fonction de callback pour la gestion des erreurs
def delivery_report(err, msg):
    if err is not None:
        print('Erreur lors de l\'envoi du message: {}'.format(err))
    else:
        print('Message envoyé avec succès à {} [{}]'.format(msg.topic(), msg.partition()))

# Envoi de messages
topic = 'test_topic'
for i in range(10):
    message = f'Message {i}'
    producer.produce(topic, message.encode('utf-8'), callback=delivery_report)
    producer.poll(0)

# Attendre que tous les messages aient été envoyés avant de terminer
producer.flush()
