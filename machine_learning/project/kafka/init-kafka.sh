#!/bin/sh

set -e

# Ждем, пока Kafka станет доступной
echo "Waiting for kafka starting"
while ! kafka-topics.sh --bootstrap-server broker:29092 --list; do
  sleep 5
done

# Создаем топики
echo "Topic creation...."
kafka-topics.sh --create --if-not-exists --topic image-color-to-grayscale --partitions 3 --replication-factor 1 --bootstrap-server broker:29092
kafka-topics.sh --create --if-not-exists --topic image-color-to-grayscale-result --partitions 3 --replication-factor 1 --bootstrap-server broker:29092
kafka-topics.sh --create --if-not-exists --topic image-grayscale-to-color --partitions 3 --replication-factor 1 --bootstrap-server broker:29092
kafka-topics.sh --create --if-not-exists --topic image-grayscale-to-color-result --partitions 3 --replication-factor 1 --bootstrap-server broker:29092
kafka-topics.sh --create --if-not-exists --topic image-crop --partitions 3 --replication-factor 1 --bootstrap-server broker:29092
kafka-topics.sh --create --if-not-exists --topic image-crop-result --partitions 3 --replication-factor 1 --bootstrap-server broker:29092
kafka-topics.sh --create --if-not-exists --topic image-rotate --partitions 3 --replication-factor 1 --bootstrap-server broker:29092
kafka-topics.sh --create --if-not-exists --topic image-rotate-result --partitions 3 --replication-factor 1 --bootstrap-server broker:29092
kafka-topics.sh --create --if-not-exists --topic image-style --partitions 3 --replication-factor 1 --bootstrap-server broker:29092
kafka-topics.sh --create --if-not-exists --topic image-style-result --partitions 3 --replication-factor 1 --bootstrap-server broker:29092
kafka-topics.sh --create --if-not-exists --topic image-metadata --partitions 3 --replication-factor 1 --bootstrap-server broker:29092
kafka-topics.sh --create --if-not-exists --topic image-metadata-result --partitions 3 --replication-factor 1 --bootstrap-server broker:29092

echo "All topics created!"