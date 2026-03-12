import hashlib
import time

salt = "mysalt"
HSP = None

def hash_data(data):
    return hashlib.sha256(data.encode("utf-8")).hexdigest()

def register(password):
    global HSP
    HSP = hash_data(password + salt)
    print("Registration successful.")
    print("Initial HSP:", HSP)

def generate_otp():
    global HSP
    t = str(int(time.time()))
    HSP = hash_data(HSP + t)
    otp = HSP[-6:]
    print("Updated HSP:", HSP)
    print("Generated OTP (simulated SMS):", otp)
    return otp

def verify_otp(user_input):
    expected = HSP[-6:]
    if user_input == expected:
        print("Login successful.")
    else:
        print("Login failed.")

password = input("Enter password for registration: ")
register(password)

otp = generate_otp()
user_otp = input("Enter the OTP you received: ")
verify_otp(user_otp)

wrong_otp = input("Enter a wrong OTP to test rejection: ")
verify_otp(wrong_otp)
