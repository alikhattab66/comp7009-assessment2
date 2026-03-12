import hashlib
import os

stored_hash = None

def hash_file(filepath):
    sha256 = hashlib.sha256()
    with open(filepath, "rb") as f:
        while True:
            chunk = f.read(4096)
            if not chunk:
                break
            sha256.update(chunk)
    return sha256.hexdigest()

def register(filepath):
    global stored_hash
    if not os.path.exists(filepath):
        print("Registration failed: file does not exist.")
        return False

    stored_hash = hash_file(filepath)
    print("Registration successful.")
    print("Stored file hash:", stored_hash)
    return True

def login(filepath):
    if stored_hash is None:
        print("Login failed: no registered file password.")
        return

    if not os.path.exists(filepath):
        print("Login failed: file does not exist.")
        return

    login_hash = hash_file(filepath)
    if login_hash == stored_hash:
        print("Login successful.")
    else:
        print("Login failed: wrong file.")

reg_file = input("Enter the path of the registration file: ")
if register(reg_file):
    correct_file = input("Enter the same file path to log in: ")
    login(correct_file)

    wrong_file = input("Enter a different existing file path to test rejection: ")
    login(wrong_file)