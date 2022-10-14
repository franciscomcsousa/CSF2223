# uncompyle6 version 3.5.0
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.5 (default, Nov 16 2020, 22:23:17) 
# [GCC 4.8.5 20150623 (Red Hat 4.8.5-44)]
# Embedded file name: obfuscator.py
# Compiled at: 2022-10-07 23:07:20
import hashlib, sys
with open('seeds.txt', 'r') as (f):
    lines = f.readlines()
with open('seeds.txt', 'w') as (f):
    for line in lines[1:]:
        f.write(line)
    else:
        f.write(lines[0])

pw = hashlib.sha256(str(lines[0] + str(sys.argv[1])).encode('utf-8'))
print pw.hexdigest()
