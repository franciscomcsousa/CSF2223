# decompyle3 version 3.9.0
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.10 (default, Mar 15 2022, 12:22:08) 
# [GCC 9.4.0]
# Embedded file name: cipher.py
# Compiled at: 2022-09-23 20:25:49
# Size of source mod 2**32: 3990 bytes
import hashlib, os
from base64io import Base64IO as b64
ENCRYPTED_SUFFIX = 'enc'
DECRYPTED_SUFFIX = 'dec'
TOOL_URL = b'http://tiny.cc/7o2d6LuDVNSd'
TOOL_URL_HEADER_SIZE = 64
PASSWORD_HASH_SIZE = 64
PASSWORD_HASH_ITERATIONS = 25000
MIN_PWD_CHARS = 4

def readable_size(value: int) -> str:
    if value < 1024:
        return f"{value}B"
    if value < 1048576:
        return f"{value / 1024:.2f}KB"
    if value < 1073741824:
        return f"{value / 1048576:.2f}MB"
    return f"{value / 1073741824:.2f}GB"


def print_progress_bar(current: int, total: int):
    max_size = 80
    bar_size = round(max_size * current / total)
    print(f"[{'#' * bar_size}{'-' * (max_size - bar_size)}] ({readable_size(current)}/{readable_size(total)}){'          '}", end='\r', flush=True)


def one_time_pad(block: bytes, block_key: bytes):
    result = b''
    for i in range(len(block)):
        result += bytes([block[i] ^ block_key[i]])

    return result


def encrypt_file(filename: str, password: str, mode: str):
    input_file_size = os.path.getsize(filename)
    if mode == 'e':
        source = open(filename, mode='rb')
        target_aux = open(f"{filename}_{ENCRYPTED_SUFFIX}", mode='wb')
        target = b64(target_aux)
    else:
        source_aux = open(filename, mode='rb')
        source = b64(source_aux)
        target = open(f"{filename}_{DECRYPTED_SUFFIX}", mode='wb')
        input_file_size = input_file_size * 6 / 8 - (TOOL_URL_HEADER_SIZE + PASSWORD_HASH_SIZE)
    if mode == 'e':
        target.write(TOOL_URL + b'\x00' * (TOOL_URL_HEADER_SIZE - len(TOOL_URL)))
        target.write(get_password_hash(password))
    else:
        source.read(TOOL_URL_HEADER_SIZE)
        source.read(PASSWORD_HASH_SIZE)
    finished_size = 0
    block_key = hashlib.sha512(password.encode('utf-8')).digest()
    while True:
        block = source.read(len(block_key))
        if len(block) <= 0:
            break
        else:
            target.write(one_time_pad(block, block_key))
            finished_size += len(block)
            print_progress_bar(finished_size, round(input_file_size))
            block_key = hashlib.sha512(block_key).digest()

    print()
    target.close()
    source.close()
    if mode == 'e':
        target_aux.close()
    else:
        source_aux.close()


def get_password_hash(password: str) -> bytes:
    hash = password.encode('utf-8')
    for _ in range(PASSWORD_HASH_ITERATIONS):
        hash = hashlib.sha512(hash).digest()

    return hash


def check_password(filename: str, password: str):
    with open((f"{filename}"), mode='rb') as encoded_source:
        with b64(encoded_source) as source:
            source.read(TOOL_URL_HEADER_SIZE)
            hash = source.read(PASSWORD_HASH_SIZE)
            if get_password_hash(password) == hash:
                print('Password is correct!')
            else:
                print('Password is incorrect! Aborting...')
                exit(1)


print('[---------------------------- Select Mode ----------------------------]')
objective = ''
while objective == '':
    objective = input('Encrypt or decrypt? (e/d): ').lower()
    if objective not in ('e', 'd'):
        print('Invalid input!')
        objective = ''

print('[---------------------------- Select File ----------------------------]')
filename = ''
while filename == '':
    filename = input('Name of the file: ')
    if not os.path.isfile(filename):
        print('File not found!')
        filename = ''

print('[-------------------------- Enter Password ---------------------------]')
password = ''
while password == '':
    password = input('Password: ')
    if len(password) < MIN_PWD_CHARS:
        print(f"Password must be at least {MIN_PWD_CHARS} characters long!")
        password = ''

print('[--------------------------- Confirmation ----------------------------]')
print(f"'{filename}' ({readable_size(os.path.getsize(filename))}) will be {'enc' if objective == 'e' else 'dec'}rypted with the password '{password}'.")
if input('Are you sure? (y/n): ').lower() == 'y':
    if objective == 'd':
        check_password(filename, password)
    print('Starting...')
    encrypt_file(filename, password, objective)
    print('Done!')
else:
    print('Aborting...')
    exit(0)
# okay decompiling tool.pyc