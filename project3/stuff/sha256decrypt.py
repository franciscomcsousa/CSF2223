#!/usr/bin/python
import urllib.request
import urllib.parse
import http.client
import subprocess
import sys
import base64
import os
from Crypto import Random
from Crypto.Cipher import AES
import hashlib
 
password = "Fj39@vF4@54&8dE@!)(*^+-pL;'dK3J2"
 
def encrypt(raw, password, downloadFlag):
    private_key = hashlib.sha256(password.encode("utf-8")).digest()
    iv = Random.new().read(AES.block_size)
    cipher = AES.new(private_key, AES.MODE_CFB, iv)
    if downloadFlag == 0: #cmd
        return base64.b64encode(iv + cipher.encrypt(str.encode(raw)))
    return base64.b64encode(iv + cipher.encrypt(raw)) #download
 
 
def decrypt(enc, password):
    private_key = hashlib.sha256(password.encode("utf-8")).digest()
    enc = base64.b64decode(enc)
    iv = enc[:16]
    cipher = AES.new(private_key, AES.MODE_CFB, iv)
    return cipher.decrypt(enc[16:])


file1 = open("file.txt", "r")

message = str(decrypt(file1.read(), password), 'utf-8')

#print(str(decrypt(file1.read(), password), 'utf-8'))
#print(file1.read())
