#!/bin/sh

# Ждем, пока Kafka станет доступной
echo "Waiting for kafka starting"
while ! /opt/kafka/bin/kafka-topics.sh --bootstrap-server localhost:9092 --list; do
  sleep 5
done

# Создаем топики
echo "Topic creation...."
/opt/kafka/bin/kafka-topics.sh --create --topic image-color-to-grayscale --partitions 3 --replication-factor 1 --bootstrap-server localhost:9092
/opt/kafka/bin/kafka-topics.sh --create --topic image-color-to-grayscale-result --partitions 3 --replication-factor 1 --bootstrap-server localhost:9092
/opt/kafka/bin/kafka-topics.sh --create --topic image-grayscale-to-color --partitions 3 --replication-factor 1 --bootstrap-server localhost:9092
/opt/kafka/bin/kafka-topics.sh --create --topic image-grayscale-to-color-result --partitions 3 --replication-factor 1 --bootstrap-server localhost:9092
/opt/kafka/bin/kafka-topics.sh --create --topic image-crop --partitions 3 --replication-factor 1 --bootstrap-server localhost:9092
/opt/kafka/bin/kafka-topics.sh --create --topic image-crop-result --partitions 3 --replication-factor 1 --bootstrap-server localhost:9092
/opt/kafka/bin/kafka-topics.sh --create --topic image-rotate --partitions 3 --replication-factor 1 --bootstrap-server localhost:9092
/opt/kafka/bin/kafka-topics.sh --create --topic image-rotate-result --partitions 3 --replication-factor 1 --bootstrap-server localhost:9092
/opt/kafka/bin/kafka-topics.sh --create --topic image-style --partitions 3 --replication-factor 1 --bootstrap-server localhost:9092
/opt/kafka/bin/kafka-topics.sh --create --topic image-style-result --partitions 3 --replication-factor 1 --bootstrap-server localhost:9092
/opt/kafka/bin/kafka-topics.sh --create --topic image-metadata --partitions 3 --replication-factor 1 --bootstrap-server localhost:9092
/opt/kafka/bin/kafka-topics.sh --create --topic image-metadata-result --partitions 3 --replication-factor 1 --bootstrap-server localhost:9092

echo "All topics created!"