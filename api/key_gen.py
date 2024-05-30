#!/usr/bin/python3
import uuid
import hashlib

"""Generate unique random IDs for Users, Listings etc"""

def uni_key_gen(val: str):
    #thanks to Sam Stoelinga
    hex_string = hashlib.md5(val.encode("UTF-8")).hexdigest()
    return uuid.UUID(hex=hex_string)