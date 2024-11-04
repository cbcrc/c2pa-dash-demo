import sys
from base64 import b64decode
from hashlib import sha256
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_PSS
import boto3
import logging
import argparse

def configure_logger(name, level=logging.DEBUG):
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    handler = logging.FileHandler('application.log')
    handler.setLevel(level)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger

logger = configure_logger("signer")

def parse_cli_args():
    """Parses command line arguments."""
    parser = argparse.ArgumentParser(description='Sign data using a private key.')
    parser.add_argument('--reserve-size', type=int, default=2048, help='Reserve size in bytes.')
    parser.add_argument('--alg', default='SHA256withRSA', help='Algorithm for signing.')
    parser.add_argument('--sign-cert-path', required=False, help='Path to the private key PEM file.')
    
    args = parser.parse_args()
    
    return args.reserve_size, args.alg, args.sign_cert_path


def read_bytes_from_stdin():
  """Reads bytes from standard input."""
  return sys.stdin.buffer.read()

def load_private_key(key_path):
  """Loads the private key from a PEM file."""
  with open(key_path, "rb") as key_file:
    pem_data = key_file.read()
  return RSA.importKey(pem_data)

def sign_bytes(data):
  """Signs the data using the private key and specified algorithm
  aws kms sign \
    --key-id [ insert your key id ] \
    --message $MESSAGE \
    --message-type RAW \
    --signing-algorithm ECDSA_SHA_256 \
    --output text \
    --query Signature
  """
  # call the cli script...
  client = boto3.client('kms')
  response = client.sign(   
    KeyId="arn:aws:kms:us-west-2:123456789012:key/12345678-1234-1234-1234-123456789012", # add your key id
    Message=data,
    MessageType='RAW',
    SigningAlgorithm='ECDSA_SHA_256'    
  )
  logger.debug("response: %s", response)
  return response

def write_bytes_to_stdout(data):
  """Writes bytes to standard output."""
  logger.debug(f"Writing signature to stdout {data}")
  sys.stdout.buffer.write(data)

def main():
  """Main function to read data, sign it, and write the signature."""
  data = read_bytes_from_stdin()
  reserve_size, alg, sign_cert_path = parse_cli_args()  # Simulated parsing
  signature = sign_bytes(data)
  write_bytes_to_stdout(signature['Signature'])

if __name__ == "__main__":
  main()
