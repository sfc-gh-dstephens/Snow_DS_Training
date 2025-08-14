#!/bin/bash
set -e

echo "Creating directory for keys"
mkdir -p ~/.snowflake/keys
cd ~/.snowflake/keys

openssl genrsa 2048 | openssl pkcs8 -topk8 -inform PEM -out rsa_key.p8 -nocrypt

openssl rsa -in rsa_key.p8 -pubout -out rsa_key.pub

chmod 600 rsa_key.p8
chmod 644 rsa_key.pub

## run this in the terminal to generate keys
# chmod +x create-keys.sh 
# sh create-keys.sh

## Create python env
# uv init
# uv sync
# source .venv/bin/activate
# uv add requests pyJWT cryptography

