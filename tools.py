import argon2
import json


def check_username_password(username, password):
    # hash the username and password
    username = bytes(username, "UTF-8")
    password = bytes(password, "UTF-8")

    # open the config file as a json and read the hash of username and password
    with open('config.json') as json_file:
        data = json.load(json_file)
        username_hash = bytes(data['username'], "UTF-8")
        password_hash = bytes(data['password'], "UTF-8")
        pulbic_id = data['public_id']
        #argon2.verify_password(username_hash, username)
    try:
        argon2.verify_password(password_hash, password)  
        argon2.verify_password(username_hash, username)
        return True, pulbic_id
    except:
        return False, None




