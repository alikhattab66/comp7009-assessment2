import hashlib
import secrets

DB = {}

def register(username, password):
    salt = secrets.token_hex(8)
    password_hash = hashlib.sha256((password + salt).encode("utf-8")).hexdigest()
    DB[username] = (salt, password_hash)
    print("Registered:", username)

def login(username, password):
    if username not in DB:
        print("Login OK? False")
        return

    salt, stored_hash = DB[username]
    password_hash = hashlib.sha256((password + salt).encode("utf-8")).hexdigest()
    print("Login OK?", password_hash == stored_hash)

username = input("Enter username for registration: ")
password = input("Enter password for registration: ")
register(username, password)

login_password = input("Enter password to log in: ")
login(username, login_password)

wrong_password = input("Enter a wrong password to test rejection: ")
login(username, wrong_password)