# Utiliser une image de base Java
FROM openjdk:11-jre-slim

# Définir des variables d'environnement pour Kafka et Zookeeper
ENV KAFKA_VERSION=3.5.0 \
    SCALA_VERSION=2.13 \
    KAFKA_HOME=/opt/kafka

# Télécharger Kafka
RUN apt-get update && apt-get install -y wget \
    && wget https://archive.apache.org/dist/kafka/${KAFKA_VERSION}/kafka_${SCALA_VERSION}-${KAFKA_VERSION}.tgz \
    && mkdir -p $KAFKA_HOME \
    && tar -xzf kafka_${SCALA_VERSION}-${KAFKA_VERSION}.tgz -C $KAFKA_HOME --strip-components=1 \
    && rm -f kafka_${SCALA_VERSION}-${KAFKA_VERSION}.tgz \
    && apt-get clean && rm -rf /var/lib/apt/lists/*


# Installer pip et confluent_kafka pour Python
RUN apt-get update && apt-get install -y python3 python3-pip \
    && pip3 install confluent_kafka


# Exposer les ports Kafka et Zookeeper
EXPOSE 9092 2181

# Ajouter les scripts de démarrage
COPY start.sh /usr/bin/start.sh
RUN chmod +x /usr/bin/start.sh

# Définir le point d'entrée
ENTRYPOINT ["/usr/bin/start.sh"]
