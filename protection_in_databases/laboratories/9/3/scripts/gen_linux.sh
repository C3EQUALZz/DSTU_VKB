#!/bin/bash -xe
## gen_certs_rsa.sh

# Default values
COUNTRY='US'
STATE='California'
LOCATION='Santa Clara'
BLOCK_SIZE=4096
DAYS=365

read -p "Enter country code [empty for default value - US]: " -r
if [ ! -z "$REPLY" ]
then
    COUNTRY=$REPLY
fi
read -p "Enter state [empty for default value - California]: " -r
if [ ! -z "$REPLY" ]
then
    STATE=$REPLY
fi
read -p "Enter location [empty for default value - Santa Clara]: " -r
if [ ! -z "$REPLY" ]
then
    LOCATION=$REPLY
fi
read -p "Enter block size [empty for default value - 4096]: " -r
if [ ! -z "$REPLY" ]
then
    BLOCK_SIZE=$REPLY
fi
read -p "Enter expiration length [empty for default value - 365]: " -r
if [ ! -z "$REPLY" ]
then
    DAYS=$REPLY
fi

OPENSSL_SUBJ="/C=${COUNTRY}/ST=${STATE}/L=${LOCATION}"
OPENSSL_CA="$OPENSSL_SUBJ/CN=fake-CA"
OPENSSL_SERVER="$OPENSSL_SUBJ/CN=fake-server"
OPENSSL_CLIENT="$OPENSSL_SUBJ/CN=user2"

mkdir certs

# Generate new CA certificate ca.pem file.
openssl genrsa $BLOCK_SIZE > certs/ca-key.pem

openssl req -new -x509 -nodes -days $DAYS \
    -subj "$OPENSSL_CA" \
    -key certs/ca-key.pem -out certs/ca.pem

# Create the server-side certificates
openssl req -newkey rsa:$BLOCK_SIZE -nodes \
    -subj "$OPENSSL_SUBJ" \
    -keyout certs/server-key.pem -out certs/server-req.pem

# Use old format for key
openssl rsa -in certs/server-key.pem -out certs/server-key.pem

openssl x509 -req -in certs/server-req.pem -days $DAYS \
    -CA certs/ca.pem -CAkey certs/ca-key.pem -set_serial 01 -out certs/server-cert.pem

# # Create the client-side certificates
openssl req -newkey rsa:$BLOCK_SIZE -nodes \
    -subj "$OPENSSL_CLIENT" \
    -keyout certs/client-key.pem -out certs/client-req.pem

# Use old format for key
openssl rsa -in certs/client-key.pem -out certs/client-key.pem

openssl x509 -req -in certs/client-req.pem -days $DAYS \
    -CA certs/ca.pem -CAkey certs/ca-key.pem -set_serial 01 -out certs/client-cert.pem

# # Verify the certificates are correct
openssl verify -CAfile certs/ca.pem certs/server-cert.pem certs/client-cert.pem

# Insecure but required for mysql user to be able to read the certs
chmod -R +r certs/