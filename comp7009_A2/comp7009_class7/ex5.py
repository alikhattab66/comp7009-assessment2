import random

def encrypt(message, key):
    return f"enc({message})with[{key}]"

def decrypt(ciphertext, key):
    prefix = "enc("
    suffix = f")with[{key}]"
    if ciphertext.startswith(prefix) and ciphertext.endswith(suffix):
        return ciphertext[len(prefix):-len(suffix)]
    return None

Kbs = "Key_BS"

print("Needham-Schroeder Replay Attack Demonstration\n")

# Recorded values from an earlier genuine session
recorded_Kab = "OldSessionKey123"
recorded_message3 = encrypt(f"{recorded_Kab},A", Kbs)

print("Assumptions for the replay attack:")
print(f"- Eve has learned an old session key K_AB = {recorded_Kab}")
print(f"- Eve recorded an old Message 3 = {recorded_message3}")
print(f"- B still uses the same long-term shared key with S: K_BS = {Kbs}\n")

print("Replay attack begins:")

# Replayed Step 3
print(f"3) Eve -> B : {recorded_message3}")

decrypted_ticket = decrypt(recorded_message3, Kbs)
if decrypted_ticket is None:
    print("Replay attack failed: B could not decrypt the recorded ticket.")
    raise SystemExit

parts = decrypted_ticket.split(",")
if len(parts) != 2:
    print("Replay attack failed: malformed recorded ticket.")
    raise SystemExit

kab_from_ticket, claimed_identity = parts
print(f"B decrypts recorded ticket: Kab={kab_from_ticket}, claimed sender={claimed_identity}")
print("B has no freshness check here, so B accepts the old ticket as valid.")

# Step 4
Nb = random.randint(1000, 9999)
message4 = encrypt(str(Nb), kab_from_ticket)
print(f"\n4) B -> A : {message4}")
print("Bob believes he is challenging Alice, but the message is actually received by Eve.")

decrypted_challenge = decrypt(message4, recorded_Kab)
if decrypted_challenge is None:
    print("Replay attack failed: Eve could not decrypt Bob's challenge.")
    raise SystemExit

print(f"Eve decrypts Bob's challenge using the compromised old Kab and gets Nb={decrypted_challenge}")

# Step 5
message5 = encrypt(str(int(decrypted_challenge) - 1), recorded_Kab)
print(f"\n5) Eve -> B : {message5}")

decrypted_response = decrypt(message5, kab_from_ticket)
if decrypted_response is None:
    print("Replay attack failed: B could not decrypt Eve's response.")
    raise SystemExit

print(f"B decrypts response: {decrypted_response}")

if decrypted_response == str(Nb - 1):
    print("\nReplay attack successful: B accepts Eve as Alice.")
    print("This works because Eve reused an old Message 3 and an old compromised session key Kab.")
else:
    print("\nReplay attack failed: response was not Nb-1.")